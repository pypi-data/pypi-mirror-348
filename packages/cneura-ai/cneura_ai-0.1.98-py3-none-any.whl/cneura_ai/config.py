import os
import json


class CLIConfig:
    # Immutable settings
    VERSION = "0.1.58"
    BASE_DIR = os.getcwd()
    CONFIG_DIR = os.path.join(BASE_DIR, "configs")
    DEFAULT_RUN_CONFIG = os.path.join(CONFIG_DIR, "run.json")
    DEFAULT_INIT_CONFIG = os.path.join(CONFIG_DIR, "init.json")
    DOCKER_COMPOSE_FILE = os.path.join(BASE_DIR, "docker-compose.yml")
    DEFAULT_NETWORK = "cneura_network"

    # Mutable fields (overridable via CLI)
    run_config_override = None
    init_config_override = None

    IMMUTABLE_FIELDS = {
        "VERSION", "BASE_DIR", "CONFIG_DIR",
        "DOCKER_COMPOSE_FILE", "DEFAULT_NETWORK"
    }

    @classmethod
    def ensure_paths(cls):
        if not os.path.exists(cls.CONFIG_DIR):
            os.makedirs(cls.CONFIG_DIR)

    @classmethod
    def apply_override(cls, override_path: str):
        if not os.path.exists(override_path):
            raise FileNotFoundError(f"Override config file not found: {override_path}")
        
        with open(override_path) as f:
            data = json.load(f)

        for key, value in data.items():
            if key in cls.IMMUTABLE_FIELDS:
                continue
            if hasattr(cls, key):
                setattr(cls, key, value)
