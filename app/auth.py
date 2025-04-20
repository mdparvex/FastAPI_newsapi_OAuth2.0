from fastapi import Depends, HTTPException, status, Form, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowClientCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import base64
from jose import ExpiredSignatureError
from app.config import SECRET_KEY, ALGORITHM, CLIENT_ID, CLIENT_SECRET

router = APIRouter()
oauth2_scheme = OAuth2(
    flows=OAuthFlowsModel(
        clientCredentials=OAuthFlowClientCredentials(tokenUrl="/token")
    )
)

def authenticate_client(client_id: str, client_secret: str):
    return client_id == CLIENT_ID and client_secret == CLIENT_SECRET

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as e:
        print("JWT decode error:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/token")
async def login(request: Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        client_id, client_secret = decoded.split(":", 1)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid basic auth encoding")

    if not authenticate_client(client_id, client_secret):
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    token = create_access_token({"client_id": client_id})
    return {"access_token": token, "token_type": "bearer"}
