from dataclasses import dataclass
from typing import Dict, Any, Tuple
from firebase_admin import auth
import firebase_admin
@dataclass
class AuthResult:
    success: bool
    user_id: str = None
    user_email: str = None
    response: Tuple[Dict[str, Any], int] = None

def authenticate(request) -> AuthResult:
    """Authenticate the request using Firebase ID token."""
    if 'Authorization' not in request.headers:
        return AuthResult(
            success=False,
            response=({'error': 'No authorization token provided'}, 401)
        )

    try:
        token = request.headers['Authorization'].split('Bearer ')[-1]
        decoded_token = auth.verify_id_token(token)
        project_id = firebase_admin.get_app().project_id

        if 'aud' not in decoded_token or decoded_token['aud'] != project_id:
            return AuthResult(
            success=False,
            response=({'error': 'Invalid token audience'}, 401)
            )
            
        return AuthResult(success=True, user_id=decoded_token['uid'], user_email=decoded_token['email'])
        
    except Exception as e:
        return AuthResult(
            success=False,
            response=({'error': f'Invalid token: {str(e)}'}, 401)
        )