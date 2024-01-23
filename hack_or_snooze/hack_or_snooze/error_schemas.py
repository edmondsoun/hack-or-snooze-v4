from ninja import Schema


class Unauthorized(Schema):
    detail: str


class BadRequest(Schema):
    detail: str


class ObjectNotFound(Schema):
    detail: str
