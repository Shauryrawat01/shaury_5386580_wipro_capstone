Feature: Property Search and Filters
  As a user
  I want to search for properties and apply filters

  Scenario: Location Search Flow
    Given I am on the 99acres home page
    When I click on the Projects tab
    And I enter the location from test data
    And I select the location from suggestions
    And I click the Search button
    Then the search results page should be displayed

  Scenario: Property Search Filter Refinement
    Given I have searched for a location
    When I apply the 3 BHK filter
    And I apply the 2036 filter
    Then the required property card should be visible

  Scenario: Invalid Location Search
    Given I am on the 99acres home page
    When I click on the Projects tab
    And I enter an invalid location "InvalidLocation12345"
    And I click the Search button
    Then I should see a message indicating no results were found

  Scenario: Empty Location Search
    Given I am on the 99acres home page
    When I click on the Projects tab
    And I enter an empty location
    And I click the Search button
    Then I should see a message indicating no results were found
