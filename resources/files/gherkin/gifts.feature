Feature: Gifts
    Scenario: Send a Thank You note for a gift
        Given a gift
        And I am polite
        When you can
        Then send a thank you note

    Scenario: Regift a gift
        Given a gift
        And I don't like it
        And I don't think I'll get in trouble for regifting
        Then give it to someone else as a gift
