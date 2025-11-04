class Usuario:
    """Representa o usuário do sistema (agora com ID e Saldo)."""
    def __init__(self, id, nome: str, email: str, saldo: float = 0.0):
        if not nome or not nome.strip():
            raise ValueError("O nome do usuário não pode ser vazio.")
        if not email or "@" not in email:
            raise ValueError("Email inválido.")
            
        self.id = id
        self.nome = nome
        self.email = email
        self.saldo = saldo

    def __str__(self):
        return f"Usuário: {self.nome} | Email: {self.email} | Saldo: R$ {self.saldo:.2f}"