from ninja import Schema


class Unauthorized(Schema):
    detail: str


class BadRequest(Schema):
    detail: str
