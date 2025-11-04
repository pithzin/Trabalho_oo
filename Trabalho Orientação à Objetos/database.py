import sqlite3
from datetime import date

# Importa nossos modelos
from usuario import Usuario
from categoria import Categoria
from transacao import Transacao

DB_FILE = "financas.db"

def conectar():
    """Cria uma conexão com o banco de dados SQLite."""
    try:
        con = sqlite3.connect(DB_FILE)
        # Permite que os resultados da consulta sejam acessados pelos nomes das colunas
        con.row_factory = sqlite3.Row
        return con
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas():
    """Cria as tabelas do banco se elas não existirem."""
    with conectar() as con:
        try:
            con.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    saldo REAL NOT NULL DEFAULT 0.0
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    valor REAL NOT NULL,
                    tipo TEXT NOT NULL, -- 'Receita' ou 'Despesa'
                    data DATE NOT NULL,
                    id_usuario INTEGER NOT NULL,
                    id_categoria INTEGER NOT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
                    FOREIGN KEY (id_categoria) REFERENCES categorias(id)
                )
            """)
            con.commit()
            # Inserir categorias padrão se não existirem
            _inserir_categorias_padrao(con)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

def _inserir_categorias_padrao(con):
    """Insere categorias iniciais no banco (apenas se estiverem vazias)."""
    categorias_padrao = ["Salário", "Alimentação", "Moradia", "Transporte", "Lazer"]
    try:
        # Verifica se já existem categorias
        cursor = con.execute("SELECT COUNT(*) FROM categorias")
        if cursor.fetchone()[0] == 0:
            for cat in categorias_padrao:
                con.execute("INSERT INTO categorias (nome) VALUES (?)", (cat,))
            con.commit()
    except sqlite3.Error as e:
        # Ignora erro de UNIQUE caso tente inserir duplicata
        if "UNIQUE constraint failed" not in str(e):
            print(f"Erro ao inserir categorias padrão: {e}")


# --- Funções de Usuário ---

def buscar_usuario_por_email(email):
    """Busca um usuário pelo email e retorna um objeto Usuario."""
    with conectar() as con:
        cursor = con.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            # Instancia o objeto Usuario com os dados do BDD
            return Usuario(id=row['id'], nome=row['nome'], email=row['email'], saldo=row['saldo'])
        return None

def criar_usuario(nome, email):
    """Cria um novo usuário e retorna um objeto Usuario."""
    try:
        # Validação do modelo (embora o BDD já tenha 'NOT NULL')
        novo_usuario = Usuario(id=None, nome=nome, email=email, saldo=0.0) 
        with conectar() as con:
            cursor = con.execute(
                "INSERT INTO usuarios (nome, email, saldo) VALUES (?, ?, ?)",
                (novo_usuario.nome, novo_usuario.email, novo_usuario.saldo)
            )
            con.commit()
            novo_usuario.id = cursor.lastrowid # Pega o ID gerado pelo BDD
            return novo_usuario
    except (ValueError, sqlite3.Error) as e:
        print(f"Erro ao criar usuário: {e}")
        return None

# --- Funções de Categoria ---

def buscar_categorias():
    """Retorna uma lista de objetos Categoria do banco."""
    with conectar() as con:
        cursor = con.execute("SELECT * FROM categorias ORDER BY nome")
        rows = cursor.fetchall()
        return [Categoria(id=row['id'], nome=row['nome']) for row in rows]

def criar_categoria(nome):
    """Cria uma nova categoria e retorna um objeto Categoria."""
    try:
        # Validação do modelo
        nova_categoria = Categoria(id=None, nome=nome)
        with conectar() as con:
            cursor = con.execute("INSERT INTO categorias (nome) VALUES (?)", (nova_categoria.nome,))
            con.commit()
            nova_categoria.id = cursor.lastrowid
            return nova_categoria
    except (ValueError, sqlite3.Error) as e:
        print(f"Erro ao criar categoria: {e}")
        return None

# --- Funções de Transação ---

def criar_transacao(descricao, valor, tipo, id_categoria, id_usuario):
    """
    Cria uma nova transação e ATUALIZA o saldo do usuário.
    Esta é a função mais importante (Lógica de Negócio).
    """
    try:
        # 1. Valida os dados usando o modelo
        # (Passamos uma categoria 'dummy' para o construtor validar)
        transacao_valida = Transacao(
            id=None, 
            descricao=descricao, 
            valor=valor, 
            tipo=tipo, 
            categoria=Categoria(id=id_categoria, nome="validação"), # Apenas para validação
            data_transacao=date.today()
        )
        
        with conectar() as con:
            # Usamos transação do BDD para garantir atomicidade
            cursor = con.cursor()
            try:
                # 2. Insere a nova transação
                cursor.execute(
                    "INSERT INTO transacoes (descricao, valor, tipo, data, id_usuario, id_categoria) VALUES (?, ?, ?, ?, ?, ?)",
                    (transacao_valida.descricao, transacao_valida.valor, transacao_valida.tipo, transacao_valida.data, id_usuario, id_categoria)
                )
                
                # 3. Calcula o valor a ser atualizado no saldo
                valor_atualizar = transacao_valida.valor if tipo == "Receita" else -transacao_valida.valor
                
                # 4. Atualiza o saldo do usuário
                cursor.execute(
                    "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?",
                    (valor_atualizar, id_usuario)
                )
                con.commit() # Confirma a transação
                return True
                
            except sqlite3.Error as e:
                con.rollback() # Desfaz tudo se der erro
                print(f"Erro ao salvar transação: {e}")
                return False

    except ValueError as e:
        print(f"Erro de validação: {e}")
        return False

def buscar_transacoes_por_usuario(id_usuario):
    """
    Busca todas as transações de um usuário, fazendo JOIN com categorias.
    """
    with conectar() as con:
        # Usamos JOIN para trazer o nome da categoria
        query = """
            SELECT t.id, t.descricao, t.valor, t.tipo, t.data, c.nome as categoria_nome
            FROM transacoes t
            JOIN categorias c ON t.id_categoria = c.id
            WHERE t.id_usuario = ?
            ORDER BY t.data DESC, t.id DESC
        """
        cursor = con.execute(query, (id_usuario,))
        rows = cursor.fetchall()
        
        # Monta os objetos Transacao com os dados do BDD
        transacoes = []
        for row in rows:
            cat_obj = Categoria(id=None, nome=row['categoria_nome']) # ID da cat não é relevante aqui
            trans_obj = Transacao(
                id=row['id'],
                descricao=row['descricao'],
                valor=row['valor'],
                tipo=row['tipo'],
                categoria=cat_obj,
                data_transacao=date.fromisoformat(row['data'])
            )
            transacoes.append(trans_obj)
        return transacoes

def buscar_usuario_por_id(id_usuario):
    """Busca um usuário pelo ID e retorna um objeto Usuario atualizado."""
    with conectar() as con:
        cursor = con.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
        row = cursor.fetchone()
        if row:
            return Usuario(id=row['id'], nome=row['nome'], email=row['email'], saldo=row['saldo'])
        return None