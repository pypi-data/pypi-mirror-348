# stenv [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Python decorator for generating meaningfully type-safe environment variable accessors.

Currently, only `pyright` is capable of correctly type checking the generated accessors. `pyre`,
`mypy`, and `pytype` will all report false positives.

## Requirements

- Python 3.10+

## Installation

```bash
pip install stenv
```

## Example

stenv provides a way to access environment variables with automatic type conversion based on
type annotations. The types are meaningful and can be checked by static type checkers: optionals
might be `None`, whereas non-optional types must be set (either in the environment or as a default
value).

```python
from pathlib import Path
from stenv import env

class Env:
    prefix = "MYAPP_"

    @env[Path]("PATH", default="./config")
    def config_path():
        pass

    @env[int | None]("PORT")
    def port():
        pass

# The following line returns a Path object read from MYAPP_PATH environment
# variable or the ./config default if not set.
print(Env.config_path)

# Since Env.port is an optional type, we need to check if it is not None,
# otherwise type checking will fail.
if Env.port is not None:
    print(Env.port)  #< We can expect Env.port to be an integer here.
```

## Usage

### Required Environment Variables

If a type is not optional, it must be set either in the environment or as a default value.

```python
from stenv import env

class Env:
    @env[str]("API_KEY")
    def api_key():
        pass
```

This class definition will raise a `RuntimeError` if the `API_KEY` environment variable is not set
when the class is imported.

Values can be defined optional (e.g. `int | None`, `Optional[int]`, `Union[int, None]`) which
removes this enforcement while also informing the type checker that the value might be `None`:

```python
from stenv import env

class Env:
    @env[int | None]("PORT")
    def port():
        pass
```

It is also possible to define a default value that will be used if the environment variable is not
set.

```python
from stenv import env

class Env:
    @env[str]("API_KEY", default="default_api_key")
    def api_key():
        pass
```

### Environment Variable Prefixing

```python
from stenv import env
from pathlib import Path
from typing import Optional

class AppConfig:
    prefix = "APP_"  # Will be prepended to all environment variable names.

    @env[int]("PORT", default=8000)
    def port():  #< Will be transformed into a class property with type int.
        pass

    @env[Path | None]("LOG_FILE")
    def log_file():  #< Will be transformed into a class property with type Path | None.
        pass

print(AppConfig.port) # APP_PORT environment variable
print(AppConfig.log_file) # APP_LOG_FILE environment variable
```

### Custom types

It is possible to use a custom type with a constructor that takes a string.

```python
import re

class Email:
    def __init__(self, email_string: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_string):
            raise ValueError(f"Invalid email: {email_string}")
        self.address = email_string
        self.username, self.domain = email_string.split("@", 1)

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.address == other.address
        return False

class Env:
    @env[Email]("EMAIL")
    def email():
        pass

print(Env.email.username)
print(Env.email.domain)
```

### Parsers

Parser functions may be used to convert the environment variable value to a different type.

```python
from datetime import date

def parse_numlist(s: str) -> list[int]:
    return [int(x) for x in s.split(",")]

class Env:
    @env[date]("TEST_DATE", parser=date.fromisoformat)
    def test_date():
        pass

    @env[list[int]]("TEST_NUMBERS", parser=parse_numlist)
    def numbers():
        pass

print(Env.test_date)
print(Env.numbers)
```

### Type annotations are optional

While type annotations are optional, leaving them out kinda defeats the purpose of the library,
for the most part. That said, when type annotations are not provided, the type will be assumed to
be `str`.

```python
class Env:
    @env("API_KEY")
    def api_key():  #< str
        pass
```

### Return types also work, but with a caveat

```python
class Env:
    @env("PORT")
    def port() -> int:
        pass

    @env("API_KEY")
    def api_key() -> str | None:
        pass
```

The above code will do what you would expect (`Env.port` is an integer, `Env.api_key` is a string or
`None`), but the type checker will complain about the return type not matching the type annotation
and type metaprogramming in Python is not yet powerful enough to express this.

## FAQ

### Why would you do this?

Static type checking is a powerful way to catch bugs early in the development process. `stenv`
allows expressing assumptions about the environment variables a program uses.

It was also just fun to make.

### Is this production-ready?

I used a version of this code in production for a while. That being said, this is an early
implementation that is yet to be battle-tested. The fact that only `pyright` can correctly type
check the generated accessors might be a deal-breaker for some. Use at your own risk.

### What's with the name?

`st` in the name stands for `statically typed`. Initially, I wanted to name it some clever word play
on "env" (like envy, envious, etc.) but the amount of people who had the exact same idea on PyPI is
staggering.

## License

MIT NON-AI
