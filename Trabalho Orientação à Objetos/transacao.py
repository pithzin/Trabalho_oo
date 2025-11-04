from datetime import date
from categoria import Categoria

class Transacao:
    """Representa uma transação financeira (agora com ID)."""
    def __init__(self, id, descricao: str, valor: float, tipo: str, categoria: Categoria, data_transacao: date = date.today()):
        if not descricao or not descricao.strip():
            raise ValueError("A descrição não pode ser vazia.")
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("O valor deve ser um número positivo.")
        if tipo not in ["Receita", "Despesa"]:
            raise ValueError("O tipo da transação deve ser 'Receita' ou 'Despesa'.")
        if not isinstance(categoria, Categoria):
             raise TypeError("A categoria deve ser um objeto da classe Categoria.")

        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.data = data_transacao
        self.categoria = categoria
        self.tipo = tipo

    def __str__(self):
        sinal = "+" if self.tipo == "Receita" else "-"
        return f"{self.data} | {self.descricao} ({self.categoria.nome}): {sinal}R$ {self.valor:.2f}"