from typing import Callable, Dict, Optional, Type, Union

from qiskit.providers.backend import BackendV1, BackendV2
from qiskit_ibm_runtime import Session
from qiskit_ibm_runtime.runtime_job_v2 import RuntimeJobV2
from qiskit_ibm_runtime.session import _active_session
from qiskit_ibm_runtime.utils.result_decoder import ResultDecoder

from strangeworks_qiskit_runtime import StrangeworksQiskitRuntimeService


class StrangeworksSession(Session):
    """Class for interacting with the Qiskit Runtime service.

    Qiskit Runtime is a new architecture offered by IBM Quantum that
    streamlines computations requiring many iterations. These experiments will
    execute significantly faster within its improved hybrid quantum/classical
    process.
    """

    def __init__(
        self,
        service: Optional[StrangeworksQiskitRuntimeService] = None,
        backend: Optional[Union[str, BackendV1, BackendV2]] = None,
        max_time: Optional[Union[int, str]] = 1440,  # seconds
    ):

        super().__init__(service, backend, max_time)

        if not self._backend.configuration().simulator:
            session = self._service._api_client.create_session(
                self.backend(),
                self._instance,
                self._max_time,
                self._service.channel,
                "dedicated",
            )
            self._session_id = session.get("id")

    @_active_session
    def run(
        self,
        program_id: str,
        inputs: Dict,
        options: Optional[Dict] = None,
        callback: Optional[Callable] = None,
        result_decoder: Optional[Type[ResultDecoder]] = None,
    ) -> RuntimeJobV2:
        """Run a program in the session.

        Args:
            program_id: Program ID.
            inputs: Program input parameters. These input values are passed
                to the runtime program.
            options: Runtime options that control the execution environment.
            callback: Callback function to be invoked for any interim results and final result.  # noqa

        Returns:
            Submitted job.
        """
        options = options or {}

        if "instance" not in options:
            options["instance"] = self._instance

        options["backend"] = self._backend

        job = self._service._run(  # type: ignore[call-arg]
            program_id=program_id,  # type: ignore[arg-type]
            options=options,
            inputs=inputs,
            session_id=self._session_id,
            callback=callback,
            result_decoder=result_decoder,
        )

        return job

    def close(self) -> None:
        """Close the session so new jobs will no longer be accepted, but existing
        queued or running jobs will run to completion. The session will be terminated once there  # noqa
        are no more pending jobs."""
        self._active = False
        if self._session_id:
            self._service._api_client.close_session(self._session_id)
