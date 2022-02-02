#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
from datetime import datetime
import requests as rq

data = datetime.now()

base_orcamento = pd.read_excel(f'http://orcamento.sf.prefeitura.sp.gov.br/orcamento/uploads/{data.year}/basedadosexecucao{data.year}.xlsx')
base_orcamento = base_orcamento[['Cd_Orgao', 'Ds_Orgao', 'Cd_Funcao', 'Ds_Funcao', 'ProjetoAtividade', 'Ds_Projeto_Atividade', 'Vl_EmpenhadoLiquido']]
df_orgaos = base_orcamento[['Cd_Orgao', 'Ds_Orgao']].drop_duplicates()
df_orgaos = df_orgaos.sort_values(by='Ds_Orgao')
d_orgaos = df_orgaos.to_json(orient='split') #  <----
df_funcao = base_orcamento[['Cd_Funcao', 'Ds_Funcao']].drop_duplicates()
df_funcao = df_funcao.sort_values(by='Ds_Funcao')
d_funcoes = df_funcao.to_json(orient='split')#  <-----
base_orcamento = base_orcamento.to_csv('base_orcamento.csv', sep=';') #  <-----

with open('d_orgaos.json', 'w', encoding='utf-8') as f:
    json.dump(d_orgaos, f)

with open('d_funcoes.json', 'w', encoding='utf-8') as f:
    json.dump(d_funcoes, f)


base = 'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v3.0.1'
token = 'e48808721e758a773ecafba78fcc4e4'
autentificacao = {'Authorization': 'Bearer e48808721e758a773ecafba78fcc4e4'}
despesa = '/despesas'
ano_despesa = '?anoDotacao='
mes_despesa = '&mesDotacao='
funcao = '&codFuncao='
projeto = '&codProjetoAtividade='
orgao = '&codOrgao='
ano_empenho = '?anoEmpenho='
mes_empenho = '&mes_empenho'
ano_contrato = '?anoContrato='
cpf = '&numCpfCnpj='
cod_contrato = '&numContrato='
ano_receita = '?anoExercicio='
mes_receita = '&mesAteMovimento='
receita = '/movimentosReceita'
base_licitacao = 'http://gateway.apilib.prefeitura.sp.gov.br/sg/dom/v1'
data_licitacao = f'dataPublicacao='
caderno_licitacao = f'&caderno=11'
token = {'Authorization': 'Bearer fdf5ce96-d46a-341e-aa21-0cf08e7b2b83'}
licitacao = '/Licitacao?'
    

hoje_data = datetime.now()
dia_l = hoje_data.day
mes_l = hoje_data.month
ano_l = hoje_data.year
url_licitacao = base_licitacao + licitacao + data_licitacao + f'{ano_l}-{mes_l}-{dia_l}' + caderno_licitacao
requisicao_licitacao = rq.get(url_licitacao, headers=token)
requisicao_licitacao = json.loads(requisicao_licitacao.text)
while not requisicao_licitacao:
    hoje_data = datetime.now() - timedelta(days=1)
    dia_l = hoje_data.day
    mes_l = hoje_data.month
    ano_l = hoje_data.year
    url_licitacao = base_licitacao + licitacao + data_licitacao + f'{ano_l}-{mes_l}-{dia_l}' + caderno_licitacao
    requisicao_licitacao = rq.get(url_licitacao, headers=token).json()

with open('requisicao_licitacao.json', 'w', encoding='utf-8') as f:
    json.dump(requisicao_licitacao, f)

