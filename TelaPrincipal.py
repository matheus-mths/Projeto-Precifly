import ttkbootstrap as tb
from ttkbootstrap.constants import * # para ser possível deixar alinhado, não ter espaços em branco e tals
import sqlite3
import unicodedata
import sys
import os
from PIL import Image, ImageTk
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PreciFly.app')

# caminho da pasta onde o programa está rodando
# quando vira .exe o __file__ não funciona, então usamos sys.executable
if getattr(sys, 'frozen', False):
    PASTA = os.path.dirname(sys.executable)
else:
    PASTA = os.path.dirname(os.path.abspath(__file__))
from calculo import buscar_aliquotas

# taxas de cada marketplace em %
taxa_mercado_livre = 14.0
taxa_shopee = 13.0
taxa_amazon = 15.0
taxa_magalu = 12.0

# função pra normalizar o texto: tira acentos e coloca tudo em minúsculo
# assim funciona mesmo se a pessoa digitar "mouse gamer", "Mouse Gamer" ou "mouse gâmer"
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto_limpo = ''
    for letra in texto:
        if unicodedata.category(letra) != 'Mn':
            texto_limpo += letra
    return texto_limpo

# criando janela
app = tb.Window(themename="superhero")
app.title("Sistema Inteligente de Precificação")
app.state('zoomed')  # abre maximizado

# título centralizado normalmente
titulo = tb.Label(app, text="Sistema Inteligente de Precificação", font=("Segoe UI", 22, 'bold'))
titulo.pack(pady=20)

# logo sobreposta no canto superior direito com place
img_logo = Image.open(os.path.join(PASTA, "LogoPrecifly.png"))
img_logo_tk = ImageTk.PhotoImage(img_logo)
label_logo = tb.Label(app, image=img_logo_tk)
label_logo.image = img_logo_tk
label_logo.place(relx=1.0, rely=0.0, anchor='ne', x=-15, y=5)

# aplica o ícone da janela
app.after(500, lambda: app.iconbitmap(os.path.join(PASTA, "icone.ico")))

# precisamos criar um "fundo" para "guardar" as coisas, como os inputs e os resultados
fundo_dados = tb.Frame(app)
fundo_dados.pack(fill=BOTH, expand=True, padx=20, pady=10)

# inputs
inputs = tb.Labelframe(fundo_dados, text="Dados do Produto", padding=20, bootstyle="primary")
inputs.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

var_nome_produto = tb.StringVar()
# Alterado para StringVar para lidar com o input de texto, permitindo trocar vírgula por ponto
var_custo_produto = tb.StringVar(value="0")
var_uf = tb.StringVar(value="SP")

mercado_livre = tb.BooleanVar()
shopee = tb.BooleanVar()
amazon = tb.BooleanVar()
magalu = tb.BooleanVar()

var_taxa_maquininha = tb.StringVar(value="0")
var_margem_lucro = tb.StringVar(value="0")

# nome do produto
tb.Label(inputs, text="Produto").pack(anchor=W, pady=(10, 2))
frame_busca = tb.Frame(inputs)
frame_busca.pack(fill=X)
input_produto = tb.Entry(frame_busca, textvariable=var_nome_produto)
input_produto.pack(side=LEFT, fill=X, expand=True)
tb.Button(frame_busca, text="Buscar", bootstyle="secondary", width=8, command=lambda: buscar_produto()).pack(side=LEFT, padx=(5, 0))

# custo do produto
tb.Label(inputs, text="Custo do Produto (R$)").pack(anchor=W, pady=(10, 2))
input_custo = tb.Entry(inputs, textvariable=var_custo_produto)
input_custo.pack(fill=X)

# estado (UF) - usado para buscar o imposto correto na API do IBPT
tb.Label(inputs, text="Estado (UF)").pack(anchor=W, pady=(10, 2))
lista_estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
                 "MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
tb.Combobox(inputs, textvariable=var_uf, values=lista_estados, width=10, state="readonly").pack(anchor=W)

