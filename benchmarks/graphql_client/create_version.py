# Generated by ariadne-codegen
# Source: queries.graphql

from typing import Any, Optional

from .base_model import BaseModel


class CreateVersion(BaseModel):
    insert_versions_one: Optional["CreateVersionInsertVersionsOne"]


class CreateVersionInsertVersionsOne(BaseModel):
    id: Any
