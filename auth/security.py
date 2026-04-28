from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration for JWT authentication
SECRET_KEY = "zmien-na-losowy-ciag-znakow-w-produkcji"  # Security warning: Change this to a secure random string in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password hashing context using the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Generates a secure hash from a plaintext password"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Validates a plaintext password against its stored hash"""
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    """Generates a signed JWT access token with an expiration timestamp"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    """Decodes and validates a JWT token using the secret key and algorithm"""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])