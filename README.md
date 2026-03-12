# ASSSIGNMENT-1
SOFTWARE TESTING



------- Flipkart Search & Product Filter – Automated Test Suite -------

Overview

-This project contains an automated test suite developed to validate the Search and Product Filter module of the Flipkart e-commerce website. The automation framework is built using Python, Selenium WebDriver, pytest, and pytest-html. The purpose of this project is to verify that the search functionality and filtering options in the Flipkart application work correctly under different scenarios. The test suite includes both positive test cases and negative test cases to ensure that the application behaves as expected when valid as well as invalid inputs are provided.
-The automation script interacts with the Flipkart website through Selenium WebDriver and simulates real user actions such as searching for products, applying filters, sorting results, and validating the displayed results. The framework also generates an HTML test report after execution, which provides detailed information about the test results. Additionally, screenshots are automatically captured during the execution of test cases and embedded into the test report to assist in debugging and analysis.

Test Coverage

-The automated test suite includes a total of 15 test cases, which consist of 10 positive test scenarios and 5 negative test scenarios. The positive test cases verify normal system behavior, such as performing a valid product search, filtering products by price range, filtering by brand, applying customer rating filters, sorting products by price, applying multiple filters simultaneously, selecting products using auto-suggestions, excluding out-of-stock products, filtering by discount percentage, and clearing applied filters.
-The negative test cases are designed to validate how the application handles incorrect or unusual input. These scenarios include submitting an empty search query, entering only special characters in the search box, providing an invalid price range where the minimum price is greater than the maximum price, submitting an extremely long search string, and searching for a completely non-existent or meaningless product keyword. These tests ensure that the application handles edge cases gracefully without crashing or producing unexpected behavior.

Framework and Tools

-The automation framework is developed using Python as the programming language. Selenium WebDriver is used to automate browser interactions and perform actions such as opening the Flipkart website, locating elements on the page, entering search queries, clicking filters, and validating results. The pytest framework is used to structure the test cases and manage test execution. It provides features such as fixtures, assertions, and easy test organization.
-The project also uses pytest-html to generate detailed HTML reports after the execution of test cases. These reports display information such as test status, execution details, and embedded screenshots for failed or executed tests. The webdriver-manager package is included to automatically manage the browser driver required for running Selenium tests.

Execution Process

-To run the test suite, the required dependencies must first be installed. Once the dependencies are installed, the test cases can be executed using the pytest command. During execution, the framework launches the Chrome browser, navigates to the Flipkart website, and performs automated interactions based on the defined test scenarios. Each test runs independently and uses a fresh browser instance to ensure that results are not affected by previous test executions.
-When the test execution completes, an HTML report file is generated that summarizes the results of all executed test cases. The report indicates whether each test case passed or failed and includes screenshots captured during execution. These screenshots help testers understand the state of the application at the time the test was performed.

Project Structure

-The project consists of multiple files that work together to implement the automation framework. The main test logic is contained in the test script file, which includes all the defined test cases for the search and filter functionality. The pytest configuration file contains settings related to HTML report generation and automatic screenshot capture. A requirements file lists all the Python dependencies required to run the project. The repository also includes the README file, which provides documentation about the project and instructions for execution.

Conclusion

-This project demonstrates the implementation of a web automation testing framework for an e-commerce application. By automating the testing process, it becomes easier to verify application functionality, identify defects quickly, and ensure consistent test execution. The use of Selenium with pytest provides a flexible and scalable testing solution, while the generated reports and screenshots help testers analyze test results effectively.
