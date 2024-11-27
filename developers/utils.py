from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
import uuid
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

def generate_jwt_token(developer):
    token = AccessToken()
    token['token_type'] = 'access'
    token['jti'] = str(uuid.uuid4())
    token['user_id'] = str(developer.developer_id)  # Use developer_id
    token['email'] = developer.email
    token.set_exp(lifetime=timedelta(hours=24))  # Set 24 hours expiration time
    return token

def get_developer_id_from_token(token):
    try:
        access_token = AccessToken(token)
        access_token.check_exp()  # Will raise exception if expired
        developer_id = access_token['user_id']
        if not developer_id:
            raise ValueError("No developer_id found in token")
        return developer_id
    except TokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")
    except InvalidToken as e:
        raise ValueError(f"Invalid token: {str(e)}")
