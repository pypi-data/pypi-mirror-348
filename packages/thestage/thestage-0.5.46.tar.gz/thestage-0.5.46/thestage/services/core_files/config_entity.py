from typing import Optional

from pydantic import BaseModel, Field

# saved to file
class MainConfigEntity(BaseModel):
    thestage_auth_token: Optional[str] = Field(None, alias='thestage_auth_token')
    thestage_api_url: Optional[str] = Field(None, alias='thestage_api_url')

# not saved to file
class RuntimeConfigEntity(BaseModel):
    working_directory: Optional[str] = Field(None, alias='working_directory')
    config_global_path: Optional[str] = Field(None, alias='config_global_path')


class ConfigEntity(BaseModel):
    global_config_path: str = Field(None, alias='global_config_path')
    can_use_inference: bool = Field(None, alias='can_use_inference')
    main: MainConfigEntity = Field(default_factory=MainConfigEntity, alias='main')
    runtime: RuntimeConfigEntity = Field(default_factory=RuntimeConfigEntity, alias="runtime") # TODO merge with main
