from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Self

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr

from easyssp_utils.models.client_localized_message import ClientLocalizedMessage


class LocalizedErrorMessage(BaseModel):
    """
    LocalizedErrorMessage
    """
    code: StrictInt | None = None
    message: StrictStr | None = None
    details: StrictStr | None = None
    localized_message: ClientLocalizedMessage | None = Field(default=None, alias="localizedMessage")
    __properties: ClassVar[list[str]] = ["code", "message", "details", "localizedMessage"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> Self | None:
        """Create an instance of LocalizedErrorMessage from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with the value `None`
          are ignored.
        """
        excluded_fields: set[str] = set({})

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of localized_message
        if self.localized_message:
            _dict["localizedMessage"] = self.localized_message.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict[str, Any] | None) -> Self | None:
        """Create an instance of LocalizedErrorMessage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "code": obj.get("code"),
            "message": obj.get("message"),
            "details": obj.get("details"),
            "localizedMessage": ClientLocalizedMessage.from_dict(obj["localizedMessage"]) if obj.get(
                "localizedMessage") is not None else None
        })
        return _obj
