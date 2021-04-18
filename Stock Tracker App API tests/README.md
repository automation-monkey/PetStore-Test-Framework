# The Test Engineering Challenge

This project contains automated API testing framework for the [Stock Tracker App](https://github.com/automate-digital/stocktracker-py) written in Python3 using 
[pytest](https://docs.pytest.org/).

## Test Plan   

1. Test Scope:
   

    - Stock Tracker App and its functionalities:
      - Add/Update holding
      - Remove holding
      - Get Valuation
      - Get Portfolio


2. Test Schedule:
   

    - Start date: Friday, April 16 18:00
    - Requirement Understanding
    - Test Plan creation
    - Test Cases creation
    - Test Execution in Different Environments
    - QA Sign-off
    - End date: Monday, April 19 18:00


3. Test Types:
   

    - The overall application will include the following testing types/techniques:
        - Feature > Basic Feature Testing
        - GUI > Basic Validate look and feel of the application
        - Database > Basic Verification of DB interactions (csv file)
        - E2E > Validate flows
        - Business Rule > Validate rules with positive/negative conditions
        - Service Level Testing > Validate web service level features (API`s)
        - Error Handling > Verify Application's Error handling
   

4. Test Environment
   

      - Local Environment
   
5. Test Approach


      Test levels: Acceptance Testing
      Test types: Happy Path, Functional, E2E, Exploratory, Blackbox
   
6. Exit Criteria
   

      - All features been verified and covered by tests
      - Manual tests have passed
      - No Critical or Blocker defects outstanding.
      - Automation Suite Successfully Passed.


7. Open Risks/Issues
      

      - Risks: In case of downtime on the 3rd party software the App doesn't handle those cases.
      - Issues: None





### Notes on improvements that could be considered to further develop the tests
Since the app is based on a 3rd party API I suggest:
- Add tests that check the actual valuation of stocks added to app and comparing it with the portfolio created by the app.
- Create cases that check how app behaves during downtime, since app is relaying on [alphavantage](https://www.alphavantage.co/) endpoints.