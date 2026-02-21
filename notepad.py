# IMPORTAÇÕES
import tkinter as tk
from tkinter import filedialog, font, ttk
from PIL import Image, ImageTk #Consertar o erro do PIL no Linux
import subprocess
import sys
import webbrowser

# JANELA PRINCIPAL
janela = tk.Tk()
janela.title("Bloco de Notas")

largura_tela = janela.winfo_screenwidth()
altura_tela  = janela.winfo_screenheight()
largura = int(largura_tela * 0.8)
altura  = int(altura_tela  * 0.8)
pos_x   = int((largura_tela - largura) / 2)
pos_y   = int((altura_tela  - altura)  / 2)
janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

# FONTE 
fonte_texto = font.Font(family="Arial", size=14)
fontes_disponiveis = sorted(set(font.families()))

# ESTILO DAS ABAS
estilo = ttk.Style()
estilo.theme_use("default")
estilo.configure("TNotebook", background="#e0e0e0", borderwidth=0)
estilo.configure("TNotebook.Tab",
    background="#d0d0d0", foreground="#444444",
    padding=[12, 5], font=("Arial", 10)
)
estilo.map("TNotebook.Tab",
    background=[("selected", "#ffffff")],
    foreground=[("selected", "#000000")]
)

# BARRA DE STATUS
status = tk.Label(
    janela,
    text="Linhas: 1 | Caracteres: 0",
    anchor="e", padx=10,
    font=("Arial", 10),
    bg="#f0f0f0", fg="#555555"
)
status.pack(side="bottom", fill="x")

# BARRA DE FERRAMENTAS
barra = tk.Frame(janela, bg="#f0f0f0", pady=4)
barra.pack(side="top", fill="x")

def sep():
    tk.Label(barra, text="|", bg="#f0f0f0", fg="#cccccc",
             font=("Arial", 14)).pack(side="left", padx=4)

# Arquivo
tk.Button(barra, text="📄 Novo",   font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: nova_aba()).pack(side="left", padx=2)
tk.Button(barra, text="📂 Abrir",  font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: abrir_arquivo()).pack(side="left", padx=2)
tk.Button(barra, text="💾 Salvar", font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: salvar_arquivo()).pack(side="left", padx=2)
sep()

# Fonte
fonte_var = tk.StringVar(value="Arial")
campo_fonte = tk.Entry(barra, textvariable=fonte_var, width=18,
                       font=("Arial", 10), relief="solid", bd=1)
campo_fonte.pack(side="left", padx=(4, 0))
sep()

# Tamanho
campo_tamanho = tk.Entry(barra, width=4, font=("Arial", 10),
                         justify="center", relief="solid", bd=1)
campo_tamanho.insert(0, "14")
campo_tamanho.pack(side="left", padx=(0, 4))
sep()

# Alinhamento
tk.Button(barra, text="⬅", font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: alinhar("esquerda")).pack(side="left", padx=2)
tk.Button(barra, text="≡", font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: alinhar("centro")).pack(side="left", padx=2)
tk.Button(barra, text="➡", font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: alinhar("direita")).pack(side="left", padx=2)
sep()

# Inserção
tk.Button(barra, text="🔗 Link",    font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: inserir_link()).pack(side="left", padx=2)
tk.Button(barra, text="🖼️ Imagem", font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: inserir_imagem()).pack(side="left", padx=2)
tk.Button(barra, text="📌 Nota",   font=("Arial", 10), relief="flat",
          bg="#f0f0f0", cursor="hand2",
          command=lambda: nova_nota_adesiva()).pack(side="left", padx=2)

# NOTEBOOK 
notebook = ttk.Notebook(janela)
notebook.pack(side="top", expand=True, fill="both")

abas = {}
contador_abas = [0]

def get_texto_ativo():
    aba_atual = notebook.select()
    if not aba_atual:
        return None
    frame = notebook.nametowidget(aba_atual)
    return abas[frame]["texto"]

def get_frame_ativo():
    aba_atual = notebook.select()
    if not aba_atual:
        return None
    return notebook.nametowidget(aba_atual)

