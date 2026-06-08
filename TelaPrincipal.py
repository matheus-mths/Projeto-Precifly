import ttkbootstrap as tb
from ttkbootstrap.constants import * # para ser possível deixar alinhado, não ter espaços em branco e tals

# criando janela
app = tb.Window(themename="superhero")
app.title("Sistema Inteligente de Precificação")
app.geometry("1440x1024")

titulo = tb.Label(app, text="Sistema Inteligente de Precificação", font=("Segoe UI", 22, 'bold'))
titulo.pack(pady=20)

# precisamos criar um "fundo" para "guardar" as coisas, como os inputs e os resultados
fundo_dados = tb.Frame(app)
fundo_dados.pack(fill=BOTH, expand=True, padx=20, pady=10)

# inputs
inputs = tb.Labelframe(fundo_dados, text="Dados do Produto", padding=20, bootstyle="primary")
inputs.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

var_nome_produto = tb.StringVar()
# Alterado para StringVar para lidar com o input de texto, permitindo trocar vírgula por ponto
var_custo_produto = tb.StringVar(value="0") 
var_frete_fornecedor = tb.StringVar(value="0")
var_frete_assumido = tb.StringVar(value="0")
var_custo_embalagem = tb.StringVar(value="0")

mercado_livre = tb.BooleanVar()
shopee = tb.BooleanVar()
amazon = tb.BooleanVar()
magalu = tb.BooleanVar()

var_taxa_maquininha = tb.StringVar(value="0")
var_imposto_ibpt = tb.StringVar(value="0")
var_margem_lucro = tb.StringVar(value="0")

# nome do produto
tb.Label(inputs, text="Produto").pack(anchor=W, pady=(10, 2))
input_produto = tb.Entry(inputs, textvariable=var_nome_produto)
input_produto.pack(fill=X)

# custo do produto
tb.Label(inputs, text="Custo do Produto (R$)").pack(anchor=W, pady=(10, 2))
input_custo = tb.Entry(inputs, textvariable=var_custo_produto)
input_custo.pack(fill=X)

# frete fornecedor
tb.Label(inputs, text="Frete do Fornecedor (R$)").pack(anchor=W, pady=(10, 2))
input_frete_fornecedor = tb.Entry(inputs, textvariable=var_frete_fornecedor)
input_frete_fornecedor.pack(fill=X)

# frete assumido
tb.Label(inputs, text="Frete Assumido pelo Vendedor (R$)").pack(anchor=W, pady=(10, 2))
input_frete_assumido = tb.Entry(inputs, textvariable=var_frete_assumido)
input_frete_assumido.pack(fill=X)

# custo pra embalar
tb.Label(inputs, text="Embalagem (R$)").pack(anchor=W, pady=(10, 2))
input_embalagem = tb.Entry(inputs, textvariable=var_custo_embalagem)
input_embalagem.pack(fill=X)

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

# imposto ibpt
tb.Label(inputs, text="Impostos IBPT (%)").pack(anchor=W, pady=(15, 2))
input_impostos = tb.Entry(inputs, textvariable=var_imposto_ibpt)
input_impostos.pack(fill=X)

# margem de lucro
tb.Label(inputs, text="Margem de Lucro Desejada (%)").pack(anchor=W, pady=(15, 2))
input_margem_lucro = tb.Entry(inputs, textvariable=var_margem_lucro)
input_margem_lucro.pack(fill=X)

# VARIÁVEIS PARA ATUALIZAR AS LABELS DE RESULTADO
var_resultado_custo = tb.StringVar(value="R$ 0,00")
var_resultado_minimo = tb.StringVar(value="R$ 0,00")
var_resultado_ideal = tb.StringVar(value="R$ 0,00")
var_resultado_percentual = tb.StringVar(value="0.00 %")

def calcular_precificacao():
 # Pega os valores e substitui a vírgula por ponto para conversão segura
    custo_produto = float(var_custo_produto.get().replace(',', '.'))
    frete_fornecedor = float(var_frete_fornecedor.get().replace(',', '.'))
    frete_assumido = float(var_frete_assumido.get().replace(',', '.'))
    custo_embalagem = float(var_custo_embalagem.get().replace(',', '.'))
    taxa_maquinha = float(var_taxa_maquininha.get().replace(',', '.'))
    imposto_ibpt = float(var_imposto_ibpt.get().replace(',', '.'))
    margem_de_lucro = float(var_margem_lucro.get().replace(',', '.'))
        
    custo_operacional = custo_produto + frete_fornecedor + frete_assumido + custo_embalagem
    custos_percentuais = (taxa_maquinha + imposto_ibpt) / 100
    preco_minimo = custo_operacional / (1 - custos_percentuais)
        
    # Preço Ideal com Lucro ($ Preço = \frac{Custo}{1 - \%Custos - \%Lucro}$)
    divisor = 1 - custos_percentuais - (margem_de_lucro / 100)
    preco_lucro = custo_operacional / (1 - custos_percentuais - (margem_de_lucro / 100))
        
    # ATUALIZA AS VARIÁVEIS DE TEXTO
    var_resultado_custo.set(f"R$ {custo_operacional:.2f}".replace('.', ','))
    var_resultado_minimo.set(f"R$ {preco_minimo:.2f}".replace('.', ','))
    var_resultado_ideal.set(f"R$ {preco_lucro:.2f}".replace('.', ','))
    var_resultado_percentual.set(f"{(custos_percentuais * 100):.2f} %".replace('.', ','))

botao = tb.Button(inputs, text="Calcular Preço", bootstyle=SUCCESS, command=calcular_precificacao)
botao.pack(pady=20)

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

app.mainloop()