from categoria import Categoria

print("--- Iniciando Testes da Classe Categoria ---")

# --- Teste 1: Instanciação com nome válido ---
print("\n[Teste 1] Criando categoria com nome válido...")
try:
    cat1 = Categoria("Alimentação")
    print(f"  SUCESSO! Categoria criada: '{cat1}'")
except ValueError as e:
    print(f"  FALHA! Erro inesperado: {e}")

# --- Teste 2: Instanciação com nome vazio ---
print("\n[Teste 2] Tentando criar categoria com nome vazio...")
try:
    cat2 = Categoria("")
    print(f"  FALHA! Categoria foi criada indevidamente: '{cat2}'")
except ValueError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")

# --- Teste 3: Instanciação com nome contendo apenas espaços ---
print("\n[Teste 3] Tentando criar categoria com nome contendo apenas espaços...")
try:
    cat3 = Categoria("   ")
    print(f"  FALHA! Categoria foi criada indevidamente: '{cat3}'")
except ValueError as e:
    print(f"  SUCESSO! Erro esperado capturado: {e}")


print("\n--- Fim dos Testes da Classe Categoria ---")