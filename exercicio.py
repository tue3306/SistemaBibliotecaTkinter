import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import uuid
from tkinter import TclError

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("1200x900")
        self.root.configure(bg="#e8ecef")
        
        # Initialize database
        self.conn = sqlite3.connect("biblioteca.db")
        self.cursor = self.conn.cursor()
        self.criar_tabelas()
        
        # Configure modern style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=12, font=("Segoe UI", 12), background="#0288d1", foreground="#ffffff", borderwidth=0)
        self.style.map("TButton", background=[("active", "#01579b")])
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#e8ecef")
        self.style.configure("TEntry", padding=10, font=("Segoe UI", 12))
        self.style.configure("TCombobox", font=("Segoe UI", 12), padding=10)
        self.style.configure("Treeview", font=("Segoe UI", 11), rowheight=35, background="#ffffff", fieldbackground="#ffffff")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#0288d1", foreground="#ffffff")
        self.style.map("Treeview", background=[("selected", "#bbdefb")])
        self.style.configure("TLabelframe", font=("Segoe UI", 12, "bold"), background="#e8ecef")
        
        self.criar_interface()

    def criar_tabelas(self):
        """Cria as tabelas Autores e Livros no banco de dados SQLite, se não existirem."""
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
        """Configura a interface gráfica com rolagem e seções para autores, livros, busca e tabelas."""
        # Canvas for scrolling
        self.canvas = tk.Canvas(self.root, bg="#f5f6f5", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Main frame inside canvas
        self.main_frame = tk.Frame(self.canvas, bg="#e8ecef")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Update scroll region when main_frame size changes
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Header
        self.header_frame = tk.Frame(self.main_frame, bg="#0288d1", bd=0)
        self.header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(
            self.header_frame, 
            text="📚 Sistema de Gerenciamento de Biblioteca", 
            font=("Segoe UI", 24, "bold"), 
            bg="#0288d1", 
            fg="#ffffff",
            pady=15
        ).pack()

        # Authors section
        self.frame_autores = ttk.LabelFrame(self.main_frame, text="Cadastro de Autores", padding=20)
        self.frame_autores.pack(fill="x", pady=10, ipady=10)
        self.frame_autores.configure(borderwidth=2, relief="groove")

        tk.Label(self.frame_autores, text="Nome:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nome_autor = ttk.Entry(self.frame_autores)
        self.entry_nome_autor.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_nome_autor.bind("<FocusIn>", lambda e: self.show_tooltip(self.entry_nome_autor, "Digite o nome completo do autor"))
        
        tk.Label(self.frame_autores, text="Nacionalidade:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_nacionalidade = ttk.Entry(self.frame_autores)
        self.entry_nacionalidade.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_nacionalidade.bind("<FocusIn>", lambda e: self.show_tooltip(self.entry_nacionalidade, "Digite a nacionalidade do autor"))
        
        self.btn_adicionar_autor = ttk.Button(self.frame_autores, text="Adicionar Autor", command=self.adicionar_autor)
        self.btn_adicionar_autor.grid(row=2, column=0, columnspan=2, pady=15)
        self.btn_adicionar_autor.bind("<Enter>", lambda e: self.show_tooltip(self.btn_adicionar_autor, "Adiciona um novo autor ao banco de dados"))

        # Authors table section
        self.frame_tabela_autores = ttk.LabelFrame(self.main_frame, text="Autores Cadastrados", padding=20)
        self.frame_tabela_autores.pack(fill="x", pady=10, ipady=10)
        self.frame_tabela_autores.configure(borderwidth=2, relief="groove")

        self.tree_autores = ttk.Treeview(
            self.frame_tabela_autores, 
            columns=("ID", "Nome", "Nacionalidade"), 
            show="headings",
            height=4
        )
        self.tree_autores.heading("ID", text="ID")
        self.tree_autores.heading("Nome", text="Nome")
        self.tree_autores.heading("Nacionalidade", text="Nacionalidade")
        self.tree_autores.column("ID", width=50, anchor="center")
        self.tree_autores.column("Nome", width=300, anchor="w")
        self.tree_autores.column("Nacionalidade", width=200, anchor="w")
        self.tree_autores.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        scrollbar_autores = ttk.Scrollbar(self.frame_tabela_autores, orient="vertical", command=self.tree_autores.yview)
        scrollbar_autores.grid(row=0, column=2, sticky="ns")
        self.tree_autores.configure(yscrollcommand=scrollbar_autores.set)

        # Books section
        self.frame_livros = ttk.LabelFrame(self.main_frame, text="Cadastro de Livros", padding=20)
        self.frame_livros.pack(fill="x", pady=10, ipady=10)
        self.frame_livros.configure(borderwidth=2, relief="groove")

        tk.Label(self.frame_livros, text="Título:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_titulo = ttk.Entry(self.frame_livros)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_titulo.bind("<FocusIn>", lambda e: self.show_tooltip(self.entry_titulo, "Digite o título do livro"))
        
        tk.Label(self.frame_livros, text="Ano de Publicação:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_ano = ttk.Entry(self.frame_livros)
        self.entry_ano.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_ano.bind("<FocusIn>", lambda e: self.show_tooltip(self.entry_ano, "Digite o ano de publicação (ex.: 2023)"))
        
        tk.Label(self.frame_livros, text="Gênero:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_genero = ttk.Entry(self.frame_livros)
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.entry_genero.bind("<FocusIn>", lambda e: self.show_tooltip(self.entry_genero, "Digite o gênero do livro (ex.: Ficção, Sci-Fi)"))
        
        tk.Label(self.frame_livros, text="Autor:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.combo_autor = ttk.Combobox(self.frame_livros, state="readonly")
        self.combo_autor.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.combo_autor.bind("<FocusIn>", lambda e: self.show_tooltip(self.combo_autor, "Selecione o autor do livro"))
        
        self.btn_adicionar_livro = ttk.Button(self.frame_livros, text="Adicionar Livro", command=self.adicionar_livro)
        self.btn_adicionar_livro.grid(row=4, column=0, columnspan=2, pady=15)
        self.btn_adicionar_livro.bind("<Enter>", lambda e: self.show_tooltip(self.btn_adicionar_livro, "Adiciona um novo livro ao banco de dados"))

        # Search and filter section
        self.frame_busca = ttk.LabelFrame(self.main_frame, text="Busca e Filtros", padding=20)
        self.frame_busca.pack(fill="x", pady=10, ipady=10)
        self.frame_busca.configure(borderwidth=2, relief="groove")

        tk.Label(self.frame_busca, text="Buscar por Título:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_busca = ttk.Entry(self.frame_busca)
        self.entry_busca.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", self.buscar_livros)
        self.entry_busca.bind("<FocusIn>", lambda e: self.show_tooltip(self.entry_busca, "Digite parte do título para buscar livros"))
        
        tk.Label(self.frame_busca, text="Filtrar por Autor:", bg="#e8ecef", font=("Segoe UI", 12)).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.combo_filtro_autor = ttk.Combobox(self.frame_busca, state="readonly")
        self.combo_filtro_autor.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        self.combo_filtro_autor.bind("<<ComboboxSelected>>", self.filtrar_por_autor)
        self.combo_filtro_autor.bind("<FocusIn>", lambda e: self.show_tooltip(self.combo_filtro_autor, "Selecione um autor para filtrar os livros"))

        # Books table section
        self.frame_tabela = ttk.LabelFrame(self.main_frame, text="Livros Cadastrados", padding=20)
        self.frame_tabela.pack(fill="both", expand=True, pady=10)
        self.frame_tabela.configure(borderwidth=2, relief="groove")

        self.tree = ttk.Treeview(
            self.frame_tabela, 
            columns=("ID", "Título", "Ano", "Gênero", "Autor"), 
            show="headings",
            height=8
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.heading("Autor", text="Autor")
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Título", width=400, anchor="w")
        self.tree.column("Ano", width=120, anchor="center")
        self.tree.column("Gênero", width=180, anchor="w")
        self.tree.column("Autor", width=250, anchor="w")
        self.tree.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons below table
        btn_frame = tk.Frame(self.frame_tabela, bg="#e8ecef")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Editar Selecionado", command=self.editar_registro).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Excluir Selecionado", command=self.excluir_registro).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Limpar Filtros", command=self.atualizar_tabela).pack(side="left", padx=10)

        # Configure grid weights
        self.frame_tabela.grid_rowconfigure(0, weight=1)
        self.frame_tabela.grid_columnconfigure(0, weight=1)
        self.frame_tabela_autores.grid_rowconfigure(0, weight=1)
        self.frame_tabela_autores.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Initialize data
        self.atualizar_combo_autores()
        self.atualizar_tabela()
        self.atualizar_tabela_autores()

    def show_tooltip(self, widget, text):
        """Mostra uma dica flutuante (tooltip) ao focar em um widget."""
        try:
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 10))
            label.pack()
            widget.bind("<FocusOut>", lambda e: self.tooltip.destroy())
            widget.bind("<Leave>", lambda e: self.tooltip.destroy())
        except TclError:
            pass

    def atualizar_combo_autores(self):
        """Atualiza o Combobox de autores com os dados do banco e gerencia o estado do botão de adicionar livro."""
        self.cursor.execute("SELECT id_autor, nome FROM Autores")
        autores = self.cursor.fetchall()
        valores = [f"{autor[1]} (ID: {autor[0]})" for autor in autores]
        self.combo_autor["values"] = valores
        self.combo_filtro_autor["values"] = ["Todos"] + valores
        if valores:
            self.combo_autor.set("")  # Não seleciona autor por padrão
            self.combo_filtro_autor.set("Todos")
            self.btn_adicionar_livro.state(["!disabled"])
        else:
            self.combo_autor.set("")
            self.combo_filtro_autor.set("Todos")
            self.btn_adicionar_livro.state(["disabled"])
            messagebox.showwarning("Aviso", "Cadastre pelo menos um autor antes de adicionar livros.")

    def atualizar_tabela_autores(self):
        """Atualiza a tabela de autores com os dados do banco."""
        for item in self.tree_autores.get_children():
            self.tree_autores.delete(item)
        self.cursor.execute("SELECT id_autor, nome, nacionalidade FROM Autores")
        rows = self.cursor.fetchall()
        if not rows:
            self.tree_autores.insert("", tk.END, values=("", "Nenhum autor cadastrado", ""))
        else:
            for row in rows:
                self.tree_autores.insert("", tk.END, values=row)

    def adicionar_autor(self):
        """Adiciona um novo autor ao banco de dados."""
        try:
            nome = self.entry_nome_autor.get().strip()
            nacionalidade = self.entry_nacionalidade.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome do autor é obrigatório!")
                return
            if not nome.replace(" ", "").isalpha():
                messagebox.showerror("Erro", "O nome do autor deve conter apenas letras e espaços!")
                return
            self.cursor.execute("INSERT INTO Autores (nome, nacionalidade) VALUES (?, ?)", (nome, nacionalidade))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Autor adicionado com sucesso!")
            self.entry_nome_autor.delete(0, tk.END)
            self.entry_nacionalidade.delete(0, tk.END)
            self.atualizar_combo_autores()
            self.atualizar_tabela()
            self.atualizar_tabela_autores()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Erro ao adicionar autor. Verifique os dados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def adicionar_livro(self):
        """Adiciona um novo livro ao banco de dados, com validações adicionais."""
        try:
            titulo = self.entry_titulo.get().strip()
            ano = self.entry_ano.get().strip()
            genero = self.entry_genero.get().strip()
            autor_selecionado = self.combo_autor.get()
            
            # Validações
            if not all([titulo, ano, autor_selecionado]):
                messagebox.showerror("Erro", "Título, ano e autor são obrigatórios!")
                return
            try:
                ano = int(ano)
                if ano < 0 or ano > datetime.now().year:
                    messagebox.showerror("Erro", "Ano inválido! Deve estar entre 0 e o ano atual.")
                    return
            except ValueError:
                messagebox.showerror("Erro", "O ano deve ser um número válido!")
                return
            
            # Extrair ID do autor
            try:
                id_autor = int(autor_selecionado.split("ID: ")[1].replace(")", ""))
            except (IndexError, ValueError):
                messagebox.showerror("Erro", "Selecione um autor válido!")
                return
            
            # Verificar duplicidade
            self.cursor.execute("SELECT id_livro FROM Livros WHERE titulo = ? AND id_autor = ?", (titulo, id_autor))
            if self.cursor.fetchone():
                messagebox.showerror("Erro", "Este livro já está cadastrado para este autor!")
                return
            
            # Inserir livro
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
        """Atualiza a tabela de livros com filtros opcionais por autor ou título."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        query = """
            SELECT Livros.id_livro, Livros.titulo, Livros.ano_publicacao, Livros.genero, Autores.nome
            FROM Livros
            JOIN Autores ON Livros.id_autor = Autores.id_autor
        """
        params = []
        if filtro_autor and filtro_autor != "Todos":
            try:
                id_autor = int(filtro_autor.split("ID: ")[1].replace(")", ""))
                query += " WHERE Livros.id_autor = ?"
                params.append(id_autor)
            except (IndexError, ValueError):
                return
        if busca_titulo:
            if "WHERE" in query:
                query += " AND Livros.titulo LIKE ?"
            else:
                query += " WHERE Livros.titulo LIKE ?"
            params.append(f"%{busca_titulo}%")
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        if not rows:
            self.tree.insert("", tk.END, values=("", "Nenhum livro cadastrado", "", "", ""))
        else:
            for row in rows:
                self.tree.insert("", tk.END, values=row)

    def buscar_livros(self, event):
        """Filtra livros com base no título digitado."""
        busca_titulo = self.entry_busca.get().strip()
        filtro_autor = self.combo_filtro_autor.get()
        self.atualizar_tabela(filtro_autor, busca_titulo)

    def filtrar_por_autor(self, event):
        """Filtra livros com base no autor selecionado."""
        busca_titulo = self.entry_busca.get().strip()
        filtro_autor = self.combo_filtro_autor.get()
        self.atualizar_tabela(filtro_autor, busca_titulo)

    def editar_registro(self):
        """Abre uma janela para editar um livro selecionado."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um livro para editar!")
            return
        id_livro = self.tree.item(selecionado)["values"][0]
        if not id_livro:  # Caso seja a linha "Nenhum livro cadastrado"
            messagebox.showerror("Erro", "Nenhum livro válido selecionado!")
            return
        self.cursor.execute("SELECT titulo, ano_publicacao, genero, id_autor FROM Livros WHERE id_livro = ?", (id_livro,))
        livro = self.cursor.fetchone()
        
        # Create edit window
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Livro")
        janela_edicao.geometry("600x450")
        janela_edicao.configure(bg="#e8ecef")
        janela_edicao.resizable(False, False)
        
        frame_edicao = tk.Frame(janela_edicao, bg="#e8ecef", bd=2, relief="flat")
        frame_edicao.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame_edicao, text="Título:", bg="#e8ecef", font=("Segoe UI", 12)).pack(pady=10)
        entry_titulo = ttk.Entry(frame_edicao)
        entry_titulo.insert(0, livro[0])
        entry_titulo.pack(pady=5, padx=20, fill="x")
        
        tk.Label(frame_edicao, text="Ano de Publicação:", bg="#e8ecef", font=("Segoe UI", 12)).pack(pady=10)
        entry_ano = ttk.Entry(frame_edicao)
        entry_ano.insert(0, livro[1])
        entry_ano.pack(pady=5, padx=20, fill="x")
        
        tk.Label(frame_edicao, text="Gênero:", bg="#e8ecef", font=("Segoe UI", 12)).pack(pady=10)
        entry_genero = ttk.Entry(frame_edicao)
        entry_genero.insert(0, livro[2] or "")
        entry_genero.pack(pady=5, padx=20, fill="x")
        
        tk.Label(frame_edicao, text="Autor:", bg="#e8ecef", font=("Segoe UI", 12)).pack(pady=10)
        combo_autor = ttk.Combobox(frame_edicao, values=self.combo_autor["values"], state="readonly")
        self.cursor.execute("SELECT nome FROM Autores WHERE id_autor = ?", (livro[3],))
        autor_nome = self.cursor.fetchone()[0]
        combo_autor.set(f"{autor_nome} (ID: {livro[3]})")
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
                try:
                    id_autor = int(novo_autor.split("ID: ")[1].replace(")", ""))
                except (IndexError, ValueError):
                    messagebox.showerror("Erro", "Selecione um autor válido!")
                    return
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
        
        ttk.Button(frame_edicao, text="Salvar Alterações", command=salvar_edicao).pack(pady=20)

    def excluir_registro(self):
        """Exclui um livro selecionado após confirmação."""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um livro para excluir!")
            return
        id_livro = self.tree.item(selecionado)["values"][0]
        if not id_livro:  # Caso seja a linha "Nenhum livro cadastrado"
            messagebox.showerror("Erro", "Nenhum livro válido selecionado!")
            return
        if messagebox.askyesno("Confirmação", "Deseja excluir o livro selecionado?"):
            try:
                self.cursor.execute("DELETE FROM Livros WHERE id_livro = ?", (id_livro,))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def __del__(self):
        """Fecha a conexão com o banco de dados ao destruir o objeto."""
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
