"""Defines Pydantic models for structured LLM responses."""

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from .types import ActionType


class LLMCommandResponse(BaseModel):
    """Schema for structured responses from the LLM for command execution."""

    action_type: ActionType = Field(
        ..., description="The type of action the LLM wants to perform."
    )
    commands: list[str] | None = Field(
        None,
        description=(
            "List of command parts (arguments) for kubectl, *excluding* the initial"
            " command verb (e.g., get, create). Required if action_type is COMMAND"
            " and no yaml_manifest is provided."
        ),
    )
    yaml_manifest: str | None = Field(
        None,
        description=(
            "YAML manifest content as a string. Used when action_type is COMMAND and"
            " requires a manifest (e.g., for kubectl create -f -). Can be combined"
            " with 'commands' for flags like '-n'."
        ),
    )
    explanation: str | None = Field(
        None, description="Textual explanation or feedback from the LLM."
    )
    error: str | None = Field(
        None,
        description=(
            "Error message if the LLM encountered an issue or refused the request."
            " Required if action_type is ERROR."
        ),
    )
    wait_duration_seconds: int | None = Field(
        None,
        description="Duration in seconds to wait. Required if action_type is WAIT.",
    )
    # TODO: Consider adding a validator for allowed_exit_codes to ensure unique entries,
    # though unclear if non-unique entries should cause outright rejection.
    allowed_exit_codes: list[int] | None = Field(
        None,
        description=(
            "List of allowed exit codes for the planned command. If not provided, "
            "the system may use a default (e.g., [0]) or infer based on the "
            "command verb in specific contexts."
        ),
    )

    @field_validator("commands", mode="before")
    @classmethod
    def check_commands(
        cls, v: list[str] | None, info: ValidationInfo
    ) -> list[str] | None:
        """Validate commands field based on action_type."""
        if "action_type" in info.data:
            action_type_str = info.data["action_type"]
            try:
                action_type = ActionType(action_type_str)
                # For COMMAND, either commands or yaml_manifest must be present.
                yaml_manifest = info.data.get("yaml_manifest")
                if action_type == ActionType.COMMAND and not v and not yaml_manifest:
                    raise ValueError(
                        "Either 'commands' or 'yaml_manifest' is required when"
                        " action_type is COMMAND"
                    )
            except ValueError as e:
                # Handle cases where action_type itself is invalid
                if "action_type" in str(e):
                    raise ValueError(
                        f"Invalid action_type provided: {action_type_str}"
                    ) from e
                # Re-raise validation errors from the check
                raise e
        return v

    @field_validator("error", mode="before")
    @classmethod
    def check_error(cls, v: str | None, info: ValidationInfo) -> str | None:
        """Validate error field based on action_type."""
        if "action_type" in info.data:
            action_type_str = info.data["action_type"]
            try:
                action_type = ActionType(action_type_str)
                if action_type == ActionType.ERROR and not v:
                    raise ValueError("error is required when action_type is ERROR")
            except ValueError as e:
                raise ValueError(
                    f"Invalid action_type provided: {action_type_str}"
                ) from e
        return v

    @field_validator("wait_duration_seconds", mode="before")
    @classmethod
    def check_wait_duration(cls, v: int | None, info: ValidationInfo) -> int | None:
        """Validate wait_duration_seconds field based on action_type."""
        if "action_type" in info.data:
            action_type_str = info.data["action_type"]
            try:
                action_type = ActionType(action_type_str)
                if action_type == ActionType.WAIT and v is None:
                    raise ValueError(
                        "wait_duration_seconds is required when action_type is WAIT"
                    )
            except ValueError as e:
                raise ValueError(
                    f"Invalid action_type provided: {action_type_str}"
                ) from e
        return v

    model_config = {
        "use_enum_values": True,
        "extra": "ignore",
    }


class ApplyFileScopeResponse(BaseModel):
    """Schema for LLM response when scoping files for kubectl apply."""

    file_selectors: list[str] = Field(
        ...,
        description=(
            "List of file paths, directory paths, or glob patterns identified for "
            "kubectl apply."
        ),
    )
    remaining_request_context: str = Field(
        ...,
        description=(
            "The remaining part of the user's request that is not related to file "
            "selection."
        ),
    )


class LLMFinalApplyPlanResponse(BaseModel):
    """Schema for LLM response containing the final list of planned apply commands."""

    planned_commands: list[LLMCommandResponse] = Field(
        ...,
        description=(
            "A list of LLMCommandResponse objects, each representing a kubectl "
            "command to be executed."
        ),
    )

    model_config = {
        "use_enum_values": True,
        "extra": "forbid",  # Forbid extra fields to ensure strict adherence
    }


# TODO: Add PromptFragment model for typed prompt construction
