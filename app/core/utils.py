from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.schemas.token import DataToken


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

        return encoded_jwt

    @staticmethod
    def verify_token_access(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

            id: str = payload.get("user_id")

            if id is None:
                raise credentials_exception
            token_data = DataToken(id=id)
        except JWTError as e:
            print(e)
            raise credentials_exception

        return token_data
