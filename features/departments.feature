Feature: Departments Management
  As a system user
  I want to manage departments
  So that I can view and add department information

  Background:
    Given the following users exist:
      | email                | password |
      | admin@hospital.com   | admin123 |
    And I am authenticated as "admin@hospital.com"

  Scenario: View departments list
    Given the following departments exist:
      | name        | description                    |
      | Cardiology  | Heart and circulation diseases |
      | Neurology   | Nervous system diseases        |
    When I send a GET request to "/departments"
    Then the response status should be "200"
    And the response should contain "Cardiology"
    And the response should contain "Neurology"

  Scenario: Create a new department
    When I send a POST request to "/departments" with:
      | name         | Orthopedics              |
      | description  | Bone and joint diseases  |
    Then the response status should be "201"
    And the response should contain "Orthopedics"
    And the response should contain "Bone and joint diseases"
    When I send a GET request to "/departments"
    Then the response should contain "Orthopedics"




