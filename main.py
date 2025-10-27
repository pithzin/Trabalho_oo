import os
from datetime import date
from time import sleep

from categoria import Categoria
from transacao import Transacao
from conta import Conta
from usuario import Usuario

usuario_principal = None
categorias_disponiveis = []


def limpar_tela():
    """Limpa o console para uma melhor experiência de usuário."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    """Pausa a execução e espera o usuário pressionar Enter."""
    input("\nPressione Enter para continuar...")


def criar_novo_usuario():
    """Solicita os dados do usuário e cria o objeto principal."""
    global usuario_principal
    limpar_tela()
    print("--- Bem-vindo ao Sistema de Finanças Pessoais ---")
    print("Para começar, por favor, crie seu perfil de usuário.\n")
    
    nome_usuario = ""
    email_usuario = ""

    while True:
        nome_usuario = input("Digite seu nome: ").strip()
        try:
            if not nome_usuario:
                 raise ValueError("O nome do usuário não pode ser vazio.")
            break
        except ValueError as e:
            print(f"Erro: {e}")

    while True:
        email_usuario = input("Digite seu e-mail: ").strip()
        try:
            if not email_usuario or "@" not in email_usuario:
                raise ValueError("Email inválido.")
            break
        except ValueError as e:
            print(f"Erro: {e}")

    try:
        usuario_principal = Usuario(nome=nome_usuario, email=email_usuario)
        print(f"\nUsuário '{usuario_principal.nome}' criado com sucesso!")
        print("Carregando sistema...")
        sleep(2)
    except ValueError as e:
        print(f"Erro inesperado ao criar usuário: {e}")
        exit()



def _obter_valor_valido():
    """Loop para garantir que o usuário insira um valor numérico positivo."""
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
    """Loop para garantir que o tipo seja 'Receita' ou 'Despesa'."""
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
    """Exibe as categorias e permite ao usuário escolher uma."""
    if not categorias_disponiveis:
        return None 

    print("\nEscolha uma categoria:")
    for i, cat in enumerate(categorias_disponiveis):
        print(f"  [{i+1}] {cat.nome}")
    
    while True:
        try:
            escolha = int(input("Número da categoria: "))
            if 1 <= escolha <= len(categorias_disponiveis):
                return categorias_disponiveis[escolha - 1]
            else:
                print("Erro: Número fora do intervalo.")
        except ValueError:
            print("Erro: Digite um número.")

def adicionar_transacao():
    """Fluxo completo para adicionar uma nova transação."""
    limpar_tela()
    print("--- Adicionar Nova Transação ---")

    if not categorias_disponiveis:
        print("Erro: Você precisa cadastrar pelo menos uma categoria antes de adicionar uma transação.")
        print("Por favor, vá ao menu 'Gerenciar Categorias'.")
        return

    descricao = input("Digite a descrição: ")
    valor = _obter_valor_valido()
    tipo = _obter_tipo_valido()
    categoria = _escolher_categoria()

    try:
        nova_transacao = Transacao(descricao=descricao, 
                                   valor=valor, 
                                   categoria=categoria, 
                                   tipo=tipo)
        
        usuario_principal.conta.adicionar_transacao(nova_transacao)
        
        print(f"\nSucesso! Transação '{descricao}' registrada.")
        print(f"Novo saldo da conta: R$ {usuario_principal.conta.saldo:.2f}")
    
    except (ValueError, TypeError) as e:
        print(f"\nErro ao criar transação: {e}")

def ver_extrato():
    """Exibe o extrato da conta do usuário."""
    limpar_tela()
    usuario_principal.conta.gerar_extrato()

def _adicionar_nova_categoria():
    """Função interna para adicionar uma categoria à lista global."""
    print("\n--- Adicionar Nova Categoria ---")
    nome_categoria = input("Digite o nome da nova categoria (ex: Lazer): ")
    try:
        nova_cat = Categoria(nome_categoria)
        categorias_disponiveis.append(nova_cat)
        print(f"Sucesso! Categoria '{nome_categoria}' adicionada.")
    except ValueError as e:
        print(f"Erro: {e}")

def _listar_categorias():
    """Função interna para listar as categorias cadastradas."""
    print("\n--- Categorias Cadastradas ---")
    if not categorias_disponiveis:
        print("Nenhuma categoria cadastrada.")
    else:
        for cat in categorias_disponiveis:
            print(f"- {cat.nome}")

def gerenciar_categorias():
    """Exibe o sub-menu de gerenciamento de categorias."""
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

def carregar_categorias_padrao():
    """Carrega uma lista inicial de categorias na memória."""
    cat1 = Categoria("Salário")
    cat2 = Categoria("Alimentação")
    cat3 = Categoria("Moradia")
    cat4 = Categoria("Transporte")
    
    categorias_disponiveis.extend([cat1, cat2, cat3, cat4])
    

def main():
    """Função principal que executa o loop do menu."""
    
    criar_novo_usuario()
    
    carregar_categorias_padrao()
    
    while True:
        limpar_tela()
        print(f"--- Sistema de Finanças Pessoais ---")
        print(f"Usuário: {usuario_principal.nome} ({usuario_principal.email})")
        print(f"Saldo Atual: R$ {usuario_principal.conta.saldo:.2f}\n")
        
        print("Menu Principal:")
        print("[1] Adicionar nova transação")
        print("[2] Ver extrato financeiro")
        print("[3] Gerenciar categorias")
        print("[0] Sair do sistema")
        
        opcao = input("\nEscolha sua opção: ")
        
        if opcao == '1':
            adicionar_transacao()
            pausar_tela()
        elif opcao == '2':
            ver_extrato()
            pausar_tela()
        elif opcao == '3':
            gerenciar_categorias()
        elif opcao == '0':
            print(f"\nObrigado por usar o sistema, {usuario_principal.nome}. Até logo!")
            sleep(2)
            break
        else:
            print("Opção inválida! Tente novamente.")
            sleep(1)
if __name__ == "__main__":
    main()