# marketplace
tb.Label(inputs, text="Marketplace").pack(anchor=W, pady=(15, 5))
marketplace_checks = tb.Frame(inputs)
marketplace_checks.pack(fill=X)
tb.Checkbutton(marketplace_checks, text="Mercado Livre", variable=mercado_livre, bootstyle="success-round-toggle").pack(anchor=W)
tb.Checkbutton(marketplace_checks, text="Shopee", variable=shopee, bootstyle="success-round-toggle").pack(anchor=W)
tb.Checkbutton(marketplace_checks, text="Amazon", variable=amazon, bootstyle="success-round-toggle").pack(anchor=W)
tb.Checkbutton(marketplace_checks, text="Magalu", variable=magalu, bootstyle="success-round-toggle").pack(anchor=W)

# taxa da maquininha
tb.Label(inputs, text="Taxa da Maquininha (%)").pack(anchor=W, pady=(15, 2))
input_taxa_maquininha = tb.Entry(inputs, textvariable=var_taxa_maquininha)
input_taxa_maquininha.pack(fill=X)

# margem de lucro
tb.Label(inputs, text="Margem de Lucro Desejada (%)").pack(anchor=W, pady=(15, 2))
input_margem_lucro = tb.Entry(inputs, textvariable=var_margem_lucro)
input_margem_lucro.pack(fill=X)

# VARIÁVEIS PARA ATUALIZAR AS LABELS DE RESULTADO
var_resultado_custo = tb.StringVar(value="R$ 0,00")
var_resultado_minimo = tb.StringVar(value="R$ 0,00")
var_resultado_ideal = tb.StringVar(value="R$ 0,00")
var_resultado_percentual = tb.StringVar(value="0,00 %")
var_resultado_marketplace = tb.StringVar(value="Nenhum marketplace selecionado")

def buscar_produto():
    nome_digitado = var_nome_produto.get()

    if nome_digitado == "":
        tb.dialogs.Messagebox.show_warning("Digite o nome do produto primeiro!", "Aviso")
        return

    # busca todos os produtos e compara ignorando maiúsculas e acentos
    conexao = sqlite3.connect(os.path.join(PASTA, 'banco.db'))
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, custo, margem_lucro, uf FROM produtos")
    todos_produtos = cursor.fetchall()
    conexao.close()

    produto_encontrado = None
    for p in todos_produtos:
        if normalizar_texto(p[0]) == normalizar_texto(nome_digitado):
            produto_encontrado = p
            break

    if produto_encontrado:
        if produto_encontrado[1] is not None:
            var_custo_produto.set(str(produto_encontrado[1]))
        if produto_encontrado[2] is not None:
            var_margem_lucro.set(str(produto_encontrado[2]))
        if produto_encontrado[3] is not None:
            var_uf.set(produto_encontrado[3])
        tb.dialogs.Messagebox.show_info(f"Produto '{produto_encontrado[0]}' carregado!", "Sucesso")
    else:
        tb.dialogs.Messagebox.show_warning("Produto não encontrado no banco de dados!", "Aviso")

def salvar_produto():
    nome = var_nome_produto.get()

    if nome == "":
        tb.dialogs.Messagebox.show_warning("Digite o nome do produto antes de salvar!", "Aviso")
        return

    try:
        custo = float(var_custo_produto.get().replace(',', '.'))
        margem = float(var_margem_lucro.get().replace(',', '.'))
        uf = var_uf.get()
    except ValueError:
        tb.dialogs.Messagebox.show_error("Verifique se os valores digitados são números válidos!", "Erro")
        return

    # busca o nome exato no banco (ignorando acentos e maiúsculas) pra salvar corretamente
    conexao = sqlite3.connect(os.path.join(PASTA, 'banco.db'))
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM produtos")
    todos = cursor.fetchall()

    nome_real = None
    for p in todos:
        if normalizar_texto(p[0]) == normalizar_texto(nome):
            nome_real = p[0]
            break

    if nome_real is None:
        conexao.close()
        tb.dialogs.Messagebox.show_warning("Produto não encontrado no banco! Verifique o nome.", "Aviso")
        return

    cursor.execute(
        "UPDATE produtos SET custo = ?, margem_lucro = ?, uf = ? WHERE nome = ?",
        (custo, margem, uf, nome_real)
    )
    conexao.commit()
    conexao.close()

    tb.dialogs.Messagebox.show_info(f"Produto '{nome_real}' salvo!", "Sucesso")

