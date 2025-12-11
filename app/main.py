from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import auth
from .schemas import User, UserCreate, Token, TokenData

app = FastAPI(
    title="FastAPI JWT Auth Service",
    description="Demo authentication API with register, login, JWT, and a protected /me endpoint.",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    """
    Create a new user with a hashed password.
    This implementation uses an in-memory store just for demo purposes.
    """
    try:
        user = auth.register_user(payload)
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT access token.
    """
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency that decodes the JWT token and returns the current user.
    """
    try:
        token_data: TokenData = auth.decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth._fake_users_db.get(token_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


@app.get("/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)):
    """
    Protected endpoint that returns the authenticated user's profile.
    """
    return current_user
