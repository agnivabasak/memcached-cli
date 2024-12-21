# memcached-cli
A cli tool to access your memcached server

## Steps to build a source distribution:

- In the root directory, run the command
   `python3 setup.py sdist`

## Steps to run the code locally:

- Make sure you have virtualenv/venv installed in your host python
- In the root directory, run the command:
  `python3 -m venv env` (This will create a env folder in the root directory)
- To activate the virtual environment, run the command:
  `source env/bin/activate`
- Run
  `pip install -r requirements.txt` to install the dependencies inside your virtual environment
- Run
  `pip install .` to install the memclid cli tool and use
  `memclid --help` to get started
- Run
  `deactivate` to exit the virtual environment

## Steps to run unit tests of the code:

- Activate a new virtual env for tests called test_env using the same steps described above
- Run
  `cd tests` to switch to the tests directory
- Run
  `pip install -r requirements.test.txt` to install the test dependencies
- Run
  `python3 -m coverage run -m unittest discover -b` to run the tests(with coverage) 
- To get the coverage report run: `python3 -m coverage report`
- To get it in HTML format and interactive format run: `python3 -m coverage html` (This will generate the html reports in tests/coverage_report, the main one is index.html)
- Run `deactivate` to exit the virtual environment

## Features Table

| Feature | Description |
| ------------ | ------------ |
| Add | Add the value corresponding to a new key in memcached server |
| Append | Append the value to the value corresponding to an existing key stored in memcached server
| CAS | Set the value corresponding to an existing key stored in memcached server using cas_unique
| Decr | Decrement the value corresponding to an existing key stored in memcached server by the value specified by the user
| Delete | Deletes the key-value stored in memcached server
| Get | Get the value corresponding to a key stored in memcached server
| Gets | Get the cas unique value for the entry and the value corresponding to a key stored in memcached server
| Incr | Increment the value corresponding to an existing key stored in memcached server by the value specified by the user
| Prepend | Prepend the value to the value corresponding to an existing key stored in memcached server
| Replace | Replace the value corresponding to an existing key stored in memcached server
| Set | Set the value corresponding to a key stored in memcached server

To know more about the commands use `memclid --help` after installing it

To know about the commands in memcached refer to its [`Protocol Documentation`](https://github.com/memcached/memcached/blob/master/doc/protocol.txt)

## Issues or bugs in the tool? Want to add a new functionality?
Contributions are always welcome. You could open up an issue if you feel like something is wrong with the CLI tool or a PR if you just want to improve it.
