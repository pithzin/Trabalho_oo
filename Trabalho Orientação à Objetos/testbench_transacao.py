from transacao import Transacao, Categoria
from datetime import date

print("--- Iniciando Testes da Classe Transacao ---")

# --- Teste 1: Cenário de Sucesso (Despesa) ---
print("\n[Teste 1] Criando uma transação de despesa válida...")
try:
    cat_alimentacao = Categoria("Alimentação")
    despesa = Transacao(descricao="Almoço no restaurante", valor=35.50, categoria=cat_alimentacao, tipo="Despesa")
    print(f"  SUCESSO! Transação criada: {despesa}")
except (ValueError, TypeError) as e:
    print(f"  FALHA! Erro inesperado: {e}")

# --- Teste 2: Cenário de Falha (Valor Inválido) ---
print("\n[Teste 2] Tentando criar transação com valor negativo...")
try:
    cat_lazer = Categoria("Lazer")
    transacao_falha = Transacao(descricao="Cinema", valor=-50.00, categoria=cat_lazer, tipo="Despesa")
    print(f"  FALHA! Transação foi criada indevidamente: {transacao_falha}")
except ValueError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")

# --- Teste 3: Cenário de Falha (Tipo Inválido) ---
print("\n[Teste 3] Tentando criar transação com tipo inválido...")
try:
    cat_outros = Categoria("Outros")
    transacao_falha_2 = Transacao(descricao="Presente", valor=100, categoria=cat_outros, tipo="Gasto")
    print(f"  FALHA! Transação foi criada indevidamente: {transacao_falha_2}")
except ValueError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")

# --- Teste 4: Cenário de Falha (Categoria Inválida) ---
print("\n[Teste 4] Tentando criar transação com objeto de categoria inválido...")
try:
    transacao_falha_3 = Transacao(descricao="Feira", valor=80.0, categoria="Compras", tipo="Despesa")
    print(f"  FALHA! Transação foi criada indevidamente: {transacao_falha_3}")
except TypeError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")


print("\n--- Fim dos Testes da Classe Transacao ---")