import tkinter as tk
from tkinter import ttk, messagebox
from database.db import Database

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("1200x900")
        self.root.configure(bg="#e8ecef")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.db = Database()
        self.setup_style()
        self.criar_interface()

    def setup_style(self):
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

    def criar_interface(self):
        self.canvas = tk.Canvas(self.root, bg="#f5f6f5", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.main_frame = tk.Frame(self.canvas, bg="#e8ecef", width=1180)
        self.canvas_frame = self.canvas.create_window((600, 0), window=self.main_frame, anchor="n")
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        header_frame = tk.Frame(self.main_frame, bg="#0288d1", bd=0)
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="📚 Sistema de Gerenciamento de Biblioteca", font=("Segoe UI", 24, "bold"), bg="#0288d1", fg="#ffffff", pady=15).pack()
        self.frame_autores = ttk.LabelFrame(self.main_frame, text="Cadastro de Autores", padding=20)
        self.frame_autores.pack(fill="x", pady=10, ipady=10, padx=10)
        tk.Label(self.frame_autores, text="Nome:", bg="#e8ecef").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nome_autor = ttk.Entry(self.frame_autores)
        self.entry_nome_autor.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        tk.Label(self.frame_autores, text="Nacionalidade:", bg="#e8ecef").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_nacionalidade = ttk.Entry(self.frame_autores)
        self.entry_nacionalidade.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ttk.Button(self.frame_autores, text="Adicionar Autor", command=self.adicionar_autor).grid(row=2, column=0, columnspan=2, pady=15)
        self.frame_tabela_autores = ttk.LabelFrame(self.main_frame, text="Autores Cadastrados", padding=20)
        self.frame_tabela_autores.pack(fill="x", pady=10, ipady=10, padx=10)
        self.tree_autores = ttk.Treeview(self.frame_tabela_autores, columns=("ID", "Nome", "Nacionalidade"), show="headings", height=4)
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
        self.frame_livros = ttk.LabelFrame(self.main_frame, text="Cadastro de Livros", padding=20)
        self.frame_livros.pack(fill="x", pady=10, ipady=10, padx=10)
        tk.Label(self.frame_livros, text="Título:", bg="#e8ecef").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_titulo = ttk.Entry(self.frame_livros)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        tk.Label(self.frame_livros, text="Ano de Publicação:", bg="#e8ecef").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_ano = ttk.Entry(self.frame_livros)
        self.entry_ano.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        tk.Label(self.frame_livros, text="Gênero:", bg="#e8ecef").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_genero = ttk.Entry(self.frame_livros)
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        tk.Label(self.frame_livros, text="Autor:", bg="#e8ecef").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.combo_autor = ttk.Combobox(self.frame_livros, state="readonly")
        self.combo_autor.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.btn_adicionar_livro = ttk.Button(self.frame_livros, text="Adicionar Livro", command=self.adicionar_livro)
        self.btn_adicionar_livro.grid(row=4, column=0, columnspan=2, pady=15)
        self.frame_busca = ttk.LabelFrame(self.main_frame, text="Busca e Filtros", padding=20)
        self.frame_busca.pack(fill="x", pady=10, ipady=10, padx=10)
        tk.Label(self.frame_busca, text="Buscar por Título:", bg="#e8ecef").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_busca = ttk.Entry(self.frame_busca)
        self.entry_busca.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_busca.bind("<KeyRelease>", self.buscar_livros)
        tk.Label(self.frame_busca, text="Filtrar por Autor:", bg="#e8ecef").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.combo_filtro_autor = ttk.Combobox(self.frame_busca, state="readonly")
        self.combo_filtro_autor.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        self.combo_filtro_autor.bind("<<ComboboxSelected>>", self.filtrar_por_autor)
        self.frame_tabela = ttk.LabelFrame(self.main_frame, text="Livros Cadastrados", padding=20)
        self.frame_tabela.pack(fill="both", expand=True, pady=10, padx=10)
        self.tree = ttk.Treeview(self.frame_tabela, columns=("ID", "Título", "Ano", "Gênero", "Autor"), show="headings", height=8)
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
        btn_frame = tk.Frame(self.frame_tabela, bg="#e8ecef")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Editar Livro", command=self.editar_livro).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Editar Autor", command=self.editar_autor).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Excluir Livro", command=self.excluir_livro).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Excluir Autor", command=self.excluir_autor).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Limpar Filtros", command=self.atualizar_tabela).pack(side="left", padx=10)
        self.frame_tabela.grid_rowconfigure(0, weight=1)
        self.frame_tabela.grid_columnconfigure(0, weight=1)
        self.frame_tabela_autores.grid_rowconfigure(0, weight=1)
        self.frame_tabela_autores.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(5, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.atualizar_combo_autores()
        self.atualizar_tabela()
        self.atualizar_tabela_autores()

    def atualizar_combo_autores(self):
        autores = self.db.listar_autores()
        valores = [f"{autor[1]} (ID: {autor[0]})" for autor in autores]
        self.combo_autor["values"] = valores
        self.combo_filtro_autor["values"] = ["Todos"] + valores
        if valores:
            self.combo_autor.set("")
            self.combo_filtro_autor.set("Todos")
            self.btn_adicionar_livro.state(["!disabled"])
        else:
            self.combo_autor.set("")
            self.combo_filtro_autor.set("Todos")
            self.btn_adicionar_livro.state(["disabled"])
            messagebox.showwarning("Aviso", "Cadastre pelo menos um autor antes de adicionar livros.")

    def atualizar_tabela_autores(self):
        for item in self.tree_autores.get_children():
            self.tree_autores.delete(item)
        autores = self.db.listar_autores()
        if not autores:
            self.tree_autores.insert("", tk.END, values=("", "Nenhum autor cadastrado", ""))
        else:
            for row in autores:
                self.tree_autores.insert("", tk.END, values=row)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        livros = self.db.listar_livros()
        if not livros:
            self.tree.insert("", tk.END, values=("", "Nenhum livro cadastrado", "", "", ""))
        else:
            for row in livros:
                self.tree.insert("", tk.END, values=row)

    def adicionar_autor(self):
        try:
            nome = self.entry_nome_autor.get().strip()
            nacionalidade = self.entry_nacionalidade.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome do autor é obrigatório!")
                return
            self.db.adicionar_autor(nome, nacionalidade)
            messagebox.showinfo("Sucesso", "Autor adicionado com sucesso!")
            self.entry_nome_autor.delete(0, tk.END)
            self.entry_nacionalidade.delete(0, tk.END)
            self.atualizar_combo_autores()
            self.atualizar_tabela()
            self.atualizar_tabela_autores()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def adicionar_livro(self):
        try:
            autor_selecionado = self.combo_autor.get()
            if not autor_selecionado:
                messagebox.showerror("Erro", "Selecione um autor!")
                return
            id_autor = int(autor_selecionado.split("ID: ")[1].replace(")", ""))
            self.db.adicionar_livro(
                self.entry_titulo.get().strip(),
                self.entry_ano.get().strip(),
                self.entry_genero.get().strip(),
                id_autor
            )
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
            self.entry_titulo.delete(0, tk.END)
            self.entry_ano.delete(0, tk.END)
            self.entry_genero.delete(0, tk.END)
            self.combo_autor.set("")
            self.atualizar_tabela()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def buscar_livros(self, event):
        busca_titulo = self.entry_busca.get().strip()
        filtro_autor = self.combo_filtro_autor.get()
        self.atualizar_tabela_filtros(filtro_autor, busca_titulo)

    def filtrar_por_autor(self, event):
        busca_titulo = self.entry_busca.get().strip()
        filtro_autor = self.combo_filtro_autor.get()
        self.atualizar_tabela_filtros(filtro_autor, busca_titulo)

    def atualizar_tabela_filtros(self, filtro_autor, busca_titulo):
        for item in self.tree.get_children():
            self.tree.delete(item)
        livros = self.db.listar_livros(filtro_autor, busca_titulo)
        if not livros:
            self.tree.insert("", tk.END, values=("", "Nenhum livro encontrado", "", "", ""))
        else:
            for row in livros:
                self.tree.insert("", tk.END, values=row)

    def editar_livro(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um livro para editar!")
            return
        id_livro = self.tree.item(selecionado)["values"][0]
        if not id_livro:
            messagebox.showerror("Erro", "Nenhum livro válido selecionado!")
            return
        livro = self.db.listar_livros()
        livro = next((l for l in livro if l[0] == id_livro), None)
        janela = tk.Toplevel(self.root)
        janela.title("Editar Livro")
        janela.geometry("600x450")
        janela.configure(bg="#e8ecef")
        frame = tk.Frame(janela, bg="#e8ecef")
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        tk.Label(frame, text="Título:", bg="#e8ecef").pack(pady=10)
        entry_titulo = ttk.Entry(frame)
        entry_titulo.insert(0, livro[1])
        entry_titulo.pack(pady=5, padx=20, fill="x")
        tk.Label(frame, text="Ano de Publicação:", bg="#e8ecef").pack(pady=10)
        entry_ano = ttk.Entry(frame)
        entry_ano.insert(0, livro[2])
        entry_ano.pack(pady=5, padx=20, fill="x")
        tk.Label(frame, text="Gênero:", bg="#e8ecef").pack(pady=10)
        entry_genero = ttk.Entry(frame)
        entry_genero.insert(0, livro[3] or "")
        entry_genero.pack(pady=5, padx=20, fill="x")
        tk.Label(frame, text="Autor:", bg="#e8ecef").pack(pady=10)
        combo_autor = ttk.Combobox(frame, values=self.combo_autor["values"], state="readonly")
        combo_autor.set(livro[4])
        combo_autor.pack(pady=5, padx=20, fill="x")
        def salvar_edicao():
            try:
                id_autor = int(combo_autor.get().split("ID: ")[1].replace(")", ""))
                self.db.atualizar_livro(
                    id_livro,
                    entry_titulo.get().strip(),
                    entry_ano.get().strip(),
                    entry_genero.get().strip(),
                    id_autor
                )
                messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
                janela.destroy()
                self.atualizar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        ttk.Button(frame, text="Salvar Alterações", command=salvar_edicao).pack(pady=20)

    def editar_autor(self):
        selecionado = self.tree_autores.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um autor para editar!")
            return
        id_autor = self.tree_autores.item(selecionado)["values"][0]
        if not id_autor:
            messagebox.showerror("Erro", "Nenhum autor válido selecionado!")
            return
        autor = self.db.listar_autores()
        autor = next((a for a in autor if a[0] == id_autor), None)
        janela = tk.Toplevel(self.root)
        janela.title("Editar Autor")
        janela.geometry("400x300")
        janela.configure(bg="#e8ecef")
        frame = tk.Frame(janela, bg="#e8ecef")
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        tk.Label(frame, text="Nome:", bg="#e8ecef").pack(pady=10)
        entry_nome = ttk.Entry(frame)
        entry_nome.insert(0, autor[1])
        entry_nome.pack(pady=5, padx=20, fill="x")
        tk.Label(frame, text="Nacionalidade:", bg="#e8ecef").pack(pady=10)
        entry_nacionalidade = ttk.Entry(frame)
        entry_nacionalidade.insert(0, autor[2] or "")
        entry_nacionalidade.pack(pady=5, padx=20, fill="x")
        def salvar_edicao():
            try:
                self.db.atualizar_autor(
                    id_autor,
                    entry_nome.get().strip(),
                    entry_nacionalidade.get().strip()
                )
                messagebox.showinfo("Sucesso", "Autor atualizado com sucesso!")
                janela.destroy()
                self.atualizar_tabela_autores()
                self.atualizar_combo_autores()
                self.atualizar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        ttk.Button(frame, text="Salvar Alterações", command=salvar_edicao).pack(pady=20)

    def excluir_livro(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um livro para excluir!")
            return
        id_livro = self.tree.item(selecionado)["values"][0]
        if not id_livro:
            messagebox.showerror("Erro", "Nenhum livro válido selecionado!")
            return
        if messagebox.askyesno("Confirmação", "Deseja excluir o livro selecionado?"):
            try:
                self.db.excluir_livro(id_livro)
                messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def excluir_autor(self):
        selecionado = self.tree_autores.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um autor para excluir!")
            return
        id_autor = self.tree_autores.item(selecionado)["values"][0]
        if not id_autor:
            messagebox.showerror("Erro", "Nenhum autor válido selecionado!")
            return
        if messagebox.askyesno("Confirmação", "Deseja excluir o autor selecionado?"):
            try:
                self.db.excluir_autor(id_autor)
                messagebox.showinfo("Sucesso", "Autor excluído com sucesso!")
                self.atualizar_tabela_autores()
                self.atualizar_combo_autores()
                self.atualizar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", str(e))