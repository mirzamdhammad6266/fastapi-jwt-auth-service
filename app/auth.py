from datetime import datetime, timedelta
from typing import Optional, Dict

from jose import jwt, JWTError
from passlib.context import CryptContext

from .schemas import User, UserCreate, TokenData

# In a real system this would be a database table.
# Here we keep it deliberately simple for demo purposes.
_fake_users_db: Dict[str, User] = {}
_fake_password_hashes: Dict[str, str] = {}

SECRET_KEY = "change-me-in-production-very-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def register_user(payload: UserCreate) -> User:
    """
    Registers a new user in the in-memory store.

    Raises ValueError if the email is already taken.
    """
    if payload.email in _fake_users_db:
        raise ValueError("User with this email already exists.")

    user_id = len(_fake_users_db) + 1
    user = User(id=user_id, email=payload.email, is_active=True, role="user")

    _fake_users_db[payload.email] = user
    _fake_password_hashes[payload.email] = get_password_hash(payload.password)

    return user


def authenticate_user(email: str, password: str) -> Optional[User]:
    user = _fake_users_db.get(email)
    if not user:
        return None

    hashed = _fake_password_hashes.get(email)
    if not hashed or not verify_password(password, hashed):
        return None

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError("Token payload missing 'sub'")
        return TokenData(email=email)
    except JWTError as exc:
        raise JWTError("Could not validate credentials") from exc
