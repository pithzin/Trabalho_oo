import os
import database as db  # Importa nosso módulo de banco de dados
from time import sleep

# --- Funções Auxiliares de Interface ---

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    input("\nPressione Enter para continuar...")

# --- Funções de Fluxo ---

def login_ou_criar_usuario():
    """Gerencia o login ou criação de um novo usuário."""
    limpar_tela()
    print("--- Bem-vindo ao Sistema de Finanças Pessoais ---")
    
    while True:
        email = input("Digite seu e-mail para login ou cadastro: ").strip()
        if not email or "@" not in email:
            print("Por favor, digite um e-mail válido.")
            continue

        usuario_logado = db.buscar_usuario_por_email(email)
        
        if usuario_logado:
            print(f"\nBem-vindo(a) de volta, {usuario_logado.nome}!")
            sleep(2)
            return usuario_logado
        else:
            print("\nE-mail não encontrado. Vamos criar um novo cadastro.")
            nome = ""
            while not nome:
                nome = input("Digite seu nome completo: ").strip()
                if not nome:
                    print("O nome não pode ser vazio.")
            
            novo_usuario = db.criar_usuario(nome, email)
            if novo_usuario:
                print(f"Usuário '{novo_usuario.nome}' criado com sucesso!")
                sleep(2)
                return novo_usuario
            else:
                print("Não foi possível criar o usuário. Tente novamente.")
                # O loop continuará


# --- Funções do Menu ---

def _obter_valor_valido():
    while True:
        try:
            valor_str = input("Digite o valor (ex: 50.75): R$ ")
            valor = float(valor_str)
            if valor <= 0:
                print("Erro: O valor deve ser positivo.")
            else:
                return valor
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número.")

def _obter_tipo_valido():
    while True:
        print("Qual o tipo? [1] Receita | [2] Despesa")
        tipo_str = input("Escolha: ")
        if tipo_str == '1':
            return "Receita"
        elif tipo_str == '2':
            return "Despesa"
        else:
            print("Erro: Opção inválida.")

def _escolher_categoria():
    """Busca categorias do BDD e permite ao usuário escolher uma."""
    categorias = db.buscar_categorias() # Busca do banco
    if not categorias:
        return None 
    
    print("\nEscolha uma categoria:")
    for i, cat in enumerate(categorias):
        print(f"  [{i+1}] {cat.nome}")
    
    while True:
        try:
            escolha = int(input("Número da categoria: "))
            if 1 <= escolha <= len(categorias):
                return categorias[escolha - 1] # Retorna o objeto Categoria
            else:
                print("Erro: Número fora do intervalo.")
        except ValueError:
            print("Erro: Digite um número.")

def adicionar_transacao(usuario_logado):
    limpar_tela()
    print("--- Adicionar Nova Transação ---")

    descricao = input("Digite a descrição: ")
    valor = _obter_valor_valido()
    tipo = _obter_tipo_valido()
    
    categoria_escolhida = _escolher_categoria()
    if not categoria_escolhida:
        print("Erro: Nenhuma categoria encontrada. Crie uma no menu 'Gerenciar Categorias'.")
        return

    # Chama a função do BDD para criar a transação e atualizar o saldo
    sucesso = db.criar_transacao(
        descricao=descricao,
        valor=valor,
        tipo=tipo,
        id_categoria=categoria_escolhida.id,
        id_usuario=usuario_logado.id
    )
    
    if sucesso:
        print(f"\nSucesso! Transação '{descricao}' registrada.")
        # Busca o usuário novamente para obter o saldo atualizado
        usuario_logado = db.buscar_usuario_por_id(usuario_logado.id)
    else:
        print("\nFalha ao registrar a transação.")
    
    return usuario_logado # Retorna o objeto usuário atualizado

def ver_extrato(usuario_logado):
    limpar_tela()
    print("--- Extrato da Conta ---")
    print(f"Saldo Atual: R$ {usuario_logado.saldo:.2f}")
    print("-" * 30)
    
    transacoes = db.buscar_transacoes_por_usuario(usuario_logado.id)
    
    if not transacoes:
        print("Nenhuma transação registrada.")
    else:
        for t in transacoes:
            print(t) # O método __str__ da Transacao faz a formatação

    print("-" * 30)

def _adicionar_nova_categoria():
    print("\n--- Adicionar Nova Categoria ---")
    nome_categoria = input("Digite o nome da nova categoria (ex: Lazer): ")
    nova_cat = db.criar_categoria(nome_categoria)
    if nova_cat:
        print(f"Sucesso! Categoria '{nova_cat.nome}' adicionada.")
    else:
        print("Erro ao adicionar categoria (talvez já exista).")

def _listar_categorias():
    print("\n--- Categorias Cadastradas ---")
    categorias = db.buscar_categorias()
    if not categorias:
        print("Nenhuma categoria cadastrada.")
    else:
        for cat in categorias:
            print(f"- {cat.nome}")

def gerenciar_categorias():
    while True:
        limpar_tela()
        print("--- Gerenciar Categorias ---")
        print("[1] Adicionar nova categoria")
        print("[2] Listar categorias cadastradas")
        print("[0] Voltar ao menu principal")
        
        opcao_cat = input("\nEscolha sua opção: ")

        if opcao_cat == '1':
            _adicionar_nova_categoria()
            pausar_tela()
        elif opcao_cat == '2':
            _listar_categorias()
            pausar_tela()
        elif opcao_cat == '0':
            break
        else:
            print("Opção inválida!")
            sleep(1)

def main():
    # 1. Garante que o BDD e as tabelas existam
    db.criar_tabelas()
    
    # 2. Força o login ou criação do usuário
    usuario_logado = login_ou_criar_usuario()
    
    # 3. Inicia o loop do menu principal
    while True:
        limpar_tela()
        print(f"--- Sistema de Finanças Pessoais ---")
        print(f"Usuário: {usuario_logado.nome} ({usuario_logado.email})")
        # O saldo é atualizado a cada loop para refletir a realidade
        print(f"Saldo Atual: R$ {usuario_logado.saldo:.2f}\n")
        
        print("Menu Principal:")
        print("[1] Adicionar nova transação")
        print("[2] Ver extrato financeiro")
        print("[3] Gerenciar categorias")
        print("[0] Sair do sistema")
        
        opcao = input("\nEscolha sua opção: ")
        
        if opcao == '1':
            # Atualiza o objeto usuario_logado com o novo saldo
            usuario_logado = adicionar_transacao(usuario_logado)
            pausar_tela()
        elif opcao == '2':
            ver_extrato(usuario_logado)
            pausar_tela()
        elif opcao == '3':
            gerenciar_categorias()
        elif opcao == '0':
            print(f"\nObrigado por usar o sistema, {usuario_logado.nome}. Até logo!")
            sleep(2)
            break
        else:
            print("Opção inválida! Tente novamente.")
            sleep(1)

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    main()