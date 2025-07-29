from typing_extensions import Literal, Any, Union, Dict
from toml import load, dump
from os import makedirs
from pathlib import Path

__version__ = "0.1.0"
__all__ = ["config", "get_config", "remove_config", "init", "initsettings",
           "LOCAL", "GLOBAL", "ALL", "HOME", "CWD"
        ]

initsettings = {}

LOCAL = "local"
GLOBAL = "global"
ALL = "all"

HOME = Path.home()
CWD = Path.cwd()

def init(**kwargs):
    global initsettings

    initsettings.update(kwargs)

def config(
    config_name: str,
    value: Any,
    config_type: Literal["local", "global"]=initsettings.get("default_config_type", LOCAL)
):
    local_config_path = initsettings.get("local_config_path", Path.home() / "appdata" / "Roaming" / "xystudio" / "configurer" / "config.toml")
    global_config_path = initsettings.get("global_config_path", Path.cwd() / ".xystudio" / "configurer" / "config.toml")

    makedirs(global_config_path.parent, exist_ok=True)
    makedirs(local_config_path.parent, exist_ok=True)

    if not(local_config_path.exists()):
        local_config_path.touch()
    if not(global_config_path.exists()):
        global_config_path.touch()

    if initsettings.get("must_two_texts", False):
        config_split = config_name.split(".", 1)
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
        except IndexError:
            raise ValueError("config name must with two texts, example : 'a.b'.")
        if config_type == LOCAL:
            with open(local_config_path, "r", encoding="utf-8") as f:
                config = load(f)
                config.update({config_char_1 : {config_char_2 : value}})
            with open(local_config_path, "w", encoding="utf-8") as f:
                dump(config, f)
        elif config_type == GLOBAL:
            with open(global_config_path, "r", encoding="utf-8") as f:
                config = load(f)
                config.update({config_char_1 : {config_char_2 : value}})
            with open(global_config_path, "w", encoding="utf-8") as f:
                dump(config, f)
        else:
            raise ValueError("This config type not found.")
    else:
        if config_type == LOCAL:
            with open(local_config_path, "r") as f:
                local_config = load(f)
            local_config[config_name] = value
            with open(local_config_path, "w") as f:
                dump(local_config, f)
        elif config_type == GLOBAL:
            with open(global_config_path, "r") as f:
                global_config = load(f)
            global_config[config_name] = value
            with open(global_config_path, "w") as f:
                dump(global_config, f)
        else:
            raise ValueError("Invalid config type.")

def get_config(config_name:str, default: Any=None) -> Any:
    global_config_path = Path(initsettings.get("local_config_path", Path.home() / "appdata" / "Roaming" / "xystudio" / "configurer"))
    local_config_path = Path(initsettings.get("global_config_path", Path.cwd() / ".xystudio" / "configurer"))

    if config_name == ALL:
        with open(local_config_path, "r") as f:
            local_config = load(f)
        with open(global_config_path, "r") as f:
            global_config = load(f)
        return {**local_config, **global_config}
    if local_config_path.exists():
        with open(local_config_path, "r") as f:
            local_config = load(f)
        if config_name in local_config:
            return local_config[config_name]
    if global_config_path.exists():
        with open(global_config_path, "r") as f:
            global_config = load(f)
        if config_name in global_config:
            return global_config[config_name]
    return default


def remove_config(
    config_name: str, config_type: Literal["local", "global"]
):
    global_config_path = Path(initsettings.get("local_config_path", Path.home() / "appdata" / "Roaming" / "xystudio" / "configurer"))
    local_config_path = Path(initsettings.get("global_config_path", Path.cwd() / ".xystudio" / "configurer"))

    if config_type == LOCAL:
        with open(local_config_path, "r") as f:
            local_config = load(f)
        if config_name in local_config:
            del local_config[config_name]
        with open(local_config_path, "w") as f:
            dump(local_config, f)
    elif config_type == GLOBAL:
        with open(global_config_path, "r") as f:
            global_config = load(f)
        if config_name in global_config:
            del global_config[config_name]
        with open(global_config_path, "w") as f:
            dump(global_config, f)
    else:
        raise ValueError("Invalid config type.")

__init__ = init

def main():
    pass

if __name__ == "__main__":
    main()