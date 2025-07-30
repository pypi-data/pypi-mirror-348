Contribution Overview
=====================

OpenDev's tools are hosted within the OpenDev collaboratory, and
development for them uses workflows described in the OpenDev
Infrastructure Manual:

http://docs.opendev.org/opendev/manual/developers.html

Defect reporting and task tracking takes place here:

https://storyboard.openstack.org/#!/project/opendev/git-review

Developing git-review
=====================

Either install `bindep` and run ``bindep test`` to check you have the needed
tools, or review ``bindep.txt`` by hand.

Running Tests
-------------

The testing system is based on a combination of nox and testr. The canonical
approach to running tests is to simply run the command `nox`. This will
create virtual environments, populate them with dependencies and run all of
the tests that OpenStack CI systems run. Behind the scenes, nox is running
`stestr run`, but is set up such that you can supply any additional
stestr arguments that are needed to nox. For example, you can run:
`nox -s tests -- --analyze-isolation` to cause nox to tell testr to add
--analyze-isolation to its argument list.

It is also possible to run the tests inside of a virtual environment
you have created, or it is possible that you have all of the dependencies
installed locally already. If you'd like to go this route, the requirements
are listed in requirements.txt and the requirements for testing are in
test-requirements.txt. Installing them via pip, for instance, is simply::

  pip install -r requirements.txt -r test-requirements.txt

In you go this route, you can interact with the testr command directly.
Running `stestr run` will run the entire test suite.
More information about testr can be found at:
https://stestr.readthedocs.io/en/latest/README.html
