import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from seekrai.types.agents.tools.tool_types import Tool


class AgentStatus(str, enum.Enum):
    INACTIVE = "Inactive"
    PENDING = "Pending"
    ACTIVE = "Active"
    FAILED = "Failed"


class CreateAgentRequest(BaseModel):
    name: str
    instructions: str
    tools: list[Tool]
    model_id: str


class Agent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    instructions: str
    status: AgentStatus
    model_id: str
    user_id: str
    tools: list[Tool]
    created_at: datetime
    updated_at: datetime
    last_deployed_at: Optional[datetime] = None
    active_duration: int = Field(default=0, ge=0)


class AgentDeleteResponse(BaseModel):
    id: str
    deleted: bool
