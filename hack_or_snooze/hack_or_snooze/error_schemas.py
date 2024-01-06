from ninja import Schema


class Unauthorized(Schema):
    error: str


class BadRequest(Schema):
    error: str
