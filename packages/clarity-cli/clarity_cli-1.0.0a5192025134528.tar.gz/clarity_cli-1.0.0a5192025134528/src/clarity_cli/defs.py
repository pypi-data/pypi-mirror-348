from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from enum import Enum
from pydantic import BaseModel


# Define the base directory for storing configuration
CONFIG_DIR = Path.home() / '.clarity'
CONFIG_FILE = CONFIG_DIR / 'config.json'
TOKEN_FILE = CONFIG_DIR / 'token.json'

EXECUTION_VIEW_PATH = 'testing/executions/view?executionId={execution_id}&projectId={project_id}'
DEVICES_LIST = 'inv-api/devices/status'
TEST_LIST = 'inv-api/testing/catalog'


class ThemeColors(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    CYAN = "cyan"
    WHITE = "white"
    RED = "red"


@dataclass
class TableColumn:
    name: str
    color: Optional[ThemeColors] = ThemeColors.WHITE


class ProfileConfig(BaseModel):
    client_id: str
    client_secret: str
    token_endpoint: str
    scope: str
    project: Optional[str] = ""
    workspace: Optional[str] = ""
    agent: Optional[str] = ""
    domain: str


class InputTypes(Enum):
    integer = int
    string = str
    boolean = bool
