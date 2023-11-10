# Testing

We think testing our code is no less crucial than the actual implementation of if, so we intend to dedicate as much
time and resources to writing and maintaining tests as we do to developing and maintaining our production code.

## Types of tests:

### Unit-tests

Unit-tests are probably the most important type of tests. Unit-tests are designed to assess the smallest units of
code—typically methods and functions—individually for correctness, reliability, and performance. These tests are
critical for several reasons:

- **Early Bug Detection**: Issues are identified at an early stage. Since unit tests are focused on a small piece of
  code,
  they make it easier to catch bugs during the development phase, long before integration testing.

- **Improved Design**: Writing tests often leads to better code design. To make code testable, it has to be modular.
  This
  modularity, in turn, leads to cleaner, more maintainable, and decoupled code structures.

- **Refactoring Confidence**: They provide a safety net. Developers can refactor code with the assurance that existing
  functionality hasn't been accidentally broken.

- **Documentation**: They serve as documentation. Good unit tests can help demonstrate how the code is intended to be
  used,
  as well as its expected behavior under various conditions.

- **Reduce Costs**: They help in reducing the cost of bugs in later stages. The more bugs you catch in the development
  phase, the less expensive (in time, money, and resources) those bugs are to fix.

- **Continuous Integration**: They are key for CI/CD practices. Unit tests can be automated and run every time the code
  is
  changed, ensuring that new changes do not break the system (regression) and that the right practices for continuous
  integration and deployment are in place.

### Integration tests

Integration tests play a critical role in ensuring that different pieces of a system work together correctly. Unlike
unit tests, which focus on the smallest parts of software, integration tests target interactions between different parts
of a system—be it different modules, services, or data interactions. These tests are pivotal for several reasons:

- **Verifying Interactions**: Integration tests confirm that different components of the system work in tandem. These
  interactions might involve network communication, data transfer, dependency handling, or the way separate modules use
  shared resources.

- **Identifying Interface Issues**: They help in catching problems that occur at the interfaces between components.
  Discrepancies in data formats, synchronization, or misuse of interfaces can be detected through these tests.

- **Simulating Real-World Use**: These tests often involve a setup closer to the actual application's operational
  settings. They help ensure that the system meets requirements under conditions that closely simulate live scenarios,
  providing confidence that it will behave as expected upon deployment.

- **Data Integrity**: Integration tests can verify the system's ability to handle various data formats and maintain data
  integrity. They ensure that all interactions, including those with databases and other external systems, preserve
  consistency and coherence.

- **Testing Comprehensive Scenarios**: They allow for testing more complex sequences or combinations of events that unit
  tests can't cover effectively. This includes scenarios like transactions, authentication flows, or intricate business
  processes.

- **Dependency Examination**: Integration tests check the system's reaction to an external dependency change. They
  ensure that upgrades or modifications in connected systems don't adversely impact your application.

- **Preparation for System Testing**: By ensuring that components interact as expected, integration tests set the stage
  for the broader scope of system testing, where the system's overall operation is evaluated in full.

### Functional tests

Functional tests are a key element in the software testing process, focusing on evaluating a system's functional
requirements. These tests check if the system behaves as expected, ensuring that features are functional from an
end-user's perspective. Functional tests are essential for several reasons:

- **User-Centric**: Functional tests are designed to reflect what users will do with the software. They help confirm
  that the software behaves as expected from a user's standpoint, ensuring all features are accessible, usable, and
  reliable.

- **Requirement Verification**: These tests are driven by the requirements and specifications of the software, ensuring
  that all stated functionalities are present and working correctly. They help in verifying that the deliverables meet
  the agreed-upon needs of the client or stakeholders.

- **System Behavior**: Functional tests evaluate the system's response to inputs, its processing, and the output
  produced. They confirm that each function of the software operates in conformance with the requirement specification.

- **Error Identification**: They help in identifying functional issues within the system, such as bugs or design flaws,
  that could affect the user experience. These might include issues with the software's operations, such as handling
  user input, processing data, and retrieving accurate information.

- **Data Handling**: Functional tests ensure that the application handles data correctly, following all the rules and
  validations. They check the software's ability to manage, retrieve, and store data as required, including interaction
  with databases and integration with other systems.

- **Accessibility and Security**: These tests often include aspects of accessibility for different types of users, as
  well as basic security tests to ensure that functional requirements related to security are being handled correctly.

- **Regression Testing**: Functional tests are crucial for regression testing, ensuring that new features, bug fixes, or
  modifications haven't disrupted or unintentionally altered existing functionality.

## Implementation and Structure

Our tests are located right next to the src folder of the code they are testing, in a folder
called [testing](../../../testing).
In it a folder for each type of tests:

### [Unit-tests](../../../testing/unit_tests)

In here, we implement all our unit tests.
This folder's structure is crucial - The folder structure should be identical to the structure of the production code
of the application, inside the [src folder](../../../src).
It should act as a mirror of the production code, and should be *updated accordingly when the production code changes.

We define a very clear definition of what is tested where and how.

- Each test would use the unittest framework.
- A testable artifact is either a **Function** or a **Class**.
- Each artifact will be tested separately in a different `TestCase` class.
- Each `TestCase` class will consist of several functions that check the same artifact in different ways.
- The name of the `TestCase` class will be:
    - `TestFunction<function name in CamelCase>` for functions
    - `TestClass<class name in CamelCase>` for classes
- Exactly one test case will be located in each script.
- The name of the script will be the exact name of the class it contains, in snake_case:
    - `test_function_<function name in snake_case>` for functions
    - `test_class_<class name in snake_case>` for classes
- The way the module hierarchy is reflected in the test hierarchy is as follows:
    - Each folder in the production code will have a corresponding folder in the unit-tests folder with the
      name `test_<folder name>`.
    - Each script in the production code will have a corresponding folder in the unit-tests folder with the
      name `test_<script name>`.
    - In the folder of each script there will be a single script for each artifact implemented in it, containing its
      test
      case. (as described above)

##### example:

For the given structure of the production code:

```text
--presentation_layer
----component1
------__init__.py
------script1.py
------script2.py
----component2
------__init__.py
------script3.py
------script4.py
--logic_layer
----component3
------...
```

The following will be the structure of the unit tests:

```text
unittests
--test_presentation_layer
----test_component1
------test_script1
--------test_function_func1.py
--------test_function_func2.py
------test_script2
--------test_function_func3.py
--------test_function_func4.py
----test_component2
------test_script3
--------test_function_func5.py
--------test_function_func6.py
------test_script4
--------test_function_func7.py
--------test_function_func8.py
--test_logic_layer
----....
```

----

> We don't require the creation and maintenance of integration tests and functional tests for each change made to the
> production code,
> but we do require the constant creation and maintenance of unit-tests for each change made to the production code.
>
> As mentioned above, we believe that unit-tests are really important, and we want to make sure that
> they always reflect the current state of the production code, and always cover the entire codebase.
