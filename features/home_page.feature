Feature: Home Page Validation
  As a user
  I want to verify that the home page elements are displayed correctly

  Scenario: Verify home page elements
    Given I am on the 99acres home page
    Then the page title should be visible
    And the Projects tab should be displayed
    And the Search box should be displayed
    And the Search button should be displayed
