import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from funções import *

janela_login = tb.Window(themename="superhero")
janela_login.title('Tela de Login')
janela_login.geometry('500x450')



imagem_original = Image.open("LogoPrecifly.png") # carregando a imagem
imagem_redimensionada = imagem_original.resize((400, 150), Image.Resampling.LANCZOS) # redimensionando a imagem
imagem_tk = ImageTk.PhotoImage(imagem_redimensionada) # carregando a imagem pra um formato compatível com o ttkbootstrap

label_imagem = tb.Label(janela_login, image=imagem_tk) # colocando a imagem na label
label_imagem.image = imagem_tk  # Necessário para evitar que o coletor de lixo do Python apague a imagem
label_imagem.pack()



titulo = tb.Label(janela_login, text='Faça o Login', font=('Segoe UI', 20))
titulo.pack(pady=(0, 10))



fundo_frame = tb.Frame(janela_login)
fundo_frame.pack(fill=Y, expand=True, padx=20, pady=10)


usuario = tb.Label(fundo_frame, text='Usuário', font=('Segoe UI', 12))
usuario.pack(anchor='w', padx=(10, 0))
input_usuario = tb.Entry(fundo_frame, width=30)
input_usuario.pack(pady=(0, 5))

senha = tb.Label(fundo_frame, text='Senha', font=('Segoe UI', 12))
senha.pack(anchor='w', padx=(10, 0))
input_senha = tb.Entry(fundo_frame, show='*', width=30)
input_senha.pack()

tb.Button(fundo_frame, text="Login", bootstyle="primary", width=15, command=realizar_login).pack(pady=20)


janela_login.mainloop()