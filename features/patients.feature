Feature: Patients Management
  As a system user
  I want to manage patients
  So that I can view and add patient information

  Background:
    Given the following users exist:
      | email                | password |
      | admin@hospital.com   | admin123 |
    And I am authenticated as "admin@hospital.com"

  Scenario: View patients list
    Given the following patients exist:
      | name        | email                 | phone      |
      | John Doe    | john@example.com      | 05321234567 |
      | Jane Smith  | jane@example.com      | 05329876543 |
    When I send a GET request to "/patients"
    Then the response status should be "200"
    And the response should contain "John Doe"
    And the response should contain "Jane Smith"

  Scenario: Create a new patient
    When I send a POST request to "/patients" with:
      | name         | Test Patient       |
      | email        | test@example.com   |
      | phone        | 05321111111        |
      | birth_date   | 1990-01-01         |
      | address      | Test Address       |
    Then the response status should be "201"
    And the response should contain "Test Patient"
    And the response should contain "test@example.com"
    When I send a GET request to "/patients"
    Then the response should contain "Test Patient"




