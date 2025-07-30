from typing import Any, cast

from mu_pipelines_interfaces.config_types.secrets.secret_value_mapping import (
    SecretValueMapping,
)
from mu_pipelines_interfaces.context import GetSecretFunc
from mu_pipelines_interfaces.modules.secrets_module_interface import (
    SecretsContext,
    SecretsModuleInterface,
)

from mu_pipelines_driver.ioc.ioc_container_interface import IOCContainerInterface


def build_get_secret_func(ioc_container: IOCContainerInterface) -> GetSecretFunc:
    def get_secret(secret_value_mapping: SecretValueMapping) -> Any:
        secret_module: SecretsModuleInterface | None = next(
            (
                module
                for module in ioc_container.secrets_modules
                if module.secret_name == secret_value_mapping["secret_name"]
            ),
            None,
        )
        if secret_module is None:
            raise ModuleNotFoundError(
                f"Unable to find SecretsModule for secret named: {secret_value_mapping['secret_name']}"
            )

        secrets: Any | None = secret_module.get(
            cast(SecretsContext, ioc_container.context)
        )

        if secrets is None:
            raise Exception(
                f"Unable to retrieve secret named: {secret_value_mapping['secret_name']}"
            )

        if "secret_value" in secret_value_mapping and isinstance(secrets, dict):
            return cast(dict, secrets)[secret_value_mapping["secret_value"]]

        return secrets

    return get_secret
