"""TMTCrunch defaults and settings functions."""

__all__ = [
    "load_config",
    "load_default_config",
    "load_phospho_config",
    "format_settings",
]


import os.path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


CONFDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf")
DEFAULT_CONFIG_FILE = os.path.join(CONFDIR, "default.toml")
PHOSPHO_CONFIG_FILE = os.path.join(CONFDIR, "phospho.toml")


def load_config(fpath: str) -> dict:
    """
    Load configuration from a file.

    :param fpath: Path to config file.
    :return: settings.
    """
    with open(fpath, "rb") as f:
        settings = tomllib.load(f)
    return settings


def load_default_config() -> dict:
    """
    Load default configuration.

    :return: settings.
    """
    return load_config(DEFAULT_CONFIG_FILE)


def load_phospho_config() -> dict:
    """
    Load default configuration for phospho-proteomics.

    :return: settings.
    """
    return load_config(PHOSPHO_CONFIG_FILE)


def format_settings(settings: dict, pretty=True) -> str:
    """
    Return formatted representation of `settings`.

    :param settings: TMTCrunch settings.
    :param pretty: If True, add header and footer.
    :return: Formatted string.
    """
    header = "====  settings  ===="
    footer = "=" * len(header)

    settings_str = ""
    if pretty:
        settings_str += header + "\n"
    for key, value in settings.items():
        if key == "psm_group":
            settings_str += f"{key}: " + "{\n"
            for group, group_cfg in value.items():
                settings_str += f"  {group}: {group_cfg},\n"
            settings_str += "}\n"
        else:
            settings_str += f"{key}: {value}\n"
    if pretty:
        settings_str += footer
    else:
        settings_str = settings_str[:-1]
    return settings_str
