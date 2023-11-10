# Developing Features Checklist


> Assuming that feature design, task ideation, grooming and estimation have been completed...

1) **Implement code**  - Implement the code to support the new feature in the appropriate place in the codebase.


2) **Implement valid tests** - write unittests to ensure that the code you have written works as expected, and to allow 
  checking if future changes break the feature.

> We support TDD (Test Driven Development) - the two previous steps can be swapped in order, according to the preference
> of the developer.

3) **Refactor Code** - If necessary, refactor the code to ensure that it is clean and readable.
  Make sure your code lines up with our [Conventions](..) to make sure the code promotes consistency, readability and 
  maintainability.


4) **Run All Tests** - Make sure that all the tests pass, not only those that you have written or those related directly
  to your changes; run all the unit-tests for the entire codebase to make sure nothing got broken in the process of 
  implementing your changes. (Surprisingly enough, this happens quite often...)


5) **Add Logging** - This is a step that is often forgotten, but is very important. Add concise, clear but expressive 
  logging to the code to allow for easy debugging and monitoring of the feature. Make sure to log any errors that may 
  occur, and any other information that may be useful for debugging - especially in production.


6) **Write Documentation** - For central features, write clear documentation in the appropriate place in the codebase
  using *markdown* files. Make sure other developers can easily understand how to use the feature, and how it works.


7) **Review Your Own Changes** - Before continuing for a code review, make sure to review your own changes. Make sure 
  that the code is clean, readable, and that the feature works as expected.


8) **Create a Pull Request** - Create a pull request for your changes, and assign it to the appropriate reviewer. 
  Make sure to include a clear description of the changes, and any other information that may be useful for the reviewer.


9) **You're Done** - Once the reviewer has approved your changes, you're done! The feature is now ready to be merged 
  into the master branch.
---
> Don't forget to update relevant places about the task being done - moving the Jira task to the "Read For Testing" 
> column, updating the task description with the relevant information, informing QA etc...
