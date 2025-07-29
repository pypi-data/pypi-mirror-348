import httpx
import time
import json

from commons.hequate_common.models import (
    CompilerTaskBase,
    QPUTaskBase,
    JobSubmission,
    JobResult)

from .token_managers import KeycloakTokenManager, DummyTokenManager
from .exceptions import QciConnectClientException

class CompilerJob:
    """Class used to hand over the compile jobs to QciConnectClient."""
    def __init__(self, compiler_id: int, compilation_pass: str, options: dict, circuits: dict):
        self.task = CompilerTaskBase(
                compiler_id = compiler_id, 
                compilation_pass = compilation_pass, 
                options = options)
        self.circuits = circuits

class BackendJob:
    """Class used to hand over the qpu jobs to QciConnectClient."""
    def __init__(self, backend_id: int, circuit: str, primitive: str, name = "Hequate Client Job", comment="Issued via API", shots=10000):
        self.name = name
        self.comment = comment
        self.circuit = circuit
        self.task = QPUTaskBase(
            qpu_id = backend_id,
            total_shots = shots,
            primitive = primitive,
            qpu_options={"coupling_map": None,
                         "basis_gates": None}
)


JOB_SUBMIT_ENDPOINT = "/api/job/submit"
JOB_RESULT_ENDPOINT = "/api/result/"
COMPILER_LIST_ENDPOINT = "/api/compiler/all"
QPU_LIST_ENDPOINT = "/api/qpu/all"


