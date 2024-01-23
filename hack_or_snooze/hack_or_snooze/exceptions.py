class InvalidUsernameException(Exception):
    """Exception for invalid username."""

    def __init__(self,message):
        self.message = message

    def __str__(self):
        return self.message


# class EmptyPatchRequestException(Exception):
#     """Exception for empty patch requests."""

#     def __init__(self,message):
#         self.message = message

#     def __str__(self):
#         return self.message