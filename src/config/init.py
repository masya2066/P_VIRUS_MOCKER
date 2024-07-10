import yaml
import os


def ensure_config_exists():
    config_dir = "configs"
    config_file_path = os.path.join(config_dir, "config.yml")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file_path):
        default_config = {
            "server": {
                "port": 8080
            },
            "database": {
                "host": "127.0.0.1",
                "port": 5432,
                "username": "admin",
                "password": "admin",
                "name": "dbname"
            }
        }
        with open(config_file_path, "w") as config_file:
            yaml.dump(default_config, config_file)


def InitConfig():
    ensure_config_exists()
    try:
        with open("configs/config.yml", "r") as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        raise Exception("The config file was not found.")
    except yaml.YAMLError as exc:
        raise Exception(f"Error in configuration file: {exc}")
    return config


def set_env_from_config(config):
    for section, settings in config.items():
        if isinstance(settings, dict):
            for key, value in settings.items():
                env_var_name = f"{section.upper()}_{key.upper()}"
                os.environ[env_var_name] = str(value)
        else:
            env_var_name = f"{section.upper()}"
            os.environ[env_var_name] = str(settings)