def nova_aba(titulo="Sem título", conteudo=""):
    contador_abas[0] += 1

    # Frame externo da aba 
    frame = tk.Frame(notebook)
    notebook.add(frame, text=f"  {titulo}  ")

    # Área de texto
    txt = tk.Text(
        frame,
        font=fonte_texto,
        wrap="word",
        undo=True,
        padx=10,
        pady=10
    )
    txt.pack(expand=True, fill="both")

    if conteudo:
        txt.insert("1.0", conteudo)

    txt.bind("<KeyRelease>", atualizar_status)

    abas[frame] = {"texto": txt, "imagens": [], "notas": []}

    notebook.select(frame)
    _adicionar_botao_fechar(frame, titulo)

    txt.focus()
    return frame

def _adicionar_botao_fechar(frame, titulo):
    idx = notebook.index(frame)


    tab_frame = tk.Frame(notebook, bg="#d0d0d0")

    lbl = tk.Label(tab_frame, text=titulo, bg="#d0d0d0",
                   font=("Arial", 10), padx=4)
    lbl.pack(side="left")

    def fechar_aba():
        idx_atual = notebook.index(frame)
        notebook.forget(frame)
        del abas[frame]
        # Se não sobrou nenhuma aba, abre uma nova
        if notebook.index("end") == 0:
            nova_aba()

    btn = tk.Button(tab_frame, text="✖", font=("Arial", 8),
                    bg="#d0d0d0", fg="#666666", relief="flat",
                    cursor="hand2", command=fechar_aba,
                    padx=2, pady=0)
    btn.pack(side="left")

    notebook.tab(frame, text=f"  {titulo}   ✖")

    frame._fechar = fechar_aba
    frame._titulo = titulo

def renomear_aba(frame=None):
    if frame is None:
        frame = get_frame_ativo()
    if not frame:
        return

    titulo_atual = getattr(frame, "_titulo", "Sem título")

    janela_rename = tk.Toplevel(janela)
    janela_rename.title("Renomear aba")
    janela_rename.geometry("320x110")
    janela_rename.resizable(False, False)
    janela_rename.grab_set()

    tk.Label(janela_rename, text="Novo nome da aba:",
             font=("Arial", 10)).pack(pady=(18, 4))

    campo = tk.Entry(janela_rename, font=("Arial", 11), width=28, relief="solid", bd=1)
    campo.insert(0, titulo_atual)
    campo.select_range(0, tk.END)
    campo.pack()
    campo.focus()

    def confirmar(event=None):
        novo = campo.get().strip()
        if not novo:
            novo = "Sem título"
        frame._titulo = novo
        notebook.tab(frame, text=f"  {novo}   ✖")
        janela_rename.destroy()

    campo.bind("<Return>", confirmar)
    tk.Button(janela_rename, text="Renomear", font=("Arial", 10),
              bg="#0078d4", fg="white", relief="flat",
              command=confirmar).pack(pady=10)

def _clique_duplo_aba(event):
    try:
        idx = notebook.index(f"@{event.x},{event.y}")
        frame = notebook.nametowidget(notebook.tabs()[idx])
        renomear_aba(frame)
    except tk.TclError:
        pass

notebook.bind("<Double-Button-1>", _clique_duplo_aba)

def fechar_aba_ativa():
    frame = get_frame_ativo()
    if frame and hasattr(frame, "_fechar"):
        frame._fechar()

# DROPDOWN DE FONTES
lista_fontes = tk.Listbox(
    janela, height=8, font=("Arial", 10),
    relief="solid", bd=1,
    selectbackground="#0078d4", selectforeground="white"
)

def mostrar_lista(event=None):
    lista_fontes.delete(0, tk.END)
    termo = fonte_var.get().lower()
    for f in fontes_disponiveis:
        if termo in f.lower():
            lista_fontes.insert(tk.END, f)
    x = campo_fonte.winfo_rootx() - janela.winfo_rootx()
    y = campo_fonte.winfo_rooty() - janela.winfo_rooty() + campo_fonte.winfo_height()
    lista_fontes.place(x=x, y=y, width=campo_fonte.winfo_width())
    lista_fontes.lift()

def selecionar_fonte(event=None):
    if lista_fontes.curselection():
        escolha = lista_fontes.get(lista_fontes.curselection())
        fonte_var.set(escolha)
        fonte_texto.config(family=escolha)
        lista_fontes.place_forget()
        txt = get_texto_ativo()
        if txt:
            txt.focus()

def esconder_lista(event=None):
    lista_fontes.place_forget()

