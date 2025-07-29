from inspect import get_annotations, stack
from .client import CompilerJob
from .result_handling import CompilerResult, FutureCompilerResult
from .client import QciConnectClient
from .exceptions import *


class Methods:
    """
    Provides a method/callable object for each compiler pass available on the platform.
    """
    def __init__(self, compiler_list: list, client: QciConnectClient):
        """
        Constructs a Methods object containing all Method objects (one per compiler pass) that are supported by the platform.

        Args:
            compiler_list: list of CompilerTable objects.
            client: Instance of QciConnectClient - QCI Connect RestAPI client.
        """
        self._passes = {}
        for compiler in compiler_list:
            for pass_name in compiler["passes_available"]:
                try:
                    method = Method(pass_name, compiler["compiler_id"], compiler["name"], client)
                except InvalidIdentifierException as e:
                    print(e)
                full_pass_name = f"{method.pass_alias}_{method._compiler_alias}"

                if full_pass_name in self._passes:
                    raise InvalidIdentifierException(
                        f"Compiler pass {full_pass_name} already exists."
                    )

                self._passes[full_pass_name] = method

    def __getattr__(self, name) -> str:
        return self._passes.__getitem__(name)

    def __dir__(self):
        extended_key_list = list(self._passes.keys())+super().__dir__()
        return extended_key_list

    def show(self):
        """Lists available compiler passes."""
        for method in self._passes.values():
            print(method)


class Method:
    """Callable object representing a compiler pass."""
    def __init__(self, pass_name: str, compiler_id: int, compiler_name: str, client: QciConnectClient):
        """
        Constructs a callable Method object, which submits a job to respective compile pass.

        Args:
            pass_name: Name of the compiler pass.
            compiler_id: ID of the compiler the compiler pass belongs to.
            compiler_name: Name of the compiler.
            client: Instance of QciConnectClient - QCI Connect RestAPI client.
        """

        self._pass_name = pass_name
        self._compiler_id = compiler_id
        self._compiler_name = compiler_name
        self._compiler_alias = compiler_name.lower().replace(' ', '_').replace('-','_')
        if not self._compiler_alias.isidentifier():
            raise InvalidIdentifierException(
                f"Compiler alias {self._compiler_alias} is not a valid python identifier."
            )
        self._client = client

    def __call__(self, input_circuits: dict, options: dict = {}, wait_for_results: bool = True) -> CompilerResult | FutureCompilerResult:
        """
        Submits input circuits to respective compile pass.

        Args:
            input_circuits: dict of input circuits.
            options: Options determining how to compile.
            wait_for_results: Wait for the computation and return result. Otherwise, return only job ID.

        Returns: If wait_for_results == True, it returns the compilation Result, which is the compiled circuits together with a bunch of meta data. Otherwise, it returns FutureCompilerResult, which promises to return the compilation result when its available.
        """
        arguments = locals()
        annotations = get_annotations(self.__call__)
        for name, value in arguments.items():
            if name == "self":
                continue
            if not isinstance(value, annotations[name]):
                print(f"Invalid type for parameter {name}. Expected {annotations[name]} got {type(value)}")
                return None
        for name, circuit in input_circuits.items():
            if not isinstance(circuit, str):
                print(f"Circuits must be given as OpenQASM strings, but got {type(circuit)} for {name}.")
                return None

        compiler_job = CompilerJob(self._compiler_id, self._pass_name, options, input_circuits)
        try:
            if wait_for_results:
                result = self._client.submit_compiler_job_and_wait(compiler_job)
                return CompilerResult.from_compiler_task_result(result.last_compiler_result)
            else:
                job_id = self._client.submit_compiler_job(compiler_job)
                return FutureCompilerResult(job_id, self._client)
        except (QciConnectClientException, KeycloakTokenManagerException) as e:
            print(e)
            return None
        except Exception as e:
            raise e

    def __str__(self) -> str:
        return f"{self.pass_alias}_{self._compiler_alias}"

    @property
    def pass_alias(self):
        """Returns method/compiler pass alias."""
        return self._pass_name.lower().replace(' ', '_').replace('-','_')
