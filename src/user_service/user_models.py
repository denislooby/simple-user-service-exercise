"""
Pydantic models for user data validation.
Models:
    - UserCreate: Model for creating a new user.
    - UserUpdate: Model for full updates to a user record.
    - UserPatch: Model for partial updates to a user record.
    - UserLogin: Model for login requests.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    """
    Pydantic model for POST endpoint
    """
    email: EmailStr = Field(..., json_schema_extra={"example":"user@example.com"})
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    last_login: Optional[str] = None
    model_config = {
        "extra": "forbid"
    }

class UserUpdatePut(BaseModel):
    """
    Pydantic model for PUT endpoint
    """
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    last_login: Optional[str] = Field(..., description="Required field, but we'll take null") # Using Optional allows null while .. requires field
    model_config = {
        "extra": "forbid"
    }


class UserUpdatePatch(BaseModel):
    """
    Pydantic model for PATCH endpoint
    """    
    name: Optional[str] = Field(None, min_length=1)
    password: Optional[str] = Field(None, min_length=6)
    last_login: Optional[str] = None
    model_config = {
        "extra": "forbid"
    }


class LoginRequest(BaseModel):
    """
    Pydantic model for LOGIN endpoint
    """
    email: EmailStr
    password: str
    model_config = {
        "extra": "forbid"
    }
    
