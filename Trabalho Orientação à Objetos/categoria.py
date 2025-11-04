class Categoria:
    """Representa uma categoria para transações (agora com ID)."""
    def __init__(self, id, nome: str):
        if not nome or not nome.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")
        self.id = id
        self.nome = nome

    def __str__(self):
        return self.nome