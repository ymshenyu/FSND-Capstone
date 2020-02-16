import json
from jose import jwt
from flask import request, _request_ctx_stack
from functools import wraps
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-9dxdz39b.auth0.com'
API_AUDIENCE = 'fsnd-capstone'
ALGORITHMS = ["RS256"]

# Auth error handler


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer"
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                "code": "token_expired",
                "description": "token is expired"
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                "code": "invalid_claims",
                "description":
                "incorrect claims, please check the audience and issuer"
            }, 401)
        except Exception:
            raise AuthError({
                "code": "invalid_header",
                "description": "Unable to parse authentication token."
            }, 401)
    else:
        raise AuthError({
            "code": "invalid_header",
            "description": "Unable to find appropriate key"
        }, 401)


def check_permission(permission, payload):
    permissions = payload['permissions']

    if not permissions:
        raise AuthError({
            "code": "invalid_header",
            "description": "Unable to find permissions header"
        }, 403)
    if permission not in permissions:
        raise AuthError({
            "code": "permission_denied",
            "description": "Permission denied"
        }, 403)

    return True


def require_permission(permission=''):
    def require_permission_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permission(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return require_permission_decorator