campo_fonte.bind("<FocusIn>",    mostrar_lista)
campo_fonte.bind("<KeyRelease>", mostrar_lista)
campo_fonte.bind("<Return>",     lambda e: mudar_fonte())
lista_fontes.bind("<<ListboxSelect>>", selecionar_fonte)
janela.bind("<Button-1>", lambda e: esconder_lista()
            if e.widget not in (campo_fonte, lista_fontes) else None)

campo_tamanho.bind("<Return>",   lambda e: aplicar_tamanho())
campo_tamanho.bind("<FocusOut>", lambda e: aplicar_tamanho())

# FUNÇÕES

def abrir_arquivo():
    if sys.platform == "win32":
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
    else:
        resultado = subprocess.run(
            ["kdialog", "--getopenfilename", ".", "*.txt"],
            capture_output=True, text=True
        )
        caminho = resultado.stdout.strip()
    if caminho:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        nome = caminho.split("/")[-1].split("\\")[-1]
        nova_aba(titulo=nome, conteudo=conteudo)
        janela.title(f"Bloco de Notas - {caminho}")

def salvar_arquivo():
    txt = get_texto_ativo()
    if not txt:
        return
    if sys.platform == "win32":
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt")]
        )
    else:
        resultado = subprocess.run(
            ["kdialog", "--getsavefilename", ".", "*.txt"],
            capture_output=True, text=True
        )
        caminho = resultado.stdout.strip()
    if caminho:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(txt.get("1.0", tk.END))
        nome = caminho.split("/")[-1].split("\\")[-1]
        notebook.tab(get_frame_ativo(), text=f"  {nome}   ✖")
        janela.title(f"Bloco de Notas - {caminho}")

def atualizar_status(event=None):
    txt = get_texto_ativo()
    if not txt:
        return
    conteudo = txt.get("1.0", tk.END)
    chars  = len(conteudo) - 1
    linhas = int(txt.index(tk.END).split(".")[0]) - 1
    status.config(text=f"Linhas: {linhas} | Caracteres: {chars}")

def mudar_fonte():
    fonte_texto.config(family=fonte_var.get())
    txt = get_texto_ativo()
    if txt:
        txt.focus()

def aplicar_tamanho():
    try:
        tamanho = int(campo_tamanho.get())
        tamanho = max(1, min(200, tamanho))
        fonte_texto.config(size=tamanho)
        campo_tamanho.delete(0, tk.END)
        campo_tamanho.insert(0, str(tamanho))
        txt = get_texto_ativo()
        if txt:
            txt.focus()
    except ValueError:
        campo_tamanho.delete(0, tk.END)
        campo_tamanho.insert(0, str(fonte_texto.cget("size")))

def alinhar(alinhamento):
    txt = get_texto_ativo()
    if not txt:
        return
    txt.tag_remove("esquerda", "1.0", tk.END)
    txt.tag_remove("centro",   "1.0", tk.END)
    txt.tag_remove("direita",  "1.0", tk.END)
    txt.tag_add(alinhamento, "1.0", tk.END)
    txt.tag_configure("esquerda", justify="left")
    txt.tag_configure("centro",   justify="center")
    txt.tag_configure("direita",  justify="right")

def abrir_link_url(url):
    webbrowser.open(url)

def inserir_link():
    txt = get_texto_ativo()
    if not txt:
        return
    janela_link = tk.Toplevel(janela)
    janela_link.title("Inserir Link")
    janela_link.geometry("400x200")
    janela_link.resizable(False, False)

    tk.Label(janela_link, text="Texto do link:", font=("Arial", 10)).pack(pady=(15, 2))
    campo_texto_link = tk.Entry(janela_link, width=40, font=("Arial", 10))
    campo_texto_link.pack()

    tk.Label(janela_link, text="URL:", font=("Arial", 10)).pack(pady=(8, 2))
    campo_url = tk.Entry(janela_link, width=40, font=("Arial", 10))
    campo_url.pack()

    def confirmar():
        texto_link = campo_texto_link.get().strip()
        url = campo_url.get().strip()
        if not texto_link or not url:
            return
        posicao = txt.index(tk.INSERT)
        txt.insert(posicao, texto_link)
        fim = txt.index(tk.INSERT)
        tag = f"link_{posicao}"
        txt.tag_add(tag, posicao, fim)
        txt.tag_configure(tag, foreground="#0078d4", underline=True)
        txt.tag_bind(tag, "<Button-1>", lambda e: abrir_link_url(url))
        txt.tag_bind(tag, "<Enter>", lambda e: janela.config(cursor="hand2"))
        txt.tag_bind(tag, "<Leave>", lambda e: janela.config(cursor=""))
        janela_link.destroy()

    tk.Button(janela_link, text="Inserir", font=("Arial", 10),
              bg="#0078d4", fg="white", relief="flat", command=confirmar).pack(pady=10)

