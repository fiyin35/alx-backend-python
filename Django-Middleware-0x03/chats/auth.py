from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom class if you need to extend JWT authentication later.
    """
    def authenticate(self, request):
        return super().authenticate(request)
