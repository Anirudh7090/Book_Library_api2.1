from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas.schemas import TokenData
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    print("get_current_user called")
    print(f"Token received: {token}")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print(f"Payload decoded: {payload}")
        email: str = payload.get("sub")
        role: str = payload.get("role")
        user_id: int = payload.get("id")  # Extract user id from token payload
        print(f"Email: {email}, Role: {role}, User ID: {user_id}")
        if email is None or role is None or user_id is None:
            print("Email, role, or id missing in token payload")
            raise credentials_exception
        token_data = TokenData(email=email, role=role, id=user_id)  # Set id here
        print(f"Token data prepared: {token_data}")
        return token_data
    except JWTError as e:
        print(f"JWTError occurred: {e}")
        raise credentials_exception
