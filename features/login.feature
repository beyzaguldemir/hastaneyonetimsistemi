Feature: User Login
  As a system user
  I want to login to the system
  So that I can access the hospital management system

  Background:
    Given the following users exist:
      | email                | password |
      | admin@hospital.com   | admin123 |
      | user@hospital.com    | user123  |

  Scenario: Successful login with valid credentials
    When I send a POST request to "/users/login" with:
      | email             | admin@hospital.com |
      | password          | admin123           |
    Then the response status should be "200"
    And the response should contain "Login successful"
    And the response should contain "admin@hospital.com"

  Scenario: Failed login with invalid credentials
    When I send a POST request to "/users/login" with:
      | email             | admin@hospital.com |
      | password          | wrongpassword      |
    Then the response status should be "401"
    And the response should contain "Invalid email or password"




