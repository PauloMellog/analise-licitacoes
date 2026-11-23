# Análise de Licitações Públicas (DF)

Projeto em Python que coleta licitações publicadas no **PNCP (Portal Nacional de Contratações Públicas)** para analisar valores, modalidades e órgãos contratantes do Distrito Federal.

> Status: em desenvolvimento (etapa atual: coleta dos dados).

## O que o projeto faz hoje

1. **Coleta** licitações dos últimos 30 dias pela API pública de consultas do PNCP, nas modalidades Pregão Eletrônico e Dispensa de Licitação.
2. **Salva** os dados coletados em `dados/licitacoes.json`.

## Tecnologias

Python 3 e requests.

## Como rodar

```bash
pip install -r requirements.txt
python analise_licitacoes.py
```

No começo do arquivo `analise_licitacoes.py` dá para mudar o estado (`UF`), o período (`DIAS`) e as modalidades (`MODALIDADES`).

## Estrutura

```
analise_licitacoes.py   # coleta dos dados na API do PNCP
requirements.txt        # bibliotecas necessárias
dados/                  # arquivo gerado pelo script
```

## Fonte dos dados

API de consultas do PNCP, endpoint `/v1/contratacoes/publicacao`. Documentação: [Manual das APIs de Consulta do PNCP](https://www.gov.br/pncp/pt-br/acesso-a-informacao/manuais/ManualPNCPAPIConsultasVerso1.0.pdf).

## Próximos passos

As próximas etapas são tratar os dados coletados com pandas, selecionando as colunas mais úteis e convertendo valores e datas, e calcular indicadores como o valor estimado total, os órgãos com maior valor contratado e a economia entre o valor estimado e o homologado. Depois, a ideia é gerar gráficos para visualizar os resultados.
