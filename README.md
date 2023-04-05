# python-fast-api-template

[![Python](https://img.shields.io/badge/Python3.9-Python?style=for-the-badge&logo=Python)](https://www.python.org/downloads/release/python-390/)
[![FastAPI](https://img.shields.io/badge/FastAPI-FastAPI?style=for-the-badge&color=green)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Pydantic?style=for-the-badge&color=red)](https://docs.pydantic.dev/)
[![DependencyInjector](https://img.shields.io/badge/Dependency.Injector-DependencyInjector?style=for-the-badge&color=blue)](https://github.com/ets-labs/python-dependency-injector)

[![Linter](https://img.shields.io/badge/Codestyle-Black-black?style=for-the-badge)](https://github.com/psf/black)
[![Behave](https://img.shields.io/badge/Tests-BDD-BDD?style=for-the-badge&color=orange)](https://github.com/behave/behave)

## Getting Started

### Pre-requisites

- Install `python 3.9` or newer or [pyenv](https://github.com/pyenv/pyenv-installer)
- Install [poetry](https://python-poetry.org/docs/)

### Setup

```shell
# skip if python 3.9 is already installed with or without pyenv
pyenv install 3.9.10

# update path to your own python 3.9 installation
poetry env use ~/.pyenv/versions/3.9.10/bin/python3.9

# install packages
poetry install
```

### Usage

```shell
# format automatically code
make fmt

# run tests
make test

# formats code and run with reloading
make run_dev

# run
make run
```

### API Documentation

- [localhost:8000/docs](http://localhost:8000/docs) ([swagger.io/tools/swagger-ui](https://swagger.io/tools/swagger-ui/))
- [localhost:8000/redoc](http://localhost:8000/redoc) ([redocly.github.io/redoc/](https://redocly.github.io/redoc/))

## How to add new routes?

If you wanted to add `POST /x/y` you would do:

### Implement your new service

Implement your new service at `src/svc/x.py`.

You can define your `YRequest` and `YResponse` using pydantic in `src/models/x.py` for instance.

If your service has custom exceptions, add them there: `src/errors.py`.

If your service has a configuration:
- copy `src/config/server.py` into `src/config/x.py` and update it

### (Optional) Implement your new infra

Implement *repositories*, *external caches*, etc. under `src/infra` if your service requires some.

If your infra has a configuration:
- copy `src/config/server.py` into `src/config/my_shiny_infra.py` and update it

(e.g. database credentials)

### Add the new routes

Now we make your service accessible to the outside.

Copy `src/api/health.py` into `src/api/x.py` and update it to use your service.

Add your new router to `src/app.py`:

```python
# [...]
import src.api.x as api_x

def create_app() -> FastAPI:
    # [...]
    app.include_router(api_x.router)
    # [...]
```

If your endpoint brings new custom exceptions, then update `src/main.py` to add an `exception_handler` for every new exception.

### Update the dependency injection

We update the dependency injection so your endpoints will be able to use your new services & new infra (if you made one).

Update the `src/container.py`:

```python
# [...]
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.health",
            "src.api.x",  # TODO: add your new module
        ]
    )
    
    # config
    # [...]
    # TODO: add your new config if you have one, e.g.
    x_config: XConfig = providers.Singleton(XConfig)

    # infra
    # TODO: setup your new infra if you have some

    # services
    # TODO: setup your new service
    x: XService = providers.Singleton(
        XService,
        cfg=x_config,
    )
    # [...]
```

### Add BDD tests

Copy `tests/bdd/health.feature` into `tests/bdd/x.feature` and update it to use your new routes.

If you need custom steps, add them under `tests/bdd/steps`.

```bash
make test
```

```
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/__init__.py              6      0   100%
src/api/__init__.py          0      0   100%
src/api/health.py           25      7    72%   11-13, 19, 25, 31, 37
src/app.py                  21      1    95%   25
src/config/__init__.py       0      0   100%
src/config/server.py         9      0   100%
src/container.py             7      0   100%
src/errors.py                8      3    62%   3, 6, 11
src/infra/__init__.py        0      0   100%
src/main.py                 23     10    57%   15-16, 21-22, 27-32
src/svc/__init__.py          0      0   100%
src/svc/health.py           10      1    90%   7
------------------------------------------------------
TOTAL                      109     22    80%
```

> Coverage is only 80% because an example exception is not used

🎉
