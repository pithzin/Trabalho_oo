from conta import Conta

class Usuario:
    """Representa o usuário do sistema."""
    def __init__(self, nome: str, email: str):
        if not nome or not nome.strip():
            raise ValueError("O nome do usuário não pode ser vazio.")
        if not email or "@" not in email:
            raise ValueError("Email inválido.")
        self.nome = nome
        self.email = email
        self.conta = Conta() # Cada usuário é criado com uma nova conta

    def __str__(self):
        return f"Usuário: {self.nome} | Email: {self.email}"