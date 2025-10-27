from conta import Conta
from transacao import Transacao
from categoria import Categoria

print("--- Iniciando Testes da Classe Conta ---")

# --- Teste 1: Adicionar transações e verificar saldo ---
print("\n[Teste 1] Adicionando receita e despesa para verificar o saldo...")
try:
    conta_teste = Conta()
    print(f"  Saldo inicial: R$ {conta_teste.saldo:.2f}")

    cat_salario = Categoria("Salário")
    receita = Transacao("Pagamento mensal", 3000.00, cat_salario, "Receita")
    conta_teste.adicionar_transacao(receita)
    print(f"  Após receita de R$ {receita.valor:.2f}, Saldo: R$ {conta_teste.saldo:.2f}")

    cat_moradia = Categoria("Moradia")
    despesa = Transacao("Aluguel", 1200.00, cat_moradia, "Despesa")
    conta_teste.adicionar_transacao(despesa)
    print(f"  Após despesa de R$ {despesa.valor:.2f}, Saldo: R$ {conta_teste.saldo:.2f}")

    # Verificação final
    saldo_esperado = 1800.00
    if abs(conta_teste.saldo - saldo_esperado) < 0.01: # Comparação de float
         print(f"  SUCESSO! Saldo final de R$ {conta_teste.saldo:.2f} é o esperado.")
    else:
         print(f"  FALHA! Saldo final é R$ {conta_teste.saldo:.2f}, mas era esperado R$ {saldo_esperado:.2f}.")

except Exception as e:
    print(f"  FALHA! Ocorreu um erro inesperado: {e}")


# --- Teste 2: Gerar extrato ---
print("\n[Teste 2] Gerando extrato da conta...")
try:
    conta_extrato = Conta()
    cat_freelance = Categoria("Freelance")
    cat_transporte = Categoria("Transporte")

    t1 = Transacao("Projeto Website", 500, cat_freelance, "Receita")
    t2 = Transacao("Gasolina", 150, cat_transporte, "Despesa")
    conta_extrato.adicionar_transacao(t1)
    conta_extrato.adicionar_transacao(t2)

    conta_extrato.gerar_extrato()
    print("  SUCESSO! Extrato gerado acima.")

except Exception as e:
     print(f"  FALHA! Ocorreu um erro ao gerar o extrato: {e}")

print("\n--- Fim dos Testes da Classe Conta ---")