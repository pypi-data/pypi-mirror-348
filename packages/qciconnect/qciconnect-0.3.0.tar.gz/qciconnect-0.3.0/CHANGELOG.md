## 0.3.0 (2025-05-15)

### changed (3 changes)

- [Release 0.3.0](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/4e308048e2f2c61fb454c85c6feeeb6cda7f7199) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/68))
- [Rename hequate -> qciconnect](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/7bc555074613d9b5c7bf12a1293972fe83e11ee9) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/62))
- [Return a "future" instead of the job id when submitting jobs non-blocking.](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/00f473ec6d411143a1cd57e2df48c8f4edc88b1e) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/51))

### fixed (3 changes)

- [Fixed missing dependencies and versioning in ci pipeline](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/c226ffaf47ad559913d6e3117520740fd7ce5c72) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/67))
- [Fixed version numbers](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/2f9a70996dc1fdee06e8ae524fb6104b4cae316c) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/58))
- [Fixed auto-completion in jupyter notebooks for nested classes](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/e506830adea614c3a95d0dcb5ccf4d7980b60f80) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/66))

### added (3 changes)

- [Added further code for error handling when accessing qpus.](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/9aee40ae48c2ca49b4a80e36cbb714921f968451) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/61))
- [Added handling of errors that can occur during initialization of QciConnectClient.](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/7ec3ac526ec7b9c278e0631021c15f5ef962b921) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/63))
- [Added Further e2e tests (against the platform)](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/41b052932b4b46a7402d2a81574976d0fa3aab22)

### improved (1 change)

- [Improved error handling so that more meaningful messages are shown to the user](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/commit/b90b19a0c57591cc0caf47c12350ff7f3803d627) ([merge request](https://gitlab.dlr.de/qci-connect/partners/all/qciconnect-sdk/-/merge_requests/65))

## 0.2.0 (2025-04-01)

### added (12 changes)

- [Keycloak support implemented](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/e1ef46b0a5b2783752449abff6dff5ce33e030ec) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/45))
- [Added "example_remote.ipynb" to test suite so that functionality of the...](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/29d03b29b0e1c6037174d0474228296e5c55980f) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/44))
- [Added release automation](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/b1d7935a6e892e584cc2f33f9827174b690365fa)
- [Added changelog-creation automation](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/de48315a9aeb4bd5d171fbd62ece1848d2736b12) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/38))
- [Added test coverage calculation to the ci](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/7bb7c791)
- [Implemented Non-blocking calls](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/37368a3a)
- [Added unit tests for qpu communication](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/98fabd66)
- [CI: Added build stage. Use this built for the testing](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/755bf1ab)
- [CI: Added unit tests for hequate client](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/134b1dfd)
- [CI: Re-enabled end to end tests](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/854d6bb8)
- [CI: Added end-to-end client tests](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/6e617974)
- [Added pydantic magic to validate and dump json](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/539f81b2)

### changed (5 changes)

- [Improved release process](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/c7bfe1f33bbd649154f5fa4cb5e95c7703308a0d) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/40))
- [Update README.md and minor fixes](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/4ef9d20d5c69b7e74a4c47eef80290c20bd75482) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/30))
- [Aligned compiler integration with the QCi connect platform](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/d5f64a4225ae1e88962b56e86ad36e0137102a2d) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/35))
- [Update QSP compiler image](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/a9b179a8d1ab12eb06a653491790804388ed963b) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/36))
- [Replaced manual rendering of QPU.show() by tabulate lib. Made parameters...](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/94bd834f82d690f74b3799bc3a1932f54ddfc2d0) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/33))

### fixed (7 change)

- [Check for succesful connection during instantiation](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/214ed08cc19fe676c776cd44fd53c5b4fd295986) ([merge request](https://gitlab.dlr.de/qc/compilation/hequate/-/merge_requests/43))
- [Increased timeout for blocking interaction with QCI Connect](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/d7d04607)
- [Enabled use of mini-orchestrator while in VPN](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/3275303d)
- [Added pyproject.toml for packaging of hequate lib/client](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/e440388d)
- [Resolved "Improve auto-completion](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/fcbc4f3f)
- [Removed deprecated files](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/c1fd7877)
- [Fixed #251: document client side source code](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/93b65a8c)


## 0.1.0 (2025-01-21)

### added (7 changes)

- [Added a proof of concept for compiler container/image handling of the mini orchestrator](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/dd7d2a6c71ddf657bc96eb48cea009dd133eca0d)
- [Added basic client side QPU handling](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/49f84a6963116545344c49c50e2ea95b49ed2c7a)
- [Added usage examples, see hequate/examples folder](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/25cda8cf1372904fd9d108c85ca67b3c0c01f4e4)
- [Added a first compiler pass](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/99511c3ff3c175b3e58112078a5aa7e1d6f71b51)
- [Added API client capabilities](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/32a30b1fdc6709cb8373af659cab08888ccdc88a)
- [Added an orchestrator](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/b75d51ab2b8e7787458d3e820b676afbdcf11fbd)
- [Added a docker compose setup](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/b240681c2ae1258152aee15ea0210973acca0315)

### changed (2 changes)

- [Updated the orchestrator](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/54f8d04f7f5f9f7d9b1bee5189777c6589ba27e5)
- [Updated docker compose setup](https://gitlab.dlr.de/qc/compilation/hequate/-/commit/adf91059870dd46f20564dbc2891717950dee2c4)
