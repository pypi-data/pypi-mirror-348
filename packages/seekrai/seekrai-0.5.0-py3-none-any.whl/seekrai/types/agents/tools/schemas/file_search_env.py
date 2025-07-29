from pydantic import Field

from seekrai.types.agents.tools.env_model_config import EnvConfig


# TODO: figure out better way of creating tool environment models (within tool ideally), but retaining separate model_configs
class FileSearchEnv(EnvConfig):
    file_search_index: str
    document_tool_desc: str
    top_k: int = Field(default=10)
    score_threshold: int = Field(default=0)