def inserir_imagem():
    txt = get_texto_ativo()
    frame = get_frame_ativo()
    if not txt:
        return
    if sys.platform == "win32":
        caminho = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
    else:
        resultado = subprocess.run(
            ["kdialog", "--getopenfilename", ".", "*.png *.jpg *.jpeg *.gif *.bmp"],
            capture_output=True, text=True
        )
        caminho = resultado.stdout.strip()
    if caminho:
        img = Image.open(caminho)
        largura_max = 400
        if img.width > largura_max:
            proporcao = largura_max / img.width
            nova_altura = int(img.height * proporcao)
            img = img.resize((largura_max, nova_altura), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        abas[frame]["imagens"].append(img_tk)
        txt.image_create(tk.INSERT, image=img_tk)

# NOTA ADESIVA
_notas_internas = []

def nova_nota_adesiva():
    frame = get_frame_ativo()
    if not frame:
        return

    nota_frame = tk.Frame(frame, bg="#fff475", bd=1, relief="solid")
    nota_frame.place(x=40, y=40, width=220, height=180)

    barra_nota = tk.Frame(nota_frame, bg="#f9e84a", pady=3)
    barra_nota.pack(fill="x")

    tk.Label(barra_nota, text="📌 Nota",
             bg="#f9e84a", font=("Arial", 9, "bold")).pack(side="left", padx=6)

    def fechar_nota():
        nota_frame.destroy()

    tk.Button(barra_nota, text="✖", bg="#f9e84a", font=("Arial", 9, "bold"),
              relief="flat", cursor="hand2", command=fechar_nota).pack(side="right", padx=4)

    texto_nota = tk.Text(nota_frame, bg="#fff475", fg="#333333",
                         font=("Arial", 10), relief="flat", wrap="word",
                         padx=6, pady=6, insertbackground="#333333")
    texto_nota.pack(expand=True, fill="both")
    texto_nota.focus()

    def iniciar_arraste(event):
        nota_frame._drag_x = event.x_root
        nota_frame._drag_y = event.y_root
        nota_frame._orig_x = nota_frame.winfo_x()
        nota_frame._orig_y = nota_frame.winfo_y()

    def arrastar(event):
        dx = event.x_root - nota_frame._drag_x
        dy = event.y_root - nota_frame._drag_y
        nota_frame.place(x=nota_frame._orig_x + dx, y=nota_frame._orig_y + dy)

    barra_nota.bind("<ButtonPress-1>", iniciar_arraste)
    barra_nota.bind("<B1-Motion>",     arrastar)

    grip = tk.Label(nota_frame, text="⇲", bg="#f9e84a", cursor="sizing", font=("Arial", 8))
    grip.place(relx=1.0, rely=1.0, anchor="se")

    def iniciar_resize(event):
        nota_frame._rx = event.x_root
        nota_frame._ry = event.y_root
        nota_frame._rw = nota_frame.winfo_width()
        nota_frame._rh = nota_frame.winfo_height()

    def fazer_resize(event):
        dw = event.x_root - nota_frame._rx
        dh = event.y_root - nota_frame._ry
        nota_frame.place(width=max(120, nota_frame._rw + dw),
                         height=max(80, nota_frame._rh + dh))

    grip.bind("<ButtonPress-1>", iniciar_resize)
    grip.bind("<B1-Motion>",     fazer_resize)

# ATALHOS DE TECLADO
janela.bind("<Control-n>", lambda e: nova_aba())
janela.bind("<Control-o>", lambda e: abrir_arquivo())
janela.bind("<Control-s>", lambda e: salvar_arquivo())
janela.bind("<Control-w>", lambda e: fechar_aba_ativa())
janela.bind("<F2>",        lambda e: renomear_aba())
janela.bind("<Control-a>", lambda e: get_texto_ativo().tag_add("sel", "1.0", tk.END) if get_texto_ativo() else None)
notebook.bind("<<NotebookTabChanged>>", atualizar_status)

# CRIA A PRIMEIRA ABA
nova_aba()

# INICIA
janela.mainloop()
