from abc import ABC, abstractmethod

from mu_pipelines_interfaces.context import Context
from mu_pipelines_interfaces.modules.destination_module_interface import (
    DestinationModuleInterface,
)
from mu_pipelines_interfaces.modules.execute_module_interface import (
    ExecuteModuleInterface,
)
from mu_pipelines_interfaces.modules.secrets_module_interface import (
    SecretsModuleInterface,
)


class IOCContainerInterface(ABC):
    @property
    @abstractmethod
    def context(self) -> Context:
        pass

    @property
    @abstractmethod
    def execute_modules(self) -> list[ExecuteModuleInterface]:
        pass

    @property
    @abstractmethod
    def destination_modules(self) -> list[DestinationModuleInterface]:
        pass

    @property
    @abstractmethod
    def secrets_modules(self) -> list[SecretsModuleInterface]:
        pass
