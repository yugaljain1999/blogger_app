from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # tokenUrl is the url from where fastapi fetch access token

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't verify credentials", headers={"WWW-Authenticate":"Bearer"})

    # verify token
    token_data = tokens.verify_token(token, credentials_exception)

    # return current user
    return token_data


