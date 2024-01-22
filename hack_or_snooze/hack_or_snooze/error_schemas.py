from ninja import Schema


# Generic output schema for error message JSON returned by API routes:

class Unauthorized(Schema):
    detail: str


class BadRequest(Schema):
    detail: str


class ObjectNotFound(Schema):
    detail: str
