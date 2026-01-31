Feature: Transfers
  Scenario: User is able to receive an incoming transfer
    Given Account registry is empty
    And I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    When I do "incoming" transfer of amount "100.0" to account with pesel "89092909246"
    Then Account with pesel "89092909246" has balance equal to "100.0"

  Scenario: User is able to do an outgoing transfer
    Given Account registry is empty
    And I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I do "incoming" transfer of amount "100.0" to account with pesel "89092909246"
    When I do "outgoing" transfer of amount "40.0" to account with pesel "89092909246"
    Then Account with pesel "89092909246" has balance equal to "60.0"

  Scenario: User is able to do an express transfer
    Given Account registry is empty
    And I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I do "incoming" transfer of amount "100.0" to account with pesel "89092909246"
    When I do "express" transfer of amount "40.0" to account with pesel "89092909246"
    Then Account with pesel "89092909246" has balance equal to "59.0"
