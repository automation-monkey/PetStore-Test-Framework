# kujan-hutage
Home Challenge For N26




# Running API Tests on your local machine
This project contains tests for the pet store sample hosted at https://petstore3.swagger.io written in Python3 using [pytest](https://docs.pytest.org/).


## Docker
In order to interact with the pet store server locally you will need to run it in a container.
- [Download and install](https://www.docker.com/products/docker-desktop)

Setup and configure a new container for the petstore project:
1. docker pull swaggerapi/petstore3:unstable
2. docker run  --name swaggerapi-petstore3 -d -p 8080:8080 swaggerapi/petstore3:unstable
3. Make sure the docker you created is up and running by going to http://localhost:8080/


## APITests
### 1. Repository
Fork https://github.com/automation-monkey/kujan-hutage.git and clone it to your machine.

```$ git clone git@github.com:automation-monkey/kujan-hutage.git```

### 2. Python
You will need at least Python 3.6 installed on your machine.
- [Download and install](https://www.python.org/downloads/)

### 3. Virtual env
Set up [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation) (or [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html)) using Python3

```$ mkvirtualenv -p python3 petstore-api-tests```

### 4. Install requirements

```$ pip3 install -r requirements.txt```

### 5. Testing environment

The configuration is set to local host by default.

Supported environments:
- http://localhost:8080/

### 6. Run a test!
Change directory to `N26`

```$ cd N26```

To run all the tests simply run

```$ pytest```

To make it verbose use

```$ pytest -v```

Use the path to the file to run a specific test 

```$ pytest /N26/tests/pet/test_pet.py```

You can generate a html and xml reports using

```$ pytest --html=html/report.html --junitxml=xml/report.xml```

To run tests in parallel specify the number of processes (N)

```$ pytest -n 4```

The basic command which runs all the tests in parallel and generates a report

```$ pytest -v --html=html/report.html --self-contained-html --junitxml=xml/report.xml tests/ -n 4```
