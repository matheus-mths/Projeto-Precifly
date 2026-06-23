import sqlite3
import requests
import gzip
import json
import os
import sys

# descobre a pasta do exe (ou do script em desenvolvimento)
# o cache do IBPT precisa ser salvo ali pra o exe conseguir acessar
if getattr(sys, 'frozen', False):
    _PASTA = os.path.dirname(sys.executable)
else:
    _PASTA = os.path.dirname(os.path.abspath(__file__))

# essa função baixa a tabela de impostos do IBPT pra um estado específico
# a tabela vem comprimida em .gz, então precisamos descompactar antes de usar
def baixar_tabela_ibpt(uf: str) -> list:
    # pega os metadados pra saber qual é a versão mais recente da tabela
    meta = requests.get("https://ibpt.valraw.com.br/api/meta.json").json()
    ano = str(meta["anos"][0])
    versao = meta["versoes"][ano][-1]

    # monta a URL e baixa o arquivo
    url = f"https://ibpt.valraw.com.br/api/{ano}/{versao}/ncm/{uf}.json.gz"
    response = requests.get(url)

    # descomprime o arquivo e transforma em lista
    dados = json.loads(gzip.decompress(response.content))
    return dados["dados"]

# essa função busca as alíquotas de imposto de um produto pelo NCM e estado (UF)
# se a tabela do estado já foi baixada antes, usa o arquivo salvo (cache)
# senão, baixa da internet e salva pra não precisar baixar de novo
def buscar_aliquotas(ncm: str, uf: str) -> dict:
    cache_path = os.path.join(_PASTA, f"ibpt_{uf}.json")

    if not os.path.exists(cache_path):
        print(f"Baixando tabela IBPT para {uf}...")
        dados = baixar_tabela_ibpt(uf)
        # salva o arquivo pra usar nas próximas vezes
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(dados, f)
    else:
        # já tem o arquivo salvo, só carrega ele
        with open(cache_path, encoding="utf-8") as f:
            dados = json.load(f)

    # procura o NCM na lista
    for item in dados:
        if item["codigo"] == ncm:
            return item

    # se não encontrou, retorna None
    return None

# essa função calcula o preço final de um produto e salva os dados no banco
def calcular_preco(produto_nome: str, custo: float, margem: float, uf: str, usuario_id: int) -> dict:
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    # busca o NCM do produto no banco de dados
    cursor.execute("SELECT NCM FROM produtos WHERE nome = ?", (produto_nome,))
    produto = cursor.fetchone()

    if not produto:
        conexao.close()
        return {"erro": "Produto não encontrado"}

    ncm = produto[0]

    # atualiza o custo, margem e UF do produto no banco
    cursor.execute("""
        UPDATE produtos SET custo = ?, margem_lucro = ?, uf = ?
        WHERE nome = ? AND usuario_id = ?
    """, (custo, margem, uf, produto_nome, usuario_id))
    conexao.commit()
    conexao.close()

    # busca os impostos do IBPT pra esse NCM e estado
    aliquotas = buscar_aliquotas(ncm, uf)

    if not aliquotas:
        return {"erro": f"NCM {ncm} não encontrado na tabela IBPT"}

    # soma as alíquotas federal + estadual + municipal
    ibpt = (
        float(aliquotas["aliquotaNacionalFederal"]) +
        float(aliquotas["aliquotaEstadual"]) +
        float(aliquotas["aliquotaMunicipal"])
    ) / 100

    # calcula o preço final
    margem_dec = margem / 100
    valor_imposto = custo * ibpt
    custo_total = custo + valor_imposto
    preco_final = custo_total * (1 + margem_dec)
    lucro = preco_final - custo_total

    return {
        "ncm": ncm,
        "uf": uf,
        "ibpt_pct": round(ibpt * 100, 2),
        "margem_pct": round(margem, 2),
        "custo_total": round(custo_total, 2),
        "preco_final": round(preco_final, 2),
        "valor_imposto": round(valor_imposto, 2),
        "lucro_liquido": round(lucro, 2)
    }
