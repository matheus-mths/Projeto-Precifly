import ttkbootstrap as tb
from ttkbootstrap.constants import * # para ser possível deixar alinhado, não ter espaços em branco e tals

# criando janla
app = tb.Window(themename="flatly")
app.title("Sistema Inteligente de Precificação")
app.geometry("1440x1024")

titulo = tb.Label(app, text="Sistema Inteligente de Precificação", font=("Segoe UI", 22, "bold"))
titulo.pack(pady=20)

# precisamos criar um "fundo" para "guardar" as coisas, como os inputs e os resultados
fundo_dados = tb.Frame(app)
fundo_dados.pack(fill=BOTH, expand=True, padx=20, pady=10)

# inputs
inputs = tb.Labelframe(fundo_dados, text="Dados do Produto", padding=20, bootstyle="primary")
inputs.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10)) 
# nome do produto
tb.Label(inputs, text="Produto").pack(anchor=W, pady=(10, 2)) 
input_produto = tb.Entry(inputs, width=25)
input_produto.pack(fill=X)

# custo do produto
tb.Label(inputs, text="Custo do Produto (R$)").pack(anchor=W, pady=(10, 2))
input_custo = tb.Entry(inputs)
input_custo.pack(fill=X)

# frete fornecedor (se houver, o lojista coloca, ele não é obrigado a colocar. ou ele põe zero)
tb.Label(inputs, text="Frete do Fornecedor (R$)").pack(anchor=W, pady=(10, 2))
input_frete_fornecedor = tb.Entry(inputs)
input_frete_fornecedor.pack(fill=X)

# frete assumido (na venda, se houver. ou ele põe zero)
tb.Label(inputs, text="Frete Assumido pelo Vendedor (R$)").pack(anchor=W, pady=(10, 2))
input_frete_assumido = tb.Entry(inputs)
input_frete_assumido.pack(fill=X)

# custo pra embalar
tb.Label(inputs, text="Embalagem (R$)").pack(anchor=W, pady=(10, 2))
input_embalagem = tb.Entry(inputs)
input_embalagem.pack(fill=X)

# marketplace
tb.Label(inputs, text="Marketplace").pack(anchor=W, pady=(15, 5))

marketplace_checks = tb.Frame(inputs) #fundo para colocar os checks
marketplace_checks.pack(fill=X)

#criando variáveis do tipo boolean para colocar nos checks pro sistema reconhecer qual foi selecionado
mercado_livre = tb.BooleanVar()
shopee = tb.BooleanVar()
amazon = tb.BooleanVar()
magalu = tb.BooleanVar()

#checks
tb.Checkbutton(marketplace_checks, text="Mercado Livre", variable=mercado_livre, bootstyle="success-round-toggle").pack(anchor=W)
tb.Checkbutton(marketplace_checks, text="Shopee", variable=shopee, bootstyle="success-round-toggle").pack(anchor=W)
tb.Checkbutton(marketplace_checks, text="Amazon", variable=amazon, bootstyle="success-round-toggle").pack(anchor=W)
tb.Checkbutton(marketplace_checks, text="Magalu", variable=magalu, bootstyle="success-round-toggle").pack(anchor=W)

# taxa da maquininha
tb.Label(inputs, text="Taxa da Maquininha (%)").pack(anchor=W, pady=(15, 2))
input_taxa_maquininha = tb.Entry(inputs)
input_taxa_maquininha.pack(fill=X)

# imposto ibpt
tb.Label(inputs, text="Impostos IBPT (%)").pack(anchor=W, pady=(15, 2))
input_impostos = tb.Entry(inputs)
input_impostos.pack(fill=X)

# margem de lucro
tb.Label(inputs, text="Margem de Lucro Desejada (%)").pack(anchor=W, pady=(15, 2))
input_margem_lucro = tb.Entry(inputs)
input_margem_lucro.pack(fill=X)

def funcao_botao():
    print("teste")

meu_botao = tb.Button(inputs, text="Calcular Preço", bootstyle="success", command=funcao_botao)
meu_botao.pack(pady=20)


# rasultados da precificação
resultados = tb.Labelframe(fundo_dados, text="Resultados da Precificação", padding=20, bootstyle="success")
resultados.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))

card_custo_total = tb.Frame(resultados, bootstyle='danger')
card_custo_total.pack(fill=X, pady=10)
tb.Label(card_custo_total, text='Custos Totais', font=("Segoe UI", 12, "bold")).pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_custo_total, text="R$ 0,00", font=("Segoe UI", 20, "bold")).pack(anchor=W, padx=15, pady=(5, 10))

card_preco_min = tb.Frame(resultados, bootstyle='warning')
card_preco_min.pack(fill=X, pady=10)
tb.Label(card_preco_min, text='Preço Mínimo', font=("Segoe UI", 12, "bold")).pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_preco_min, text="R$ 0,00", font=("Segoe UI", 20, "bold")).pack(anchor=W, padx=15, pady=(5, 10))

card_preco_ideal = tb.Frame(resultados, bootstyle='success')
card_preco_ideal.pack(fill=X, pady=10)
tb.Label(card_preco_ideal, text='Preço Ideal', font=("Segoe UI", 12, "bold")).pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_preco_ideal, text="R$ 0,00", font=("Segoe UI", 20, "bold")).pack(anchor=W, padx=15, pady=(5, 10))

card_lucro = tb.Frame(resultados, bootstyle='info')
card_lucro.pack(fill=X, pady=10)
tb.Label(card_lucro, text='Preço Mínimo', font=("Segoe UI", 12, "bold")).pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_lucro, text="R$ 0,00", font=("Segoe UI", 20, "bold")).pack(anchor=W, padx=15, pady=(5, 10))

card_total_impostos = tb.Frame(resultados, bootstyle='primary')
card_total_impostos.pack(fill=X, pady=10)
tb.Label(card_total_impostos, text='Preço Mínimo', font=("Segoe UI", 12, "bold")).pack(anchor=W, padx=15, pady=(10, 0))
tb.Label(card_total_impostos, text="R$ 0,00", font=("Segoe UI", 20, "bold")).pack(anchor=W, padx=15, pady=(5, 10))



app.mainloop()