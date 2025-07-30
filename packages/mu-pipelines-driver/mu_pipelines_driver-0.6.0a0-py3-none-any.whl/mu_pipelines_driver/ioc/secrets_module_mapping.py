from mu_pipelines_interfaces.config_types.global_properties.global_properties import (
    GlobalProperties,
)
from mu_pipelines_interfaces.config_types.secrets.secrets_config import (
    SecretsConfigItem,
)

from mu_pipelines_driver.ioc.import_mapped_class import ClassModuleMappingItem


class SecretsModuleMappingItem(ClassModuleMappingItem):
    provider: str


SECRET_MODULE_MAPPING: list[SecretsModuleMappingItem] = [
    {
        "provider": "databricks-spark",
        "module_path": "mu_pipelines_secrets_spark.databricks.databricks_secrets",
        "class_name": "DatabricksSecrets",
    },
    {
        "provider": "env",
        "module_path": "mu_pipelines_secrets.env_secrets.env_secrets",
        "class_name": "EnvSecrets",
    },
]


def find_secret_module_mapping_by_provider(
    mapping_provider: str, extra_modules: list[SecretsModuleMappingItem]
) -> SecretsModuleMappingItem | None:
    modules: list[SecretsModuleMappingItem] = SECRET_MODULE_MAPPING + extra_modules
    return next(
        (
            MAPPING
            for MAPPING in modules
            if MAPPING["provider"] == mapping_provider.lower()
        ),
        None,
    )


def find_secret_module_mapping(
    secrets_config: SecretsConfigItem,
    global_properties: GlobalProperties,
    extra_modules: list[SecretsModuleMappingItem],
) -> SecretsModuleMappingItem | None:
    # provider could be for a specific library type or any library type
    # in that order
    mapping_providers: list[str] = [
        "{provider}-{library_type}".format(
            provider=secrets_config["provider"],
            library_type=global_properties["library"],
        ).lower(),
        secrets_config["provider"].lower(),
    ]
    for mapping_provider in mapping_providers:
        mapping_item: SecretsModuleMappingItem | None = (
            find_secret_module_mapping_by_provider(mapping_provider, extra_modules)
        )
        if mapping_item is not None:
            return mapping_item

    return None
