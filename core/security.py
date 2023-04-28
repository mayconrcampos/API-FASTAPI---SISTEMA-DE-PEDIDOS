from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated="auto")


def validar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função que valida senha digitada pelo usuário em texto puro e a compara com a senha hasheada do DB.
    """
    return CRYPTO.verify(senha, hash_senha)

def generate_password_hash(senha: str) -> str:
    """
    Gera Hash e retorna seu valor
    """
    return CRYPTO.hash(senha)