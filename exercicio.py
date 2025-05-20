import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("950x750")
        self.root.configure(bg="#e6ecf0")
        
        self.conn = sqlite3.connect("biblioteca.db")
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=10, font=("Helvetica", 11), background="#3498db", foreground="#ffffff")
        self.style.map("TButton", background=[("active", "#2980b9")])
        self.style.configure("TLabel", font=("Helvetica", 11), background="#e6ecf0")
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#3498db", foreground="#ffffff")
        self.style.configure("TCombobox", font=("Helvetica", 11))
        
        self.criar_interface()

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

    def criar_interface(self):
        self.main_frame = tk.Frame(self.root, bg="#e6ecf0")
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.header_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(
            self.header_frame, 
            text="📚 Sistema de Gerenciamento de Biblioteca", 
            font=("Helvetica", 18, "bold"), 
            bg="#2c3e50", 
            fg="#ffffff",
            pady=15
        ).pack()

        self.frame_autores = ttk.LabelFrame(self.main_frame, text="Cadastro de Autores", padding=15)
        self.frame_autores.pack(fill="x", pady=10)
        tk.Label(self.frame_autores, text="Nome:", bg="#e6ecf0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_nome_autor = ttk.Entry(self.frame_autores)
        self.entry_nome_autor.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        tk.Label(self.frame_autores, text="Nacionalidade:", bg="#e6ecf0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_nacionalidade = ttk.Entry(self.frame_autores)
        self.entry_nacionalidade.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(self.frame_autores, text="Adicionar Autor").grid(row=2, column=0, columnspan=2, pady=10)

        self.frame_livros = ttk.LabelFrame(self.main_frame, text="Cadastro de Livros", padding=15)
        self.frame_livros.pack(fill="x", pady=10)
        tk.Label(self.frame_livros, text="Título:", bg="#e6ecf0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_titulo = ttk.Entry(self.frame_livros)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        tk.Label(self.frame_livros, text="Ano de Publicação:", bg="#e6ecf0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_ano = ttk.Entry(self.frame_livros)
        self.entry_ano.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        tk.Label(self.frame_livros, text="Gênero:", bg="#e6ecf0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_genero = ttk.Entry(self.frame_livros)
        self.entry_genero.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        tk.Label(self.frame_livros, text="Autor:", bg="#e6ecf0").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.combo_autor = ttk.Combobox(self.frame_livros)
        self.combo_autor.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(self.frame_livros, text="Adicionar Livro", command=self.adicionar_livro).grid(row=4, column=0, columnspan=2, pady=10)

        self.frame_busca = ttk.LabelFrame(self.main_frame, text="Busca e Filtros", padding=15)
        self.frame_busca.pack(fill="x", pady=10)
        tk.Label(self.frame_busca, text="Buscar por Título:", bg="#e6ecf0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_busca = ttk.Entry(self.frame_busca)
        self.entry_busca.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", self.buscar_livros)
        tk.Label(self.frame_busca, text="Filtrar por Autor:", bg="#e6ecf0").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.combo_filtro_autor = ttk.Combobox(self.frame_busca)
        self.combo_filtro_autor.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        self.combo_filtro_autor.bind("<<ComboboxSelected>>", self.filtrar_por_autor)

        self.frame_tabela = ttk.LabelFrame(self.main_frame, text="Livros Cadastrados", padding=15)
        self.frame_tabela.pack(fill="both", expand=True, pady=10)
        self.tree = ttk.Treeview(
            self.frame_tabela, 
            columns=("ID", "Título", "Ano", "Gênero", "Autor"), 
            show="headings",
            height=12
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.heading("Autor", text="Autor")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Título", width=350, anchor="w")
        self.tree.column("Ano", width=100, anchor="center")
        self.tree.column("Gênero", width=150, anchor="w")
        self.tree.column("Autor", width=200, anchor="w")
        self.tree.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self.frame_tabela, bg="#e6ecf0")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Editar Selecionado", command=self.editar_registro).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir Selecionado", command=self.excluir_registro).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpar Filtros", command=self.atualizar_tabela).pack(side="left", padx=5)

        self.frame_tabela.grid_rowconfigure(0, weight=1)
        self.frame_tabela.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.atualizar_combo_autores()
        self.atualizar_tabela()

    def atualizar_combo_autores(self):
        self.cursor.execute("SELECT id_autor, nome FROM Autores")
        autores = self.cursor.fetchall()
        valores = [f"{autor[1]} (ID: {autor[0]})" for autor in autores]
        self.combo_autor["values"] = valores
        self.combo_filtro_autor["values"] = ["Todos"] + valores

    def adicionar_autor(self):
        try:
            nome = self.entry_nome_autor.get().strip()
            nacionalidade = self.entry_nacionalidade.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome do autor é obrigatório!")
                return
            self.cursor.execute("INSERT INTO Autores (nome, nacionalidade) VALUES (?, ?)", (nome, nacionalidade))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Autor adicionado com sucesso!")
            self.entry_nome_autor.delete(0, tk.END)
            self.entry_nacionalidade.delete(0, tk.END)
            self.atualizar_combo_autores()
            self.atualizar_tabela()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Erro ao adicionar autor. Verifique os dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def adicionar_livro(self):
        try:
            titulo = self.entry_titulo.get().strip()
            ano = self.entry_ano.get().strip()
            genero = self.entry_genero.get().strip()
            autor_selecionado = self.combo_autor.get()
            if not all([titulo, ano, autor_selecionado]):
                messagebox.showerror("Erro", "Título, ano e autor são obrigatórios!")
                return
            try:
                ano = int(ano)
                if ano < 0 or ano > datetime.now().year:
                    messagebox.showerror("Erro", "Ano inválido!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "O ano deve ser um número válido!")
                return
            id_autor = int(autor_selecionado.split("ID: ")[1].replace(")", ""))
            self.cursor.execute(
                "INSERT INTO Livros (titulo, ano_publicacao, genero, id_autor) VALUES (?, ?, ?, ?)",
                (titulo, ano, genero, id_autor)
            )
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
            self.entry_titulo.delete(0, tk.END)
            self.entry_ano.delete(0, tk.END)
            self.entry_genero.delete(0, tk.END)
            self.combo_autor.set("")
            self.atualizar_tabela()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Erro ao adicionar livro. Verifique se o autor existe.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def atualizar_tabela(self, filtro_autor=None, busca_titulo=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
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
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def buscar_livros(self, event):
        busca_titulo = self.entry_busca.get().strip()
        filtro_autor = self.combo_filtro_autor.get()
        self.atualizar_tabela(filtro_autor, busca_titulo)

    def filtrar_por_autor(self, event):
        busca_titulo = self.entry_busca.get().strip()
        filtro_autor = self.combo_filtro_autor.get()
        self.atualizar_tabela(filtro_autor, busca_titulo)

    def editar_registro(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um livro para editar!")
            return
        id_livro = self.tree.item(selecionado)["values"][0]
        self.cursor.execute("SELECT titulo, ano_publicacao, genero, id_autor FROM Livros WHERE id_livro = ?", (id_livro,))
        livro = self.cursor.fetchone()
        
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Livro")
        janela_edicao.geometry("450x350")
        janela_edicao.configure(bg="#e6ecf0")
        
        tk.Label(janela_edicao, text="Título:", bg="#e6ecf0", font=("Helvetica", 11)).pack(pady=10)
        entry_titulo = ttk.Entry(janela_edicao)
        entry_titulo.insert(0, livro[0])
        entry_titulo.pack(pady=5, padx=20, fill="x")
        
        tk.Label(janela_edicao, text="Ano de Publicação:", bg="#e6ecf0", font=("Helvetica", 11)).pack(pady=10)
        entry_ano = ttk.Entry(janela_edicao)
        entry_ano.insert(0, livro[1])
        entry_ano.pack(pady=5, padx=20, fill="x")
        
        tk.Label(janela_edicao, text="Gênero:", bg="#e6ecf0", font=("Helvetica", 11)).pack(pady=10)
        entry_genero = ttk.Entry(janela_edicao)
        entry_genero.insert(0, livro[2] or "")
        entry_genero.pack(pady=5, padx=20, fill="x")
        
        tk.Label(janela_edicao, text="Autor:", bg="#e6ecf0", font=("Helvetica", 11)).pack(pady=10)
        combo_autor = ttk.Combobox(janela_edicao, values=self.combo_autor["values"])
        combo_autor.pack(pady=5, padx=20, fill="x")
        
        def salvar_edicao():
            try:
                novo_titulo = entry_titulo.get().strip()
                novo_ano = entry_ano.get().strip()
                novo_genero = entry_genero.get().strip()
                novo_autor = combo_autor.get()
                if not all([novo_titulo, novo_ano, novo_autor]):
                    messagebox.showerror("Erro", "Título, ano e autor são obrigatórios!")
                    return
                try:
                    novo_ano = int(novo_ano)
                    if novo_ano < 0 or novo_ano > datetime.now().year:
                        messagebox.showerror("Erro", "Ano inválido!")
                        return
                except ValueError:
                    messagebox.showerror("Erro", "O ano deve ser um número válido!")
                    return
                id_autor = int(novo_autor.split("ID: ")[1].replace(")", ""))
                self.cursor.execute(
                    "UPDATE Livros SET titulo = ?, ano_publicacao = ?, genero = ?, id_autor = ? WHERE id_livro = ?",
                    (novo_titulo, novo_ano, novo_genero, id_autor, id_livro)
                )
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
                janela_edicao.destroy()
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        
        ttk.Button(janela_edicao, text="Salvar Alterações", command=salvar_edicao).pack(pady=20)

    def excluir_registro(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um livro para excluir!")
            return
        if messagebox.askyesno("Confirmação", "Deseja excluir o livro selecionado?"):
            try:
                id_livro = self.tree.item(selecionado)["values"][0]
                self.cursor.execute("DELETE FROM Livros WHERE id_livro = ?", (id_livro,))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()