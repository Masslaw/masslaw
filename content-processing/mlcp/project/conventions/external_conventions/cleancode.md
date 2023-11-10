# Python Clean Code Guide

Based on Uncle Bob's principles of Clean Code, this guide provides a set of best practices tailored for Python developers to produce code that's easy to read, understand, and maintain.

**Recommendation:** For deeper insights into writing clean code, consider reading the book "Clean Code" by Robert C. Martin.

## Table of Contents

- [Meaningful Names](#meaningful-names)
- [Functions](#functions)
- [Comments](#comments)
- [Formatting](#formatting)
- [Objects and Data Structures](#objects-and-data-structures)
- [Error Handling](#error-handling)
- [Boundaries](#boundaries)
- [Unit Tests](#unit-tests)

## Meaningful Names

- **Use descriptive names**. Variables, functions, and classes should have names that explain their purpose.
  ```python
  # Bad:
  d = 10
  
  # Good:
  days_since_creation = 10
  ```

- **Avoid abbreviations**, unless they are universally known.
  
- **Variables and functions**: Use `snake_case`.
  
- **Classes**: Use `CamelCase`.

## Functions

- **Do one thing**. Functions should have a single responsibility. If they're doing more than one thing, consider splitting them.
  
- **Keep them small**. Ideally, functions should be short enough to be viewed without scrolling. It's easier to understand, test, and debug short functions.

- **Use descriptive names**. Like variables, the name of the function should describe its purpose.

- **Function arguments**: Functions should ideally have up to two or three arguments. This makes your function easier to read and use. If needed, use an object to encapsulate multiple parameters.

- **Avoid side effects**: A function should not alter global variables, class fields, or output parameters. Instead, they should return the result.

```python
def add_numbers(a, b):
    return a + b
```

- **Use exceptions rather than return codes**. Instead of returning error codes, consider throwing exceptions. This makes the code more readable as the error handling is separated from the main logic.

## Comments

- **Comments are not a substitute for bad code**. Instead of writing comments to explain a complex piece of code, refactor the code to make it clearer.

- **Write meaningful comments**. If you have to write a comment, ensure it adds value and explains the purpose of the code, any assumptions, and any side effects.

```python
# Bad:
# Increment x
x += 1

# Good:
# Updating the retry counter after a failed network call
retry_counter += 1
```

## Formatting

- **Follow PEP 8**, the Python Enhancement Proposal which provides guidelines and best practices on how to format your Python code.

- **Use consistent indentation**. Stick to 4 spaces as the default indentation level.

- **Limit line length**. As per PEP 8, aim for a maximum of 79 characters for regular code and 72 for comments.

- **Use blank lines** to separate functions, classes, and blocks of code inside functions.

## Objects and Data Structures

- **Use encapsulation**. Rather than using data structures directly, consider using objects with methods that operate on their data.

- **Avoid global variables**. Instead, use class variables and pass them as parameters to functions if required.

## Error Handling

- **Use exceptions for error handling**. As mentioned, instead of returning error codes, throw exceptions to handle errors. This makes the code cleaner and more maintainable.

- **Don't return null or None**. Instead of returning null, consider throwing an exception or returning a special case object.

## Boundaries

- **Separate your concerns**. Ensure that each module or class has a single responsibility. This makes the code more modular and easier to test.

## Unit Tests

- **Write tests**. Follow the TDD (Test-Driven Development) principle of writing tests before your actual code. This ensures that your code is always testable.

- **Each test should have a single reason to fail**. This makes it easier to pinpoint issues when they arise.

- **Use meaningful names for your tests**. The name should describe the expected behavior and the scenario under which it's tested.

```python
def test_add_numbers_with_positive_integers():
    result = add_numbers(1, 2)
    assert result == 3
```

- **Mock external services**. When testing functions or methods that depend on external services, mock those services to ensure your tests only test your code and are not affected by external factors.

## Conclusion

Clean code is essential for maintainability, scalability, and the overall health of your project. By adhering to these guidelines and principles, you'll produce code that not only works but is also a pleasure to read and work with. Always remember, "Code is read much more often than it is written," so write it with the reader in mind.
