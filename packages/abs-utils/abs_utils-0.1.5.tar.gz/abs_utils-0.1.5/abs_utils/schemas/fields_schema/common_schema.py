from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from enum import Enum

class ValidationRules(BaseModel):
    """Validation rules for form fields."""
    required: bool = Field(default=False, description="Whether the field is required")
    min_length: Optional[int] = Field(default=None, description="Minimum length of the field")
    max_length: Optional[int] = Field(default=None, description="Maximum length of the field")
    min_value: Optional[float] = Field(default=None, description="Minimum value of the field")
    max_value: Optional[float] = Field(default=None, description="Maximum value of the field")
    pattern: Optional[str] = Field(default=None, description="Regex pattern for field validation")

    @field_validator('min_length', 'max_length')
    def validate_length(cls, v, values, field):
        if v is not None and v < 0:
            raise ValueError(f"{field.name} cannot be negative")
        if 'min_length' in values and 'max_length' in values:
            if values['min_length'] is not None and values['max_length'] is not None:
                if values['min_length'] > values['max_length']:
                    raise ValueError("min_length cannot be greater than max_length")
        return v

    @field_validator('min_value', 'max_value')
    def validate_value(cls, v, values, field):
        if v is not None and 'min_value' in values and 'max_value' in values:
            if values['min_value'] is not None and values['max_value'] is not None:
                if values['min_value'] > values['max_value']:
                    raise ValueError("min_value cannot be greater than max_value")
        return v

class Option(BaseModel):
    """Option for select-type fields."""
    label: str = Field(description="Display label for the option")
    value: Any = Field(description="Value associated with the option")

class FieldType(str,Enum):
    """Supported field types for form fields."""
    TEXT = "text"
    TEXTAREA = "textarea"
    EMAIL = "email"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    DROPDOWN = "dropdown"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    FILE = "file"
    IMAGE = "image"
    URL = "url"
    JSON = "json"
    RICHTEXT = "richtext"
    LIST = "list"

class BaseFieldSchema(BaseModel):
    """Base schema for field definitions."""
    name: str = Field(description="Name of the field")
    label: str = Field(description="Display label for the field")
    type: FieldType = Field(description="Type of the field")
    default_value: Optional[Any] = Field(default=None, description="Default value for the field")
    placeholder: Optional[str] = Field(default=None, description="Placeholder text for the field")
    validations: Optional[ValidationRules] = Field(default=None, description="Validation rules for the field")
    options: Optional[List[Option]] = Field(default=None, description="Options for select-type fields")
    multi_select: bool = Field(default=False, description="Whether multiple selections are allowed") 