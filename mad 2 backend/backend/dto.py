class Response:
    def __init__(self, message, data=None):
        self.message = message
        self.data = data

    def serialize(self):
        return {
            'message' : self.message,
            'data' : self.data
        }
    
class ErrorResponse(Response):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors
    
    def serialize(self):
        return {
            'message' : self.message,
            'errors' : self.errors
        }