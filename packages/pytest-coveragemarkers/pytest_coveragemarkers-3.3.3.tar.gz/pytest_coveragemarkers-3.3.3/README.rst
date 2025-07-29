======================
pytest-coveragemarkers
======================

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Using pytest markers to track functional coverage and filtering of tests

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Definition of CoverageMarkers© in YAML format
* Support for applying CoverageMarkers© to tests
* Filtering of tests based on CoverageMarkers©
* Inclusion of CoverageMarkers© in JSON report


Installation
------------

You can install "pytest-coveragemarkers" from `PyPI`_::

    $ pip install pytest-coveragemarkers
    # or
    $ poetry add pytest-coveragemarkers

Usage
-----

Step 1: Define your coverage markers yaml.

    Using the format:

.. code-block:: yaml

  markers:
    - name: <marker_name>
      allowed:
        - <marker_value_1>
        - <marker_value_2>
    - name: <marker2_name>
      allowed:
        - <marker2_value_1>
        - <marker2_value_2>

Then decorate your tests with them


.. code-block:: python

    import pytest

    @pytest.mark.marker_name(['value1', 'value2'])
    @pytest.mark.marker2_name(['value1', 'value2'])
    def test_x():
        ...

    @pytest.mark.marker2_name(['value1', 'value2'])
    def test_y():
        ...


Then when the tests are executed with

.. code-block:: shell

    pytest --json-report --markers-location=/full/path/to/coverage_markers.yml

Then the JSON Test Report output from the test execution contains:

.. code-block:: json

    "tests": [
    {
      "nodeid": "...",
      "metadata": {
        "cov_markers": {
          "marker_name": {
            "value1": true,
            "value2": true
          },
          "marker2_name": {
            "value1": true,
            "value2": true
          }
        }
      }
    },
    ...
    ]

This can then be used to generate test coverage details based on the coverage markers.
A nice demo will be produced to give examples of usage.

But wait there is another benefit:

We can filter tests for execution based on their coverage markers

.. code-block:: shell

    pytest \
        --filter='"value1" in marker_name' \
        --json-report \
        --markers-location=/full/path/to/coverage_markers.yml

The above command run against the tests defined above would select 'test_x' and deselect 'test_y' for execution

Other examples of filters are:

.. code-block: shell

    '("value1" in marker_name) or ("value2" in marker_name)'

You can also supply the path to a file containing your filter.
Use argument --filter-location or key FilterLocation in the pytest.ini file.

Mandatory Coverage Markers
--------------------------

Coverage markers can be detailed as mandatory by including the mandatory attribute.

E.g.

.. code-block:: yaml

  markers:
    - name: <marker_name>
      mandatory: True
      allowed:
        - <marker_value_1>
        - <marker_value_2>

Dependent Coverage Markers
--------------------------

Coverage markers can be detailed as a dependency on another marker.
This ensures that if a marker is specified all dependencies of this
marker in the chain must also be specified.

E.g.

.. code-block:: yaml

  markers:
    - name: <marker_name>
      dependents:
        - <marker_name...>
        - <marker_name...>
      allowed:
        - <marker_value_1>
        - <marker_value_2>


Coverage Marker Argument Format
-------------------------------

The arguments supplied to Coverage Markers can follow multiple formats which allows the user to define the format that best suites them.

E.g.

.. code-block:: python

    import pytest

    @pytest.mark.marker_1('value1')                 # single string argument
    @pytest.mark.marker_2('value1', 'value2')       # multiple string arguments
    @pytest.mark.marker_3(['value1', 'value2'])     # list of arguments
    @pytest.mark.marker_4(('value1', 'value2'))     # tuple of arguments
    def test_x():
        ...



Testing
-------

Nox is used by this project to execute all tests.
To run a specific set of tests execute the below line::

    $ poetry run nox -s <session_name>

Where session_name can be one of the following

.. list-table:: Nox Sessions
   :widths: 25 75
   :header-rows: 1

   * - Session Name
     - Session Details
   * - unit_tests
     - Execute all tests marked as unit
   * - functional_tests
     - Execute all tests marked as functional

Thought Process
---------------

* The `pytest_docs`_ talks about using markers to set metadata on tests and use the markers to select required tests for execution.
* For the markers I want to add, I also want to specify a list of values that go along with that marker.
  E.g. If the marker was 'colour' then supported values may be 'Red', 'Green', 'Gold'.
* I also want the list of values validated against supported values so no unsupported values can be added.
  E.g. If the marker was 'colour' then a value of 'Panda' would not be allowed.
* Then all this meta data I want to come out in the junit json report.
* Next I want to use these markers and their supported values to filter tests. For this I need a more powerful filter engine.

Documentation
-------------

To build the docs run::

    poetry run mkdocs serve


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-coveragemarkers" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Future Changes
--------------

* Type-Hints
* Full Test Coverage
* Full Documentation


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/Gleams99/pytest-coveragemarkers/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`nox`: https://nox.thea.codes/en/stable/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest_docs`: https://docs.pytest.org/en/7.1.x/how-to/mark.html?highlight=slow
