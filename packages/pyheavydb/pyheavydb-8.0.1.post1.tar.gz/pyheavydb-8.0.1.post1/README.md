![PyPI](https://img.shields.io/pypi/v/pyheavydb?style=for-the-badge)

## pyheavydb

A python [DB API](https://www.python.org/dev/peps/pep-0249/) compliant
interface for [HeavyDB](https://www.heavy.ai/) (formerly OmniSci and MapD).

### Building from source

1. Requires Python >= 3.10
2. Clone the repository and navigate to the project directory.
3. The build rquires the thrift executable. See [thrift](https://thrift.apache.org) installed.  Make sure the directory containing the thrift binary is on your PATH.
Note - It's recommened to install a virtual python environment.  In these instuction pip is used,
4. python3 -m venv venv
5. . ./venv/bin/activate
Install the python build tools
6. pip install build
Run the build target for the makefile. This will also call the makefile's
thrift target.
7. make build

### Running the tests.

The test require a running HeavyAI backend database to connect to.

These instruction assume that the database backend is running on the same host
as the tests, that it has opened the default ports and that those ports are
accessible, as in not blocked by the local firewall.

Start the backend HeavyDB server.

Similary to building 'pyheavydb' it is recommended to install and test from
a virtual python environment.
These instruction need to be run from the project directory.

1. Build (see above) and install pyheavydb.
2. pip install pytest pytest-mock
3. pytest test/test_cursor.py
4. pytest test/test_connection.py
5. pytest test/test_integration.py
6. pytest test/test_results_set.py

### Release
Update the version numbers appropriately and run and `make publish` 
Releasing on PyPi assume you have a PyPi token in your environment.

