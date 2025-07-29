"""Strangeworks Runtime Client."""

import json
from datetime import datetime as python_datetime
from typing import Any, Dict, List, Optional

import strangeworks
from qiskit_ibm_runtime.api.clients.runtime import RuntimeClient
from qiskit_ibm_runtime.utils import RuntimeEncoder
from strangeworks.core.client.resource import Resource
from strangeworks.sw_client import SWClient as SDKClient


class StrangeworksRuntimeClient(RuntimeClient):
    # we need this for the following reasons:
    # 1. Use our own Runtime to direct requests to our product/service.
    # 2. Return errors for all functions that are related to programs such  as creation,
    #  deletion. Only list currently available programs.
    # 3. Override backend calls to retrieve backends from platform.
    def __init__(
        self,
        channel,
        rsc: Optional[Resource] = None,
        sdk_client: Optional[SDKClient] = None,
        **kwargs,
    ):
        self._channel = channel
        self.rsc = rsc
        self._sdk_client = sdk_client or strangeworks.client

        self._product_slug = "ibm-qiskit-runtime"
        self.properties = {}

    def program_run(
        self,
        program_id: str,
        backend_name: Optional[str],
        params: Dict,
        image: Optional[str],
        log_level: Optional[str],
        session_id: Optional[str],
        job_tags: Optional[List[str]] = None,
        max_execution_time: Optional[int] = None,
        start_session: Optional[bool] = False,
        session_time: Optional[int] = None,
        channel_strategy: Optional[str] = None,
    ) -> Dict:
        """Execute the program.

        Args:
            program_id: Program ID.
            backend_name: Name of the backend.
            params: Program parameters.
            image: Runtime image.
            hub: Hub to be used.
            group: Group to be used.
            project: Project to be used.
            log_level: Log level to use.
            session_id: ID of the first job in a runtime session.
            job_tags: Tags to be assigned to the job.
            max_execution_time: Maximum execution time in seconds.
            start_session: Set to True to explicitly start a runtime session.
            Defaults to False.
            session_time: Length of session in seconds.

        Returns:
            JSON response.
        """

        payload: Dict[str, Any] = {
            "program_id": program_id,
            "params": params,
        }
        if image:
            payload["runtime"] = image
        if log_level:
            payload["log_level"] = log_level
        if backend_name:
            payload["backend"] = backend_name.name
        if session_id:
            payload["session_id"] = session_id
        if job_tags:
            payload["tags"] = job_tags
        if max_execution_time:
            payload["cost"] = max_execution_time
        if start_session:
            payload["start_session"] = start_session
            payload["session_time"] = session_time
        if channel_strategy:
            payload["channel_strategy"] = channel_strategy
        data = json.dumps(payload, cls=RuntimeEncoder)

        payload = {
            "data": data,
            "program_id": program_id,
            "backend": backend_name.name,
            "channel": self._channel,
            "runtime": True,
        }

        response = strangeworks.execute(self.rsc, payload, "create_runtime_job")

        return response

    def job_get(self, job_slug, **kwargs):
        return strangeworks.jobs(slug=job_slug)[0]

    def jobs_get(self, **kwargs):
        return strangeworks.jobs(
            product_slugs=self._product_slug, resource_slugs=self.rsc.slug
        )

    def backend_properties(
        self, backend_name: str, datetime: Optional[python_datetime] = None
    ) -> Dict[str, Any]:
        """Return the properties of the IBM backend.

        Args:
            backend_name: The name of the IBM backend.
            datetime: Date and time for additional filtering of backend properties.

        Returns:
            Backend properties.

        Raises:
            NotImplementedError: If `datetime` is specified.
        """
        payload = {
            "backend_name": backend_name,
            "datetime": datetime,
        }
        if self.properties.get(backend_name, None) is None:
            self.properties[backend_name] = strangeworks.execute(
                self.rsc, payload, "runtime_backend_properties"
            )
        return self.properties[backend_name].copy()

    def backend_configuration(self, backend_name: str) -> Dict[str, Any]:
        """Return the configuration of the IBM backend.

        Args:
            backend_name: The name of the IBM backend.

        Returns:
            Backend configuration.
        """
        if backend_name not in self._configuration_registry:
            payload = {
                "backend_name": backend_name,
            }
            self._configuration_registry[backend_name] = strangeworks.execute(
                self.rsc, payload, "runtime_backend_config"
            )
        return self._configuration_registry[backend_name].copy()

    def backend_pulse_defaults(self, backend_name: str):
        """Return the pulse defaults of the IBM backend.

        Args:
            backend_name: The name of the IBM backend.

        Returns:
            Backend pulse defaults.
        """
        payload = {
            "backend_name": backend_name,
        }
        return strangeworks.execute(self.rsc, payload, "runtime_backend_pulse_defaults")

    def session_details(self, session_id: str) -> Dict[str, Any]:
        """Get session details.

        Args:
            session_id: Session ID.

        Returns:
            Session details.
        """
        payload = {
            "session_id": session_id,
        }
        return strangeworks.execute(self.rsc, payload, "session_details")

    def create_session(
        self,
        backend: Optional[str] = None,
        instance: Optional[str] = None,
        max_time: Optional[int] = None,
        channel: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Create the runtime session.

        Args:
            session_id: Session ID.
        """
        payload = {
            "backend": backend,
            "instance": instance,
            "max_time": max_time,
            "channel": channel,
            "mode": mode,
        }
        return strangeworks.execute(self.rsc, payload, "create_session")

    def close_session(self, session_id: str) -> None:
        """Close the runtime session.

        Args:
            session_id: Session ID.
        """
        payload = {
            "session_id": session_id,
        }
        strangeworks.execute(self.rsc, payload, "close_session")
