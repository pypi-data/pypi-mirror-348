"""Strangeworks Qiskit Runtime Service."""

import logging
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

import strangeworks
from qiskit_ibm_runtime import ibm_backend
from qiskit_ibm_runtime.accounts import ChannelType
from qiskit_ibm_runtime.api.exceptions import RequestsApiError
from qiskit_ibm_runtime.exceptions import IBMRuntimeError, RuntimeProgramNotFound
from qiskit_ibm_runtime.ibm_backend import IBMBackend
from qiskit_ibm_runtime.runtime_options import RuntimeOptions
from qiskit_ibm_runtime.utils.backend_decoder import configuration_from_server_data
from qiskit_ibm_runtime.utils.result_decoder import ResultDecoder
from strangeworks.core.errors.error import StrangeworksError

from .runtime_client import StrangeworksRuntimeClient
from .sw_runtime_job import StrangeworksRuntimeJob

logger = logging.getLogger(__name__)

SERVICE_NAME = "sw_runtime"


class StrangeworksQiskitRuntimeService:
    """Class for interacting with the Qiskit Runtime service.

    Qiskit Runtime is a new architecture offered by IBM Quantum that
    streamlines computations requiring many iterations. These experiments will
    execute significantly faster within its improved hybrid quantum/classical
    process.
    """

    def __init__(
        self,
        resource_slug: Optional[str] = None,
        channel: Optional[ChannelType] = "ibm_cloud",
    ) -> None:
        """StrangeworksQiskitRuntimeService constructor

        Args:
            channel: Channel type. ``ibm_cloud`` or ``ibm_quantum``.
        Returns:
            An instance of StrangeworksQiskitRuntimeService.

        Raises:
            IBMInputValueError: If an input is invalid.
        """

        ibm_warning = "WARNING From IBM: After March 31, 2024 Qiskit Runtime sessions creation will gain exclusive access to quantum systems, and will be charged for all time from the first job in the session, until the session is closed."  # noqa
        print(ibm_warning)

        if resource_slug is not None:
            self.rsc = strangeworks.resources(slug=resource_slug)[0]
            if self.rsc:
                if self.rsc.product.slug == "ibm-quantum":
                    channel = "ibm_quantum"
                elif self.rsc.product.slug == "ibm-qiskit-runtime":
                    channel = "ibm_cloud"
            else:
                raise StrangeworksError(f"Invalid resource slug '{resource_slug}'.")
        elif channel is not None:
            if channel == "ibm_quantum":
                product_slug = "ibm-quantum"
            elif channel == "ibm_cloud":
                product_slug = "ibm-qiskit-runtime"
            else:
                raise StrangeworksError(
                    f"Invalid channel type '{channel}'. "
                    f"Valid channel types are 'ibm_quantum' and 'ibm_cloud'."
                )
            rsc_list = strangeworks.resources()
            if not rsc_list and len(rsc_list) == 0:
                raise StrangeworksError(
                    "No resources found. Contact Strangeworks Support to Add a Resource to your account."  # noqa
                )
            for rr in range(len(rsc_list)):
                if rsc_list[rr].product.slug == product_slug:
                    self.rsc = rsc_list[rr]
                    break
        else:
            raise StrangeworksError("Must specify either a channel or reource slug.")
        self._api_client = StrangeworksRuntimeClient(channel=channel, rsc=self.rsc)
        self.channel = channel
        self._channel = channel
        self._channel_strategy = None

    def backend_options(
        self,
        name: Optional[str] = None,
        combined: Dict[str, Any] = None,
        min_num_qubits: Optional[int] = None,
        instance: Optional[str] = None,
        filters: Optional[Callable[[List["ibm_backend.IBMBackend"]], bool]] = None,
        **kwargs: Any,
    ) -> List["ibm_backend.IBMBackend"]:
        """Return all backends accessible via this account, subject to optional
        filtering.
        """

        payload = {
            "runtime": True,
            "channel": self.channel,
            "name": name,
            "combined": combined,
            "min_num_qubits": min_num_qubits,
            "instance": instance,
            "filters": filters,
            "kwargs": kwargs,
        }
        response = strangeworks.execute(self.rsc, payload, "runtime_backends")

        return response.get("inputs"), response.get("outputs")

    def backends(
        self,
    ) -> IBMBackend:
        """Return a list of available backends."""
        return strangeworks.backends(product_slugs="ibm-qiskit-runtime")

    def backend(
        self,
        name: str = None,
        instance: Optional[str] = None,
    ) -> IBMBackend:
        """Return a single backend matching the specified filtering."""
        backends = self.backends()
        for b in backends:
            if b.name == name:
                backend = b

        # To-Do: Need to get backend configuration from service side
        payload = {
            "runtime": True,
            "channel": self.channel,
            "name": name,
        }
        raw_config = strangeworks.execute(self.rsc, payload, "runtime_backend_config")
        config = configuration_from_server_data(
            raw_config=raw_config, instance=instance
        )
        backend = IBMBackend(
            configuration=config,
            service=self,
            api_client=self._api_client,
            instance=instance,
        )
        return backend

    def _run(
        self,
        program_id: str,
        inputs: Dict,
        options: Optional[Union[RuntimeOptions, Dict]] = None,
        callback: Optional[Callable] = None,
        result_decoder: Optional[
            Union[Type[ResultDecoder], Sequence[Type[ResultDecoder]]]
        ] = None,
        session_id: Optional[str] = None,
        start_session: Optional[bool] = False,
    ) -> StrangeworksRuntimeJob:
        """Execute the runtime program.

        Args:
            program_id: Program ID.
            inputs: Program input parameters. These input values are passed
                to the runtime program.
            options: Runtime options that control the execution environment.
                See :class:`RuntimeOptions` for all available options.

            callback: Callback function to be invoked for any interim results and final
            result.
                The callback function will receive 2 positional parameters:

                    1. Job ID
                    2. Job result.

            result_decoder: A :class:`ResultDecoder` subclass used to decode job
            results.
                If more than one decoder is specified, the first is used for interim
                results and
                the second final results. If not specified, a program-specific decoder
                or the default
                ``ResultDecoder`` is used.
            session_id: Job ID of the first job in a runtime session.
            start_session: Set to True to explicitly start a runtime session. Defaults
            to False.

        Returns:
            A ``StrangeworksJob`` instance representing the execution.

        Raises:
            IBMInputValueError: If input is invalid.
            RuntimeProgramNotFound: If the program cannot be found.
            IBMRuntimeError: An error occurred running the program.
        """

        qrt_options: RuntimeOptions = options
        if options is None:
            qrt_options = RuntimeOptions()
        elif isinstance(options, Dict):
            qrt_options = RuntimeOptions(**options)

        qrt_options.validate(channel=self.channel)

        try:
            response = self._api_client.program_run(
                program_id=program_id,
                backend_name=qrt_options.backend,
                params=inputs,
                image=qrt_options.image,
                log_level=qrt_options.log_level,
                session_id=session_id,
                job_tags=qrt_options.job_tags,
                max_execution_time=qrt_options.max_execution_time,
                start_session=start_session,
                session_time=qrt_options.session_time,
                channel_strategy=(
                    None
                    if self._channel_strategy == "default"
                    else self._channel_strategy
                ),
            )
        except RequestsApiError as ex:
            if ex.status_code == 404:
                raise RuntimeProgramNotFound(
                    f"Program not found: {ex.message}"
                ) from None
            raise IBMRuntimeError(f"Failed to run program: {ex}") from None

        sw_job = StrangeworksRuntimeJob(
            job_slug=response["slug"],
            backend=response["jobData"]["job"]["backend"],
            service=self,
        )

        return sw_job

    def job(self, job_id: str) -> StrangeworksRuntimeJob:
        """Retrieve a runtime job.

        Args:
            job_id: Job ID.

        Returns:
            Runtime job retrieved.

        Raises:
            RuntimeJobNotFound: If the job doesn't exist.
            IBMRuntimeError: If the request failed.
        """
        response = self._api_client.job_get(job_id)
        return response

    def jobs(
        self,
    ) -> List[StrangeworksRuntimeJob]:
        """Retrieve all runtime jobs, subject to optional filtering for the product"""
        response = self._api_client.jobs_get()
        return response
