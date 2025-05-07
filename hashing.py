from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class Hash():
    def bcrypt(password: str):
        hash_pass = pwd_context.hash(password)
        return hash_pass

    def verify(plain_pass, hash_pass):
        return pwd_context.verify(plain_pass, hash_pass)

