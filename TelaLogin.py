import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import subprocess
import sqlite3
import ctypes
import sys
import os

# essa linha é pra garantir que o ícone apareça na barra de tarefas do Windows, mesmo depois de compilar com PyInstaller
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PreciFly.app')

# caminho da pasta onde o programa está rodando
if getattr(sys, 'frozen', False):
    PASTA = os.path.dirname(sys.executable)
else:
    PASTA = os.path.dirname(os.path.abspath(__file__))

# criando a janela de login
janela_login = tb.Window(themename="superhero")
janela_login.title('Tela de Login')
janela_login.geometry('500x420')

# aplica como ícone da janela
janela_login.after(200, lambda: janela_login.iconbitmap(os.path.join(PASTA, "icone.ico")))

# carregando a imagem do logo
imagem_original = Image.open(os.path.join(PASTA, "LogoPrecifly.png"))
imagem_tk = ImageTk.PhotoImage(imagem_original)

label_imagem = tb.Label(janela_login, image=imagem_tk)
label_imagem.image = imagem_tk  # evita que o Python apague a imagem da memória
label_imagem.pack(pady=(20, 0))

titulo = tb.Label(janela_login, text='Faça o Login', font=('Segoe UI', 20))
titulo.pack(pady=(0, 10))

fundo_frame = tb.Frame(janela_login)
fundo_frame.pack(fill=Y, expand=True, padx=20, pady=10)

# campo de email
tb.Label(fundo_frame, text='Email', font=('Segoe UI', 12)).pack(anchor='w', padx=(10, 0))
input_usuario = tb.Entry(fundo_frame, width=30)
input_usuario.pack(pady=(0, 5))

# campo de senha
tb.Label(fundo_frame, text='Senha', font=('Segoe UI', 12)).pack(anchor='w', padx=(10, 0))
input_senha = tb.Entry(fundo_frame, show='*', width=30)
input_senha.pack()

# função que verifica o login no banco de dados
def fazer_login():
    email = input_usuario.get()
    senha_digitada = input_senha.get()

    # verifica se os campos estão preenchidos
    if email == "" or senha_digitada == "":
        tb.dialogs.Messagebox.show_warning("Preencha o email e a senha!", "Aviso")
        return

    # conecta ao banco de dados e busca o usuário
    conexao = sqlite3.connect(os.path.join(PASTA, 'banco.db'))
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = ? AND password = ?", (email, senha_digitada))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        # login correto: fecha essa janela e abre a tela principal
        janela_login.destroy()
        if getattr(sys, 'frozen', False):
            # quando está rodando como .exe, chama o TelaPrincipal.exe
            subprocess.run([os.path.join(PASTA, 'TelaPrincipal.exe')])
        else:
            # quando está rodando como script normal
            subprocess.run([sys.executable, os.path.join(PASTA, 'TelaPrincipal.py')])
    else:
        tb.dialogs.Messagebox.show_error("Email ou senha incorretos!", "Erro de Login")

tb.Button(fundo_frame, text="Entrar", bootstyle="primary", width=15, command=fazer_login).pack(pady=20)

janela_login.mainloop()
