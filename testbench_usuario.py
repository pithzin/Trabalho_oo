from usuario import Usuario
from transacao import Transacao
from categoria import Categoria

print("--- Iniciando Testes da Classe Usuario ---")

# --- Teste 1: Instanciação de usuário válido ---
print("\n[Teste 1] Criando um usuário válido...")
try:
    user1 = Usuario(nome="Ana Silva", email="ana.silva@example.com")
    print(f"  SUCESSO! Usuário criado: {user1}")
    print(f"  Saldo inicial da conta do usuário: R$ {user1.conta.saldo:.2f}")
except ValueError as e:
    print(f"  FALHA! Ocorreu um erro inesperado: {e}")

# --- Teste 2: Instanciação com nome inválido ---
print("\n[Teste 2] Tentando criar usuário com nome vazio...")
try:
    user_falha = Usuario(nome="", email="teste@example.com")
    print(f"  FALHA! Usuário foi criado indevidamente: {user_falha}")
except ValueError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")

# --- Teste 3: Instanciação com email inválido ---
print("\n[Teste 3] Tentando criar usuário com email sem '@'...")
try:
    user_falha_2 = Usuario(nome="Carlos", email="carlos.example.com")
    print(f"  FALHA! Usuário foi criado indevidamente: {user_falha_2}")
except ValueError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")


# --- Teste 4: Interação do usuário com sua conta ---
print("\n[Teste 4] Usuário realizando transações em sua conta...")
try:
    user2 = Usuario(nome="Beto Costa", email="beto@email.com")
    print(f"  Usuário '{user2.nome}' criado com saldo inicial R$ {user2.conta.saldo:.2f}")

    cat_invest = Categoria("Investimentos")
    receita_invest = Transacao("Dividendos", 250.00, cat_invest, "Receita")
    user2.conta.adicionar_transacao(receita_invest)
    print(f"  '{user2.nome}' adicionou uma receita. Novo saldo: R$ {user2.conta.saldo:.2f}")

    if user2.conta.saldo == 250.00:
        print("  SUCESSO! A conta do usuário foi atualizada corretamente.")
    else:
        print("  FALHA! O saldo da conta do usuário está incorreto.")

except Exception as e:
    print(f"  FALHA! Ocorreu um erro inesperado: {e}")


print("\n--- Fim dos Testes da Classe Usuario ---")