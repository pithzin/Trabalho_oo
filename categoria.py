class Categoria:
    """Representa uma categoria para transações, como 'Alimentação' ou 'Salário'."""
    def __init__(self, nome: str):
        if not nome or not nome.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")
        self.nome = nome

    def __str__(self):
        return self.nome