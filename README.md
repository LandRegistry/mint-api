# mint-api

This repository contains a flask application structured in the way that all
Land Registry flask APIs should be structured going forwards.

The purpose of this application is to sign a record before sending it to the register.


## Unit tests

The unit tests are contained in the unit_tests folder. [Pytest](http://docs.pytest.org/en/latest/) is used for unit testing. 

To run the unit tests if you are using the common dev-env use the following command:

```bash
docker-compose exec mint-api make unittest
or, using the alias
unit-test register
```

or

```bash
docker-compose exec mint-api make report="true" unittest
or, using the alias
unit-test register -r
```

# Linting

Linting is performed with [Flake8](http://flake8.pycqa.org/en/latest/). To run linting:
```bash
docker-compose exec mint-api make lint
```

## Endpoints

This application is documented in documentation/swagger.json
