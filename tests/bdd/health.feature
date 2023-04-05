Feature: Health
  Background:
    Given an API client
  Scenario: Health check: GET
    Given path: /
    When getting
    Then response code is 200
    And json response is "ok"
  Scenario: Health check: HEAD
    Given path: /
    When heading
    Then response code is 200
  Scenario: Health check: GET
    Given path: /health
    When getting
    Then response code is 200
    And json response is "ok"
  Scenario: Health check: HEAD
    Given path: /health
    When heading
    Then response code is 200
