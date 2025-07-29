from jose import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError
import base64
import json
KEYCLOAK_URL = "http://localhost:8090"
REALM = "master"
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"
AUDIENCE = "account"  # as per your token
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6IjhjMzkwNzFkLWZlYmItNDY2MS05NmU4LTY1YjhiZGU4YWNhOCJ9.eyJleHAiOjE3NDcyOTU0OTksImlhdCI6MTc0NzI5MTg5OSwiYXV0aF90aW1lIjoxNzQ3MjkwNjkxLCJqdGkiOiI5MGMzYTllZS02NTY2LTQ4ZDUtODc0Ni1hNmIxOTM4NmYwNmEiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwOTAvcmVhbG1zL21hc3RlciIsImF1ZCI6WyJtYXN0ZXItcmVhbG0iLCJhY2NvdW50Il0sInN1YiI6IjIzNzBhZDc1LWQyOTEtNDcyNy04NzE2LTdhYjgwNTBkZTUxMSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImhvYW5nIiwic2Vzc2lvbl9zdGF0ZSI6ImM2YjQyZjAzLWM4Y2ItNDkyZi05NmRkLTVjYmE0ODY2OTkyNyIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiY3JlYXRlLXJlYWxtIiwiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsImFkbWluIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJtYXN0ZXItcmVhbG0iOnsicm9sZXMiOlsidmlldy1yZWFsbSIsInZpZXctaWRlbnRpdHktcHJvdmlkZXJzIiwibWFuYWdlLWlkZW50aXR5LXByb3ZpZGVycyIsImltcGVyc29uYXRpb24iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIGhvYW5nc2NvcGUgcHJvZmlsZSIsInNpZCI6ImM2YjQyZjAzLWM4Y2ItNDkyZi05NmRkLTVjYmE0ODY2OTkyNyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4ifQ.cv6QLvFuZYO1q4NcWcRxeCSZHxea5FxNNS1juWFNgs2H-lXyk5f-g6R7QEzvW-GebM74hOWQgg8Wlc0NX3bDpA"  # Replace with your access token

shared_secret = "Ei2QyjxxvYSl1yi1lUL3RwxNRqiQVFI8".strip()
def get_jwt_header(token: str) -> dict:
    header_b64 = token.split('.')[0]
    header_b64 += '=' * (-len(header_b64) % 4)  # pad base64 if needed
    decoded = base64.urlsafe_b64decode(header_b64)
    return json.loads(decoded)

try:
    header = get_jwt_header(token)
    alg = header.get("alg")
    kid = header.get("kid")

    if alg == "HS512":
        payload = jwt.decode(
            token,
            shared_secret,
            algorithms=["HS512"],
            options={"verify_aud": False}
        )
        print(payload)
    elif alg == "RS256" or "ES256":
        jwk_client = PyJWKClient(JWKS_URL)
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=None,  # Accept all supported algorithms
            issuer=ISSUER,
            audience=AUDIENCE  # Optional: include if you expect it
        )

    print(" Token is valid. Payload:")
except InvalidTokenError as e:
    print(f" Invalid token: {e}")
def extract_roles(payload):
    try:
        return payload['realm_access']['roles']
    except KeyError:
        return []

