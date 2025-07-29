
from commons.qciconnect_common.qciconnect_conversion.json_conversion import JSONNumpyConverter, JSONDateTimeConverter

from commons.hequate_common.models import (
        CompilerTaskResult,
        QPUTaskResult)

from .client import QciConnectClient


class CompilerResult:
    """
    Result of a compile job.

    Attributes:
        _compiler_task_result: Result as it is returned by the platform parsed by pydantic.
        compiled_circuits: Workaround - we want to return the circuits as a list.
    """
    _compiler_task_result: CompilerTaskResult
    compiled_circuits: list

    def __getattr__(self, attribute):
        """
        Redirects getting of attributes to _compiler_task_result (except for compiled_circuits)
        and at the same time hides all the pydantic attributes from the user.

        Args:
            attribute: Name of attribute to get.

        Returns: attribute.
        """
        if attribute != "compiled_circuits":
            return getattr(self._compiler_task_result, attribute)
        else:
            return self.compiled_circuits

    def __dir__(self):
        """Fixes autocompletion and hides pydantic noise."""
        dir_output = list(self._compiler_task_result.model_fields_set)
        dir_output.append('compiled_circuits')
        dir_output.remove('compiled_circuit')
        return dir_output

    @classmethod
    def from_compiler_task_result(cls, result: CompilerTaskResult):
        """
        Creates CompilerResult from CompilerTaskResult.

        Args:
            result: compiler task result to create compiler result from.

        Returns: Compiler result
        """
        compiler_result = cls()
        compiler_result._compiler_task_result = result
        if isinstance(result.compiled_circuit, list):
            compiler_result.compiled_circuits = result.compiled_circuit
        else:
            compiler_result.compiled_circuits = [result.compiled_circuit]
        return compiler_result

class BackendResult:
    """
    Result of a qpu job.

    Attributes:
        _qpu_task_result: Result as it is returned by the platform parsed by pydantic.
    """
    _qpu_task_result: QPUTaskResult

    def __getattr__(self, attribute):
        """
        Redirects getting of attributes to _qpu_task_result and hides pydantic noise from the user.

        Args:
            attribute: Name of attribute to get.

        Returns: attribute.
        """
        return getattr(self._qpu_task_result, attribute)

    def __dir__(self):
        """Fixes autocompletion and hides pydantic noise."""
        return list(self._qpu_task_result.model_fields_set)

    @classmethod
    def from_qpu_task_result(cls, result: QPUTaskResult):
        """
        Creates BackendResult from QPUTaskResult.

        Args:
            result: QPU task result to create backend result from.

        Returns: backend result
        """
        backend_result = cls()
        backend_result._qpu_task_result = result
        backend_result._qpu_task_result.data = JSONNumpyConverter.json_list_to_nparray(backend_result._qpu_task_result.data)
        backend_result._qpu_task_result.end_date_time = JSONDateTimeConverter.json_datetime_to_datetime(backend_result._qpu_task_result.end_date_time)
        backend_result._qpu_task_result.start_date_time = JSONDateTimeConverter.json_datetime_to_datetime(backend_result._qpu_task_result.start_date_time)
        return backend_result

class FutureResult:
    """
    Object that can be used to poll/retrieve the result of an job.

    Attributes:
        status: status of the job.
        result: Result as it is returned by the platform parsed by pydantic.
    """
    def __init__(self, job_id: str, client: QciConnectClient):
        self._client = client
        self._job_id = job_id
        self._result = None
        self.update()

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def status(self) -> str:
        if not self._result:
            self.update()
        return self._status

    def update(self):
        """
        Updates status of the job and retrieves result if job has finished.
        """
        self._status = self._client.get_job_status(self._job_id)
        self._result = self._client.retrieve_result(self._job_id)

class FutureBackendResult(FutureResult):
    @property
    def result(self) -> BackendResult:
        """
        Updates future and returns BackendResult if ready.

        Returns: BackendResult object.
        """
        if not self._result:
            self.update()
        if self._result:
            return BackendResult.from_qpu_task_result(self._result.last_qpu_result)
        return None

class FutureCompilerResult(FutureResult):
    @property
    def result(self) -> CompilerResult:
        """
        Updates future and returns CompilerResult if ready.

        Returns: BackendResult object.
        """
        if not self._result:
            self.update()
        if self._result:
            return CompilerResult.from_compiler_task_result(self._result.last_compiler_result)
        return None