def calcular_precificacao():
    try:
        custo_produto = float(var_custo_produto.get().replace(',', '.'))
        taxa_maquinha = float(var_taxa_maquininha.get().replace(',', '.'))
        margem_de_lucro = float(var_margem_lucro.get().replace(',', '.'))
        uf = var_uf.get()
        nome = var_nome_produto.get()
    except ValueError:
        tb.dialogs.Messagebox.show_error("Verifique se os valores digitados são números válidos!", "Erro")
        return

    if nome == "":
        tb.dialogs.Messagebox.show_warning("Digite o nome do produto!", "Aviso")
        return

    # busca o NCM do produto no banco (ignorando acentos e maiúsculas) pra consultar o IBPT
    conexao = sqlite3.connect(os.path.join(PASTA, 'banco.db'))
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, NCM FROM produtos")
    todos_produtos = cursor.fetchall()
    conexao.close()

    ncm = None
    for p in todos_produtos:
        if normalizar_texto(p[0]) == normalizar_texto(nome):
            ncm = p[1]
            break

    if ncm is None:
        tb.dialogs.Messagebox.show_error(f"Produto '{nome}' não encontrado no banco!\nVerifique o nome.", "Erro")
        return

    # busca as alíquotas do IBPT na API (ou no cache local se já tiver baixado)
    aliquotas = buscar_aliquotas(ncm, uf)

    if not aliquotas:
        tb.dialogs.Messagebox.show_error(f"Não foi possível encontrar o NCM {ncm} para o estado {uf}.", "Erro")
        return

    # soma as alíquotas federal + estadual + municipal
    imposto_ibpt = (
        float(aliquotas["aliquotaNacionalFederal"]) +
        float(aliquotas["aliquotaEstadual"]) +
        float(aliquotas["aliquotaMunicipal"])
    )

    # 1) imposto IBPT é calculado em cima do custo do produto
    valor_imposto = custo_produto * (imposto_ibpt / 100)
    custo_total = custo_produto + valor_imposto

    # 2) preço mínimo: custo total + taxa da maquininha (só cobre os custos, sem lucro)
    preco_minimo = custo_total * (1 + taxa_maquinha / 100)

    # 3) preço ideal: soma tudo em cima do custo total (maquininha + margem de lucro)
    preco_lucro = custo_total * (1 + (taxa_maquinha + margem_de_lucro) / 100)

    # percentual total de custos (maquininha + imposto)
    total_custos_pct = taxa_maquinha + imposto_ibpt

    # ATUALIZA AS VARIÁVEIS DE TEXTO
    var_resultado_custo.set(f"R$ {custo_total:.2f}".replace('.', ','))
    var_resultado_minimo.set(f"R$ {preco_minimo:.2f}".replace('.', ','))
    var_resultado_ideal.set(f"R$ {preco_lucro:.2f}".replace('.', ','))
    var_resultado_percentual.set(f"{total_custos_pct:.2f} %".replace('.', ','))

    # 4) preço por marketplace: soma a taxa do marketplace também em cima do custo total
    resultado_texto = ""
    if mercado_livre.get():
        preco_ml = custo_total * (1 + (taxa_maquinha + taxa_mercado_livre + margem_de_lucro) / 100)
        resultado_texto += f"Mercado Livre: R$ {preco_ml:.2f}\n".replace('.', ',')
    if shopee.get():
        preco_shopee = custo_total * (1 + (taxa_maquinha + taxa_shopee + margem_de_lucro) / 100)
        resultado_texto += f"Shopee: R$ {preco_shopee:.2f}\n".replace('.', ',')
    if amazon.get():
        preco_amazon = custo_total * (1 + (taxa_maquinha + taxa_amazon + margem_de_lucro) / 100)
        resultado_texto += f"Amazon: R$ {preco_amazon:.2f}\n".replace('.', ',')
    if magalu.get():
        preco_magalu = custo_total * (1 + (taxa_maquinha + taxa_magalu + margem_de_lucro) / 100)
        resultado_texto += f"Magalu: R$ {preco_magalu:.2f}\n".replace('.', ',')

    if resultado_texto == "":
        var_resultado_marketplace.set("Nenhum marketplace selecionado")
    else:
        var_resultado_marketplace.set(resultado_texto.strip())

