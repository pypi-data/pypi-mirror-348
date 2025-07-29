from .qpus import QpuByAlias
from .methods import Methods
from .client import QciConnectClient
from .exceptions import KeycloakTokenManagerException, QciConnectClientException


class Mageia:
    """
    Represents a frontend to a quantum computing platform.
    
    Attributes:
        methods: Collects and provides all the methods/compiler passes available on the platform.
        qpus: Collects and provides all the quantum processing units (including simulators) available on the platform.
        utils: Utilities not strictly associated to compilers or qpus may go here.
    """ 

    _DEFAULT_SERVER = "https://qc-plat-pro.dlr.de/"
    _LOCALHOST = "http://127.0.0.1:8000/"

    def __init__(self, username=None, password=None, server=None):
        """Constructs a Mageia/Client object."""
        if (username is None or password is None) and server is None:
            print(f"""Warning! No server and no credentials given.
In order to use the QCI Connect server {self._DEFAULT_SERVER} you need to provide username and password.
Falling back to {self._LOCALHOST} as server.""")
            server=self._LOCALHOST
        if username is not None and password is not None and server is None:
            server=self._DEFAULT_SERVER

        try:
            self._client = QciConnectClient(server, username, password)
            self._update_methods()
            self._update_qpus()
        except KeycloakTokenManagerException as e:
            print(e)
        except QciConnectClientException as e:
            print(e)
        except Exception as e:
            if(server.__contains__("localhost") or
                    server.__contains__("0.0.0.0") or
                    server.__contains__("127.0.0.1")):
                print("Please run `docker compose up` before connecting to your backend. \n"
                      "For further information see also https://gitlab.dlr.de/qc/compilation/hequate")
            else:
                print(f"Connection to {server} could not be established.")


    @classmethod
    def DEFAULT_SERVER(cls) -> str:
        """Returns the default platform URL, used when none is given."""
        return cls._DEFAULT_SERVER

    @property
    def server_address(self) -> str:
        """Returns URL of the platform."""
        return self._client.server_address

    @server_address.setter
    def server_address(self, value: str):
        """
        Sets the URL of the platform and retrieves available methods and QPUs.

        Args:
            value: URL of the platform that shall be used.
        """
        self._client.server_address = value
        self._update_methods()
        self._update_qpus()

    def _update_methods(self):
        """Updates the methods/compiler passes available on the platform."""
        compiler_list = self._client.get_available_compilers()
        self.methods = Methods(compiler_list, self._client)

    def _update_qpus(self):
        """Updates the quantum processing units available on the platform."""
        qpu_list = self._client.get_available_qpus()
        if not qpu_list:
            try:
                delattr(self, "qpus")
            except:
                pass
        else:
            self.qpus = QpuByAlias(qpu_list, self._client)

