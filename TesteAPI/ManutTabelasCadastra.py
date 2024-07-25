from Classes.BAS_Generico import *

link = 'http://localhost:5000/ADRRBR/cadastros/manutencao/tabelas'

tipoRequisicao = 'POST'
tabela         = 'TAB_CLIENTES'
operacao       = 'ALT'

link += '/' + tabela + '/' + operacao

if operacao.upper() == "CON":
    registroJSON = ' '
    registroJSON += '{'
    registroJSON += '"colunas": "pk_cliente,codigo,nome,descricao,data_primeiro_contato,valor_faturamento,data_renovacao,hora_diaria_ligacao,valor_primeira_compra",'
    registroJSON += '"ordem": "nome",'
    registroJSON += '"condicoes": "1=1"'
    registroJSON += '}'
else:
    registroJSON = ' '
    registroJSON += '{'
    registroJSON += '"pk_cliente": 278,'
    registroJSON += '"codigo": "1",'
    registroJSON += '"nome": "GUILHERME RIBEIRO",'
    registroJSON += '"descricao": "FILHO",'
    registroJSON += '"data_primeiro_contato": "2024-07-04 01:10",'
    registroJSON += '"valor_faturamento": 1150.25,'
    registroJSON += '"data_renovacao": "2025-07-04",'
    registroJSON += '"hora_diaria_ligacao": "07:17",'
    registroJSON += '"valor_primeira_compra": 150'
    registroJSON += '}'

dic_RegistroJSON = json.loads(registroJSON)

retorno = requests.post(url=link, json=dic_RegistroJSON)

if str(retorno) != '<Response [200]>':
    sys.exit(f'A requisição falhou. {retorno}')

retorno = retorno.json()

print(retorno)


