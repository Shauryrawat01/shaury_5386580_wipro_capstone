Feature: Property Details and Contact
  As a user
  I want to view property details and contact the seller

  Scenario: View Number Flow
    Given I have searched for a location
    When I click on the third property result
    And I switch to the new tab
    And I click 'OK GOT IT' if present
    And I click the 'View Number' button
    Then the contact details popup should be displayed
    And I take a screenshot of the view number result
