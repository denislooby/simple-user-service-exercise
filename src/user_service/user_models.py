from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example":"user@example.com"})
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    last_login: Optional[str] = None
    model_config = {
        "extra": "forbid"
    }

class UserUpdatePut(BaseModel):
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    last_login: Optional[str] = Field(..., description="Required field, but we'll take null") # Using Optional allows null while .. requires field
    model_config = {
        "extra": "forbid"
    }


class UserUpdatePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    password: Optional[str] = Field(None, min_length=6)
    last_login: Optional[str] = None
    model_config = {
        "extra": "forbid"
    }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    model_config = {
        "extra": "forbid"
    }
    
