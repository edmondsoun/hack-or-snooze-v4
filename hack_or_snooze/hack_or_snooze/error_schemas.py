from ninja import Schema


# Generic output schema for error message JSON returned by API routes:

class BadRequest(Schema):
    """Schema for 400 Bad Request response."""

    detail: str


class Unauthorized(Schema):
    """Schema for 401 Unauthorized response."""

    detail: str


class ObjectNotFound(Schema):
    """Schema for 404 Not Found response."""

    detail: str
