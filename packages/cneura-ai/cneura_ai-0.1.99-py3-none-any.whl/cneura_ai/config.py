import os
import json


class CLIConfig:
    VERSION = "0.2.0"
    BASE_DIR = os.getcwd()
    CONFIG_DIR = os.path.join(BASE_DIR, "configs")
    DEFAULT_RUN_CONFIG = os.path.join(CONFIG_DIR, "run.json")
    DEFAULT_INIT_CONFIG = os.path.join(CONFIG_DIR, "init.json")

    # Configurations of External services
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "host.docker.internal")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
    LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://host.docker.internal:8765")
    REMOTE_URL = os.getenv("REMOTE_URL", "tcp://host.docker.internal:2375")
    REDIS_HOST = os.getenv("REDIS_HOST", "host.docker.internal")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://host.docker.internal:27017/")
    CHROMA_HOST = os.getenv("CHROMA_HOST", "host.docker.internal")

    # Queues
    CODE_SYNTH_INPUT = "tool.code.synth"
    CODE_SYNTH_OUTPUT = "tool.code.test"
    CODE_SYNTH_ERROR = "tool.synth.error"
    CODE_TEST_INPUT = "tool.code.test"
    CODE_TEST_OUTPUT = "tool.code.deps"
    CODE_TEST_ERROR = "tool.test.error"
    CODE_DEPS_INPUT = "tool.code.deps_in"
    CODE_DEPS_OUTPUT = "tool.code.exec"
    CODE_DEPS_OUT = "tool.code.deps_out"
    CODE_DEPS_ERROR = "tool.deps.error"
    CODE_EXE_INPUT = "tool.code.exec"
    CODE_EXE_OUTPUT = "tool.code.debug"
    CODE_EXE_OUT = "tool.code.deploy"
    CODE_EXE_ERROR = "tool.exec.error"
    CODE_DEBUG_INPUT = "tool.code.debug"
    CODE_DEBUG_OUTPUT = "tool.code.test"
    CODE_DEBUG_ERROR = "tool.debug.error"
    TOOL_DEPLOY_INPUT = "tool.code.deploy"
    TOOL_DEPLOY_OUTPUT = "meta.agent.in"
    TOOL_DEPLOY_ERROR =  "tool.deploy.error"
    META_AGENT_INPUT = "meta.agent.in"
    META_AGENT_OUTPUT = "meta.agent.out"
    META_AGENT_ERROR = "meta.agent.error"

    run_config_override = None
    init_config_override = None

    IMMUTABLE_FIELDS = {
        "VERSION", "BASE_DIR", "CONFIG_DIR",
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
