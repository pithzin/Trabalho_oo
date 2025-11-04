from transacao import Transacao

class Conta:
    """Gerencia as transações e o saldo de um usuário."""
    def __init__(self):
        self.saldo = 0.0
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)
        if transacao.tipo == "Receita":
            self.saldo += transacao.valor
        elif transacao.tipo == "Despesa":
            self.saldo -= transacao.valor

    def gerar_extrato(self):
        print("--- Extrato da Conta ---")
        if not self.transacoes:
            print("Nenhuma transação registrada.")
        else:
            for t in self.transacoes:
                print(t)
        print("------------------------")
        print(f"Saldo Final: R$ {self.saldo:.2f}")