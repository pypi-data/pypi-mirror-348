# Patronum: A Dependency Injection and Configuration Framework for Python

[![PyPI version](https://badge.fury.io/py/patronum.svg)](https://badge.fury.io/py/patronum) [![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Patronum is a modern, robust, and lightweight Python library designed to provide a Dependency Injection (DI) / Inversion of Control (IoC) container and a flexible configuration framework.

## Spring-like experience

Patronum is an independent project, partially inspired by the conventions and ease-of-use found in Spring Boot®. If you're a Python developer who appreciates Spring's way of managing components and configurations, Patronum is built for you.

Spring®, Spring Framework®, and Spring Boot® are trademarks of Broadcom Inc. and/or its subsidiaries. Patronum is not affiliated with, endorsed, or sponsored by Broadcom.

## License

Patronum is licensed under the MIT License.

# Quick-Start

## Installation

```bash
pip install patronum
```

## Basic usage

```python
# my_app/loggers.py
import abc
from patronum import Service, Qualifier

class Logger(abc.ABC):
    @abc.abstractmethod
    def log(self, message: str):
        pass

@Service
class ApplicationLogger(Logger):
    def log(self, message: str):
        print(f"[APPLICATION LOGGER]: {message}")

# my_app/main.py
from patronum import PatronumApplication, Annotated
from .loggers import Logger

def log_message(logger: Logger):
    logger.log("Hello world!")

if __name__ == "__main__":
    PatronumApplication.run(log_message)
```

# Key Features

Patronum aims to simplify your application structure and development process with the following core features:

**1. Intuitive Dependency Injection:**

- **`PatronumApplication.run(callable)`:** The heart of the DI container. Pass a callable, and Patronum will automatically find, instantiate, and inject its dependencies.
- **Component Scanning:**
  - `@Component` & `@Service`: Decorators to mark classes as managed beans. Optionally accepts a bean name.
  - `@Qualifier("name")`: Decorate components or bean methods to assign one or more unique names, allowing for precise dependency resolution.
- **Programmatic Bean Definition:**
  - `@Configuration`: Mark classes that define beans programmatically.
  - `@Bean`: Decorate methods within `@Configuration` classes. The return value of these methods are registered as beans. `@Qualifier` can also be used here.
- **Disambiguation & Control:**
  - `@Primary`: Mark a bean as the default candidate when multiple implementations of the same type exist.
  - **Strict Dependency Resolution:** Throws an error if multiple candidates are found for a dependency and none are marked `@Primary`.
- **Conditional Bean Creation:**
  - `@ConditionalOnClass(name, matchIfMissing=False)`: Bean is created only if the specified class (by fully qualified name string) is present (or missing, if `matchIfMissing=True`).
  - `@ConditionalOnProperty(propertyName, havingValue=None, matchIfMissing=False)`: Bean is created based on the presence or value of a configuration property.
- **Modern Python Support:**
  - Works seamlessly with plain Python classes, Pydantic models, and dataclasses.
  - Utilizes `typing.Annotated` for specifying injection criteria (e.g., `Annotated[MyType, "bean_name"]`).

**2. Powerful Configuration Framework:**

- **`@ActiveProfiles(["dev", "prod"])`:** Decorator to easily set active configuration profiles.
- **Flexible YAML Configuration:**
  - Loads and merges configurations from `application.yaml` files.
  - Supports profile-specific variants (e.g., `application-dev.yaml`, `application-prod.yaml`) which override base configurations.
  - Discovers configurations in the root module/directory and sub-modules/nested directories.
  - **Merging Strategy:** For YAML files, root-level configurations are loaded last and override properties from nested directories if conflicts occur. Profile-specific files override their non-profiled counterparts. OS environment variables always take precedence over YAML files.
- **Typed Configuration Properties** with `@ConfigurationProperties`:
  - `@ConfigurationProperties(prefix: str)`: Decorate a class (plain Python, Pydantic model, or dataclass) to bind properties from the merged configuration store directly to its fields.
  - The prefix argument specifies the namespace in the configuration (e.g., myapp.database).
  - Field names in the class are mapped to property keys (e.g., `user_name: str` within `myapp.database`-prefixed class, maps to `myapp.database.user_name`).
