from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import List, Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Initialize the Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# FastAPI app instance
app = FastAPI()

# JWT Secret and Algorithm
SECRET_KEY = "EgZjaHJvbWUyBggAEEUYOTIKCAEQABiABBiiBDIKCAIQABiABBiiBNIBCTE5ODc1ajBqN6gCALACAA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy database for users
fake_users_db = {
    "users": {
        "username": "CnxApiUser5@.concentrix.com",
        "full_name": "Test User",
        "hashed_password": pwd_context.hash("cNx@9#T3St@xsw_E4"),
    }
}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get('users')
    if user and verify_password(password, user["hashed_password"]) and username == user['username']:
        return user
    return None

def create_access_token(data: dict):
    """
    Generate a JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """
    Decode a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verify the current user using the provided JWT token.
    """
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return username

# Pydantic models
class TextRequest(BaseModel):
    text: str
    entities: List[str] = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]
    language: str = "en"

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
async def login(request: LoginRequest):
    """
    Endpoint to issue a JWT token.
    """
    user = authenticate_user(request.username, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password - ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/analyze/", dependencies=[Depends(get_current_user)])
async def analyze_text(request: TextRequest):
    """
    Endpoint to detect PII in the provided text.
    """
    try:
        results = analyzer.analyze(
            text=request.text, entities=request.entities, language=request.language
        )
        detected_pii = [
            {"entity": result.entity_type, "value": result.text, "confidence": result.score}
            for result in results
        ]
        return {"detected_pii": detected_pii}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")

@app.post("/anonymize/", dependencies=[Depends(get_current_user)])
async def anonymize_text(request: TextRequest):
    """
    Endpoint to detect and anonymize PII in the provided text.
    """
    try:
        results = analyzer.analyze(
            text=request.text, entities=request.entities, language=request.language
        )
        anonymized_text = anonymizer.anonymize(
            text=request.text, analyzer_results=results
        )
        return {"anonymized_text": anonymized_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error anonymizing text: {str(e)}")
