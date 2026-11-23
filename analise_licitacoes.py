"""Análise de licitações públicas do Distrito Federal (dados do PNCP).

Etapa atual: coleta. O script coleta licitações publicadas nos últimos dias
pela API pública do PNCP (Portal Nacional de Contratações Públicas) e salva
o resultado em dados/licitacoes.json.

Como rodar:  python analise_licitacoes.py
"""

import json
import time
from datetime import date, timedelta
from pathlib import Path

import requests

# ----------------------------------------------------------------------
# Configurações (pode mudar à vontade)
# ----------------------------------------------------------------------
URL_API = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
UF = "DF"  # estado
DIAS = 30  # quantos dias para trás buscar
MODALIDADES = {  # códigos da modalidade na API do PNCP
    6: "Pregão - Eletrônico",
    8: "Dispensa de Licitação",
}
TAMANHO_PAGINA = 50  # registros por página
MAX_PAGINAS = 20  # limite de páginas por modalidade (evita demora)

PASTA_DADOS = Path("dados")


# ----------------------------------------------------------------------
# 1) Coleta
# ----------------------------------------------------------------------
def buscar_pagina(parametros):
    """Faz a requisição de uma página. Tenta até 3 vezes se der erro."""
    for _ in range(3):
        try:
            resposta = requests.get(URL_API, params=parametros, timeout=60)
        except requests.RequestException as erro:
            print(f"  erro de conexão ({erro}); tentando de novo...")
            time.sleep(3)
            continue

        if resposta.status_code == 204:  # sem conteúdo = sem resultados
            return {"data": [], "totalPaginas": 0}
        if resposta.status_code == 200:
            return resposta.json()

        print(f"  a API respondeu {resposta.status_code}; tentando de novo...")
        time.sleep(3)
    return None


def coletar_licitacoes():
    """Percorre as páginas de cada modalidade e junta os registros."""
    hoje = date.today()
    inicio = hoje - timedelta(days=DIAS)
    registros = []

    for codigo, nome in MODALIDADES.items():
        print(f"Coletando: {nome}")
        for pagina in range(1, MAX_PAGINAS + 1):
            parametros = {
                "dataInicial": inicio.strftime("%Y%m%d"),
                "dataFinal": hoje.strftime("%Y%m%d"),
                "codigoModalidadeContratacao": codigo,
                "uf": UF,
                "pagina": pagina,
                "tamanhoPagina": TAMANHO_PAGINA,
            }
            resposta = buscar_pagina(parametros)
            if resposta is None:
                print("  não consegui ler esta página; passando para a próxima modalidade")
                break

            itens = resposta.get("data", [])
            registros.extend(itens)
            print(f"  página {pagina}: {len(itens)} registros")

            if pagina >= resposta.get("totalPaginas", 0):
                break
            time.sleep(0.5)  # pausa curta para não sobrecarregar a API

    return registros


# ----------------------------------------------------------------------
# Execução
# ----------------------------------------------------------------------
def main():
    registros = coletar_licitacoes()
    if not registros:
        print("Nenhum registro encontrado. Verifique a conexão ou aumente DIAS.")
        return

    PASTA_DADOS.mkdir(exist_ok=True)
    caminho = PASTA_DADOS / "licitacoes.json"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(registros, arquivo, ensure_ascii=False, indent=2)
    print(f"\n{len(registros)} licitações salvas em {caminho}")


if __name__ == "__main__":
    main()
