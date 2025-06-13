import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Autores (
                id_autor INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nacionalidade TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Livros (
                id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                ano_publicacao INTEGER,
                genero TEXT,
                id_autor INTEGER,
                FOREIGN KEY (id_autor) REFERENCES Autores(id_autor)
            )
        """)
        self.conn.commit()

    def adicionar_autor(self, nome, nacionalidade):
        if not nome.replace(" ", "").isalpha():
            raise ValueError("Nome do autor deve conter apenas letras e espaços!")
        if nacionalidade and not nacionalidade.replace(" ", "").isalpha():
            raise ValueError("Nacionalidade deve conter apenas letras e espaços!")
        self.cursor.execute("INSERT INTO Autores (nome, nacionalidade) VALUES (?, ?)", (nome, nacionalidade))
        self.conn.commit()

    def adicionar_livro(self, titulo, ano, genero, id_autor):
        if not titulo or not ano or not id_autor:
            raise ValueError("Título, ano e autor são obrigatórios!")
        ano = int(ano)
        if ano < 0 or ano > datetime.now().year:
            raise ValueError("Ano inválido!")
        self.cursor.execute("SELECT id_livro FROM Livros WHERE titulo = ? AND id_autor = ?", (titulo, id_autor))
        if self.cursor.fetchone():
            raise ValueError("Livro já cadastrado para este autor!")
        self.cursor.execute(
            "INSERT INTO Livros (titulo, ano_publicacao, genero, id_autor) VALUES (?, ?, ?, ?)",
            (titulo, ano, genero, id_autor)
        )
        self.conn.commit()

    def listar_autores(self):
        self.cursor.execute("SELECT id_autor, nome, nacionalidade FROM Autores")
        return self.cursor.fetchall()

    def listar_livros(self, filtro_autor=None, busca_titulo=None):
        query = """
            SELECT Livros.id_livro, Livros.titulo, Livros.ano_publicacao, Livros.genero, Autores.nome
            FROM Livros
            JOIN Autores ON Livros.id_autor = Autores.id_autor
        """
        params = []
        if filtro_autor and filtro_autor != "Todos":
            id_autor = int(filtro_autor.split("ID: ")[1].replace(")", ""))
            query += " WHERE Livros.id_autor = ?"
            params.append(id_autor)
        if busca_titulo:
            if "WHERE" in query:
                query += " AND Livros.titulo LIKE ?"
            else:
                query += " WHERE Livros.titulo LIKE ?"
            params.append(f"%{busca_titulo}%")
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def atualizar_livro(self, id_livro, titulo, ano, genero, id_autor):
        self.cursor.execute(
            "UPDATE Livros SET titulo = ?, ano_publicacao = ?, genero = ?, id_autor = ? WHERE id_livro = ?",
            (titulo, ano, genero, id_autor, id_livro)
        )
        self.conn.commit()

    def atualizar_autor(self, id_autor, nome, nacionalidade):
        self.cursor.execute(
            "UPDATE Autores SET nome = ?, nacionalidade = ? WHERE id_autor = ?",
            (nome, nacionalidade, id_autor)
        )
        self.conn.commit()

    def excluir_livro(self, id_livro):
        self.cursor.execute("DELETE FROM Livros WHERE id_livro = ?", (id_livro,))
        self.conn.commit()

    def excluir_autor(self, id_autor):
        self.cursor.execute("SELECT id_livro FROM Livros WHERE id_autor = ?", (id_autor,))
        if self.cursor.fetchone():
            raise ValueError("Não é possível excluir autor com livros associados!")
        self.cursor.execute("DELETE FROM Autores WHERE id_autor = ?", (id_autor,))
        self.conn.commit()

    def get_autor_by_id(self, id_autor):
        self.cursor.execute("SELECT nome FROM Autores WHERE id_autor = ?", (id_autor,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()