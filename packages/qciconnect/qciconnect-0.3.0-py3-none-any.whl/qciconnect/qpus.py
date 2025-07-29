from tabulate import tabulate

from pydantic import ValidationError as PydanticValidationError
from qciconnect.exceptions import QciConnectClientException
from .client import BackendJob
from .client import QciConnectClient
from .result_handling import BackendResult, FutureBackendResult

class Qpu:
    """Class representing a quantum circuit processing unit; might be a real device or a simulator."""
    def __init__(self, identifier: str, name: str, manufacturer: str, qubit_count: int, status: str, client: QciConnectClient):
        """
        Constructs a Qpu object.

        Args:
            identifier: Unique identifier of the quantum circuit processing unit.
            name: Name of the quantum circuit processing unit.
            manufacturer: Manufacturer of the quantum circuit processing unit.
            qubit_count: Number of qubits available on the QPU.
            status: Current operational status.
            client: Instance of QciConnectClient - QCI Connect RestAPI client.
        """
        self._id = identifier
        self._name = name
        self._alias = name.lower().replace(' ', '_').replace('-','_')
        self._manufacturer = manufacturer
        self._qubit_count = qubit_count
        self._status = status
        self._client = client

    def submit(self, circuit: str, primitive: str, shots=10000, wait_for_results=True, name: str="Hequate QPU Job", comment: str="Issued via API") -> FutureBackendResult | BackendResult:
        """
        Submits the circuit to the QPU for execution according to primitive and shots.

        Args:
            name: Name of the job.
            circuit: Quantum circuit to be executed.
            primitive: Way of execution.
            shots: Number of runs/executions.
            wait_for_results: wait for the backend to finished the submitted job.

        Returns: BackendResult, which is measurement data with a bunch of meta data or
                 FutureBackendResult which is a promise to later return a BackendResult
        """
        try:
            job = BackendJob(self._id, circuit, primitive, name=name, shots=shots, comment=comment)
        except PydanticValidationError as e:
            print(e)
            return None
        
        if wait_for_results:
            try:
                result = self._client.submit_backend_job_and_wait(job)
            except (QciConnectClientException, PydanticValidationError) as e:
                print(e)
                return None
            return BackendResult.from_qpu_task_result(result.last_qpu_result)
        else:
            try:
                job_id = self._client.submit_backend_job(job)
            except (QciConnectClientException, PydanticValidationError) as e:
                print(e)
                return None
            return FutureBackendResult(job_id, self._client)

    def __str__(self) -> str:
        return f"Name: {self._alias}, #Qubits: {self._qubit_count}, Status: {self._status}"
    
    def get_qpu_info(self) -> list[str]:
        return [self._alias, self._qubit_count, self._status]

    def __dir__(self):
        method_list = []
        for attr in dir(self):
            if not attr.startswith("__"):
                method_list.append(attr)
        return method_list

class QpuByAlias:
    """
    Dictionary of available quantum circuit processing unit on the platform indexed by their aliases.
    """
    def __init__(self, qpu_list: list, client):
        """
        Constructs a dict of QPUs available on the platform (indexed by their aliases).

        Args:
            qpu_list: list of QPUTable objects.
            client: Instance of QciConnectClient - QCI Connect RestAPI client.
        """
        self._qpus = {}
        for qpu_entry in qpu_list:
            qpu = Qpu(qpu_entry["qpu_id"], qpu_entry["name"], qpu_entry["manufacturer"], qpu_entry["number_of_qubits_available"], qpu_entry["status"], client)
            self._qpus[qpu._alias] = qpu

    def __getattr__(self, name) -> str:
        try:
            return self._qpus.__getitem__(name)
        except Exception as e:
            print(e)


    def __dir__(self):
        extended_key_list = list(self._qpus.keys())+super().__dir__()
        return extended_key_list

    def show(self):
        """Prints table of available QPUs including their qubit counts and status."""
        
        all_qpu_info = []
        for qpu in self._qpus.values():
            all_qpu_info.append(qpu.get_qpu_info())

        print(tabulate(all_qpu_info, headers=["Alias", "Qubits", "Status"]))