# botões de ação
frame_botoes = tb.Frame(inputs)
frame_botoes.pack(fill=X)
tb.Button(frame_botoes, text="Calcular Preço", bootstyle=SUCCESS, command=calcular_precificacao).pack(side=LEFT, expand=True, fill=X, padx=(0, 5), pady=20)
tb.Button(frame_botoes, text="Salvar", bootstyle=INFO, command=salvar_produto).pack(side=LEFT, expand=True, fill=X, padx=(5, 0), pady=20)

# resultados da precificação
resultados = tb.Labelframe(fundo_dados, text="Resultados da Precificação", padding=20, bootstyle=SUCCESS)
resultados.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

# Card 1 - Custo Total
card_custo_total = tb.Frame(resultados, bootstyle=DANGER)
card_custo_total.pack(fill=X, pady=10)
tb.Label(card_custo_total, text="Custo Total", font=("Segoe UI", 14, 'bold'), background="#d9534f").pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_custo_total, textvariable=var_resultado_custo, font=("Segoe UI", 20, 'bold'), background="#d9534f").pack(anchor=W, padx=15, pady=(5, 10))

# Card 2 - Preço Mínimo
card_preco_min = tb.Frame(resultados, bootstyle=WARNING)
card_preco_min.pack(fill=X, pady=10)
tb.Label(card_preco_min, text="Preço Mínimo", font=("Segoe UI", 14, 'bold'), background="#f0ad4e").pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_preco_min, textvariable=var_resultado_minimo, font=("Segoe UI", 20, 'bold'), background="#f0ad4e").pack(anchor=W, padx=15, pady=(5, 10))

# Card 3 - Preço Ideal
card_preco_ideal = tb.Frame(resultados, bootstyle=SUCCESS)
card_preco_ideal.pack(fill=X, pady=10)
tb.Label(card_preco_ideal, text="Preço Ideal (Com Lucro)", font=("Segoe UI", 14, 'bold'), background="#5cb85c").pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_preco_ideal, textvariable=var_resultado_ideal, font=("Segoe UI", 20, 'bold'), background="#5cb85c").pack(anchor=W, padx=15, pady=(5, 10))

# Card 4 - Custos Percentuais
card_custos = tb.Frame(resultados, bootstyle=INFO)
card_custos.pack(fill=X, pady=10)
tb.Label(card_custos, text="Custos Percentuais", font=("Segoe UI", 14, 'bold'), background="#5bc0de").pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_custos, textvariable=var_resultado_percentual, font=("Segoe UI", 20, 'bold'), background="#5bc0de").pack(anchor=W, padx=15, pady=(5, 10))

# Card 5 - Preço por Marketplace
card_marketplace = tb.Frame(resultados, bootstyle=SECONDARY)
card_marketplace.pack(fill=X, pady=10)
tb.Label(card_marketplace, text="Preço por Marketplace", font=("Segoe UI", 14, 'bold'), background="#6c757d").pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_marketplace, textvariable=var_resultado_marketplace, font=("Segoe UI", 16, 'bold'), background="#6c757d", justify=LEFT).pack(anchor=W, padx=15, pady=(5, 10))

app.mainloop()
