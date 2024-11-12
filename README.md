# memcached-cli
A cli tool to access your memcached server

To build a source distribution:

-Run the command: python3 setup.py sdist

To run the code locally:

-Make sure you have virtualenv/venv installed in your host python
-Run command: python3 -m venv env (This will create a env folder in the root directory)
-To activate the virtual environment, run the command: source env/bin/activate
-Run pip install -r requirements.txt to install the dependencies inside your virtual environment
-Run pip install . to install the memclid cli tool and use memclid --help to get started
-Run python3 setup.py sdist to create a source distribution (output in the dist folder)

To run unit tests of the code:

-Activate the virtual env like described above
-Move to the tests directory: cd tests
-Install the test dependencies:  pip install -r requirements.test.txt
-Run the tests(with coverage): python3 -m coverage run -m unittest test_svc_memclid -b
-To get the coverage report run: python3 -m coverage report
-To get it in html and interactive format run: python3 -m coverage html (This will generate the html reports in tests/coverage_report, the main one is index.html)