class QciConnectClient:
    """
    Client for QCI Connect frontend RestAPI.
    Handles http get/put/post requests to retrieve available compilers/QPUs
    and to submit jobs to these resources.

    Attributes:
        _server_address: Address of the platform.
        _token: Authorization token.
    """
    def __init__(self, server_address: str, username: str, password: str):
        """
        Constructs QciConnectClient object.

        Args:
            server_address: Address of the platform.
            username: username for authentication.
            password: password for authentication.
        """
        self._username = username
        self._password = password
        self.server_address = server_address # setting this also creates a KeycloakTokenManager object

    @property
    def server_address(self) -> str:
        """Returns the current server address."""
        return self._server_address

    @server_address.setter
    def server_address(self, value: str):
        """
        Sets the server address.

        Args:
            value: Server address.
        """
        value = value.rstrip('/')
        self._server_address = value
        if self._username is None and self._password is None:
            self._keycloak_token_manager = DummyTokenManager()
        else:
            self._keycloak_token_manager = KeycloakTokenManager(self.server_address, self._username, self._password)

    def _handle_http_status_error(self, errh):
        """
        Handles HTTP errors.
        Args:
            errh: HTTP error to be handled.
        """
        error_dict = json.loads(errh.response.text)
        if errh.response.status_code == 301:
            # Handle the 301 status code
            raise QciConnectClientException(f"Received a 301 status code. The requested resource has been permanently moved: \"{error_dict['detail']}\"")
        elif errh.response.status_code == 401:
            # Handle the 401 status code
            raise QciConnectClientException(f"Received a 401 status code. The request was unauthorized: \"{error_dict['detail']}\"")
        elif errh.response.status_code == 403:
            # Handle the 403 status code
            raise QciConnectClientException(f"Received a 403 status code. The request was forbidden: \"{error_dict['detail']}\"")
        else:
            # Handle other HTTP errors - print information about the error in a nicely formatted way
            error_dict_str = json.dumps(error_dict, indent=2)
            raise QciConnectClientException(f"HTTP Error occurred: {errh.response.status_code}\n\nDictionary with error message:\n{error_dict_str}")

    def _post(self, request: dict) -> str:
        """
        Sends a post request to the platform and returns the respective job ID.

        Args:
            request: JSON request in form of a dict.

        Returns: job ID.
        """
        headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive"
        }
        headers = self._keycloak_token_manager.add_auth_header(headers)

        with httpx.Client(follow_redirects=False, verify=True) as client:
            try:
                post_response = client.post(f"{self._server_address}{JOB_SUBMIT_ENDPOINT}", json=request, headers=headers)
                post_response.raise_for_status()
                job_id = post_response.json()
                print(f"Job submitted with ID: {job_id}")
                return job_id
            except httpx.RequestError as e:
                raise QciConnectClientException(f"A RequestError occurred while sending a post-request to URL: {e.request.url} - {e}")
            except httpx.HTTPStatusError as e:
                self._handle_http_status_error(e)

    def _job_id_to_result_endpoint(self, job_id: str) -> str:
        """
        Converts a job ID to the respective result endpoint.

        Args:
            job_id: Job ID to be converted.

        Returns: URL to the respective result endpoint.
        """
        return f"{self._server_address}{JOB_RESULT_ENDPOINT}{job_id}"

    def _get(self, get_url: str) -> dict:
        """
        Sends a get request for a given URL.

        Args:
            get_url: URL to which a get request is sent.

        Returns: JSON response in form of a dict.
        """
        headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive"
        }
        headers = self._keycloak_token_manager.add_auth_header(headers)

        with httpx.Client(follow_redirects=False, verify=True) as client:
            try:
                get_response = client.get(get_url, headers=headers)
                get_response.raise_for_status()
                payload = get_response.json()
                return payload
            except httpx.HTTPStatusError as errh:
                self._handle_http_status_error(errh)
            except httpx.RequestError as e:
                raise QciConnectClientException(f"A RequestError occurred while sending a get-request to URL: {e.request.url} - {e}.")
            except Exception as e:
                # Handle other exceptions
                raise QciConnectClientException(f"An error occurred: {e}")

    def _handle_http_status_error(self, errh: httpx.HTTPStatusError):
        def parse_validation_error_detail(error_detail: dict) -> str:
            # intentionally looking at the first error only for now
            error = error_detail[0]
            try:
                if error["loc"][-2] == "options":
                    if error["type"] == "extra_forbidden":
                        return f"{error['loc'][-1]} is not a valid option"
                    else:
                        return f"value for {error['loc'][-1]} has wrong type or is out of bounds."
                else:
                    return error
            except:
                return error

        error_dict = json.loads(error_text)
        error_detail = error_dict["detail"]
        error_message_table = {
            301: f'Received a 301 status code. The requested resource has been permanently moved: "{error_detail}"',
            401: f'Received a 401 status code. The request was unauthenticated: "{error_detail}"',
            403: f'Received a 403 status code. The request was unauthorized: "{error_detail}"',
            422: f'Received a 422 status code. The request was invalid: "{parse_validation_error_detail(error_detail)}"'
        }

        try:
            error_message = error_message_table[errh.response.status_code] + f'"{parse_error(errh.response.text)}"'
        except:
            raise QciConnectClientException(f"HTTP Error occurred: {errh}")
        raise QciConnectClientException(error_message)

    def _sanitize_circuit(self, circuit: str) -> str:
        """
        Sanitizes the circuit.

        Args:
            circuit: Circuit to be sanitized.

        Returns: Sanitized circuit.
        """
        if type(circuit) != str:
            raise QciConnectClientException("Circuit must be a string.")
        
        circuit = circuit.replace('OPENQASM 2.0;', '')
        circuit = circuit.replace('include "qelib1.inc";', 'include "stdgates.inc";')

        return circuit

    def submit_compiler_job(self, compiler_job: CompilerJob):
        """
        Submits a compiler job.

        Args:
            compiler_job: Quantum circuit(s) and information about the compiler pass to be used.

        Returns: id identifying the job just submitted.
        """
        circuit = list(compiler_job.circuits.values())[0]
        circuit = self._sanitize_circuit(circuit)

        request = JobSubmission(
                circuit = circuit,
                name = "Hequate Client Compile Job",
                comment = "Issued via API",
                tasks = [compiler_job.task])

        job_id = self._post(request.model_dump())
        return job_id

    def _has_job_finished(self, response: dict) -> bool:
        """
        Interprets the status message.

        Args:
            status_message: Status message to be interpreted.
        """
        if response["status"] == "SUCCESS":
            print("Job was successful.")
            return True
        elif response["status"] == "FAILURE":
            try:
                print(f"{response['status_message']}")
            except:
                print("Job failed.")
            return True
        else:
            print("Job is not finished yet.")
            return False

    def get_job_status(self, job_id: str) -> str:
        """
        Gets the status of a job.

        Args:
            job_id: id of job which status shall be returned.

        Returns: string telling the status of the job.
        """
        endpoint_url = self._job_id_to_result_endpoint(job_id)
        response = self._get(endpoint_url)
        return response["status"]

    def retrieve_result(self, job_id: str) -> JobResult:
        """
        Retrieves the result of a job.
        """
        endpoint_url = self._job_id_to_result_endpoint(job_id)
        response = self._get(endpoint_url)
        if self._has_job_finished(response):
            result = JobResult.model_validate(response)
            return result
        else:
            return None

    def wait_and_call_method(self, timeout, method, *params):
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = method(*params)
            if result is not None:
                return result
            time.sleep(5)
        raise QciConnectClientException("Timeout occured while waiting for job result.")

    def submit_compiler_job_and_wait(self, compiler_job: CompilerJob, timeout=3600) -> JobResult:
        """
        Submits a compiler job and waits for the result.

        Args:
            compiler_job: Quantum circuit(s) and information about the compiler pass to be used.
            timeout: Timeout in seconds.

        Returns: JobResult which is compiled quantum circuit(s) and a bunch of meta information.
        """
        job_id = self.submit_compiler_job(compiler_job)
        result = self.wait_and_call_method(30, self.retrieve_result, job_id)
        return result

    def submit_backend_job(self, backend_job: BackendJob) -> str:
        """
        Submits a quantum circuit processing job.

        Args:
            backend_job: Quantum circuit and information about the QPU it should run on (and how).

        Returns: id identifying the job just submitted.
        """
        circuit = self._sanitize_circuit(backend_job.circuit)


        request = JobSubmission(
            circuit = circuit,
            primitive = backend_job.task.primitive,
            name = backend_job.name,
            comment = backend_job.comment,
            tasks = [backend_job.task])

        job_id = self._post(request.model_dump())
        return job_id

    def submit_backend_job_and_wait(self, backend_job: BackendJob, timeout=3600) -> JobResult:
        """
        Submits a quantum circuit processing job and waits for the result.

        Args:
            backend_job: Quantum circuit and information about the QPU it should run on (and how).
            timeout: Timeout in seconds.

        Returns: JobResult which is measurement data and a bunch of meta information.
        """
        job_id = self.submit_backend_job(backend_job)
        result = self.wait_and_call_method(30, self.retrieve_result, job_id)
        return result

    def get_available_compilers(self) -> list:
        """Retrieves list of compilers available on the platform."""
        endpoint_url = f"{self._server_address}{COMPILER_LIST_ENDPOINT}"
        return self._get(endpoint_url)

    def get_available_qpus(self) -> list:
        """Retrieves list of QPUs available on the platform."""
        endpoint_url = f"{self._server_address}{QPU_LIST_ENDPOINT}"
        return self._get(endpoint_url)
