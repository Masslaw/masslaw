# Python Coding Conventions Guide

This guide outlines our recommended conventions for writing Python code. Following these guidelines will ensure that our
codebase remains consistent, readable, and maintainable.

## Table of Contents

- [Indentation](#indentation)
- [Naming Conventions](#naming-conventions)
- [Line Length](#line-length)
- [Imports](#imports)
- [Comments](#comments)
- [Whitespace in Expressions and Statements](#whitespace-in-expressions-and-statements)
- [PyCharm Tips](#pycharm-tips)

## Indentation

- Use 4 spaces per indentation level.
- Do not mix spaces and tabs in the same project.
- Use spaces by default unless the project you're working on uses tabs.

## Naming Conventions

- **Variables** and **function/method names**: Use `snake_case`.
  ```python
  user_name = "Alice"
  def fetch_data():
      pass

- **Constants**: Use `UPPER_SNAKE_CASE`.
  ```python
  PI = 3.14159
  MAX_SIZE = 100
  ```

- **Classes**: Use `CamelCase`.
  ```python
  class UserAccount:
    pass
  ```

- Avoid using names that clash with keywords of Python
  ```python
  # Bad
  list = [1, 2, 3]
  
  # Good
  numbers = [1, 2, 3]
  ```

## Line Length

- Limit all lines to a maximum of **79 characters** for code, and **72 characters** for comments.

## Imports

- Imports should be on separate lines.
  ```python
  # Bad:
  import os, sys
  
  # Good:
  import os
  import sys
  ```

- Import order should be:
    1. Standard library imports
    2. Related third party imports
    3. Local application/library specific imports

- Use absolute imports, with an exception for simple cases where a local import is clearer.

## Comments

- Comments should be complete sentences.
- If a comment is a sentence or longer, capitalize the first letter and use punctuation.
- Use inline comments sparingly.

## Whitespace in Expressions and Statements

Avoid extraneous whitespace:

```python
# Bad:
spam(ham[1], {eggs: 2})

# Good:
spam(ham[1], {eggs: 2})
```

##  PyCharm Tips
To maintain these conventions effortlessly, it's recommended to use the PyCharm IDE, which offers excellent support 
for Python development.

#### Using the Code Convention Plugin in PyCharm:
1. Open PyCharm and go to Preferences or Settings.
2. Navigate to Plugins and search for "Code Convention".
3. Install and enable the plugin.
4. After activation, the plugin will highlight unconventional writings in your code.

By using this plugin, you can ensure that your code adheres to the conventions outlined in this guide.

> To run a quick fix to the code and automatically fix the highlighted issues, use the keybind specified in Pycharm's
> keybind settings under `Main Menu > Code > Code Formatting Actions > Reformat File...` (default keybind: `⇧⌥F` 
> for mac) - striking a file with a simple input like that just before committing changes in it won't hurt :)

----

Note: This guide is largely influenced by [PEP 8](https://peps.python.org/pep-0008/), Python's official style guide. For more detailed conventions and 
additional recommendations, refer to PEP 8.
