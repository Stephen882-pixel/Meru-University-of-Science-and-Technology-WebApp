import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(developer):
    """
    Generate a JWT token for the given developer.
    """
    payload = {
        'developer_id': str(developer.developer_id),
        'email': developer.email,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow(),  # Issued at
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    """
    Decode a JWT token to validate it and retrieve payload.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")
    
def get_developer_id_from_token(token):
    
    try:
        payload = decode_jwt_token(token)  # Use the decode function you provided
        developer_id = payload.get('developer_id')
        if not developer_id:
            raise ValueError("developer_id not found in token payload.")
        return developer_id
    except ValueError as e:
        raise ValueError(f"Failed to extract developer_id: {str(e)}")

