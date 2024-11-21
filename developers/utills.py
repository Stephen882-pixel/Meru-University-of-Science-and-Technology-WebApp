from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings
from datetime import datetime, timedelta
import jwt
import uuid
import logging

logger = logging.getLogger(__name__)

class TokenService:
    @staticmethod
    def generate_token(developer):
        """
        Generate a JWT token with all required claims for Simple JWT
        """
        try:
            # Create a token with required Simple JWT claims
            payload = {
                # Required Simple JWT claims
                'token_type': 'access',
                'jti': str(uuid.uuid4()),  # JWT ID - Required by Simple JWT
                'user_id': str(developer.user.id) if hasattr(developer, 'user') else None,  # Required by Simple JWT
                
                # Custom claims
                'developer_id': str(developer.developer_id),
                'email': developer.email,
                
                # Timing claims
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow(),
                'nbf': datetime.utcnow(),  # Not valid before
            }
            
            # Add type verification
            payload['type'] = 'access'
            
            token = jwt.encode(
                payload,
                settings.JWT_SECRET,
                algorithm=settings.JWT_ALGORITHM
            )
            
            # Verify the token can be decoded
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            logger.info(f"Token generated successfully for developer: {developer.email}")
            return token
            
        except Exception as e:
            logger.error(f"Token generation failed: {str(e)}")
            raise

    @staticmethod
    def generate_token_using_refresh_token(developer):
        """
        Alternative method using Simple JWT's RefreshToken
        """
        try:
            refresh = RefreshToken()
            
            # Set the claims
            refresh['developer_id'] = str(developer.developer_id)
            refresh['email'] = developer.email
            refresh['user_id'] = str(developer.user.id) if hasattr(developer, 'user') else None
            
            # Get the access token
            access_token = refresh.access_token
            
            return str(access_token)
            
        except Exception as e:
            logger.error(f"Token generation failed using refresh token: {str(e)}")
            raise

    @staticmethod
    def validate_token(token):
        """
        Validate a JWT token and return the payload
        """
        try:
            # Try Simple JWT validation
            access_token = AccessToken(token)
            return {
                'valid': True,
                'payload': access_token.payload,
                'validation_method': 'simple_jwt'
            }
        except TokenError as e:
            logger.warning(f"Token validation failed: {str(e)}")
            raise ValueError(str(e))

    @staticmethod
    def debug_token(token):
        """
        Debug a token by attempting multiple validation methods
        """
        debug_info = {
            'token_format': None,
            'header_decode': None,
            'payload_decode': None,
            'signature_valid': None,
            'token_expired': None,
            'errors': [],
            'missing_claims': []
        }
        
        required_claims = ['token_type', 'jti', 'user_id']
        
        try:
            # Decode without verification
            payload = jwt.decode(token, options={"verify_signature": False})
            debug_info['payload_decode'] = payload
            
            # Check for missing required claims
            for claim in required_claims:
                if claim not in payload:
                    debug_info['missing_claims'].append(claim)
            
            # Try full verification
            try:
                jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
                debug_info['signature_valid'] = True
            except jwt.ExpiredSignatureError:
                debug_info['token_expired'] = True
                debug_info['errors'].append("Token has expired")
            except Exception as e:
                debug_info['errors'].append(f"Validation error: {str(e)}")
                
        except Exception as e:
            debug_info['errors'].append(f"Debug error: {str(e)}")
            
        return debug_info