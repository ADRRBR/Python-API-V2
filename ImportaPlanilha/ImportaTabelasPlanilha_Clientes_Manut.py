from Classes.BAS_Generico import *
from Classes.BAS_Arquivo import *
from Classes.SIS_Conexao import clsConexaoBancoDados
from Classes.APL_Planilha import clsPlanilha
from Classes.SIS_Tabelas import clsTabelas

# -------------------------------- ARQUIVOS DE LOG

caminho = os.getcwd() + "\ConfigArquivos\LogExecucao\ ".strip()

dt = dtm.now()
dtf = dt.strftime('%Y%m%d_%H%M%S')
arquivoLogExecucao = f'LogExecucao_{dtf}.log'
arquivoLogManutencao =  f'LogManutencao_{dtf}.log'

logExec = CriaArquivo(caminho, arquivoLogExecucao)
if not logExec:
    sys.exit(f'Arquivo de LOG: {caminho}{arquivoLogExecucao}')

logManut = CriaArquivo(caminho, arquivoLogManutencao)
if not logExec:
    sys.exit(f'Arquivo de LOG: {caminho}{arquivoLogManutencao}')

# -------------------------------- CONEXÃO COM O BANDO DE DADOS

RegistraLinhaArquivo(logExec,'Preparando o Acesso à Classe < Conexao >...', True)
RegistraLinhaArquivo(logExec,'Conectando ao banco de dados...', True)

conexao = clsConexaoBancoDados.ConexaoSQLServer()
conexao.conectaArquivoConfig('', '')
if conexao.status != StatusExecucao.Sucesso:
    RegistraLinhaArquivo(logExec, conexao.mensagem, True)
    sys.exit(conexao.mensagem)

if conexao.conectado:
    RegistraLinhaArquivo(logExec, 'A conexão com o SQL Server foi bem sucedida!', True)
else:
    RegistraLinhaArquivo(logExec, 'Não foi possível conectar ao SQL Server.', True)

# -------------------------------- OPERAÇÃO E LEITURA DA PLANILHA PARA MANUTENÇÃO

caminhoPlanilha = os.getcwd() + "\ ".strip()
nomePlanilha = 'Clientes_Manut.xlsx'
tabela = 'TAB_CLIENTES'
operacao = 'INC'

TipoAtualizacao = None

match operacao.upper():
    case 'INC':
        pastaTrabalhoPlanilha = 'Inclusão'
        TipoAtualizacao = conexao.tipoAtualizacaoBD.Incluir
    case 'ALT':
        pastaTrabalhoPlanilha = 'Alteração'
        TipoAtualizacao = conexao.tipoAtualizacaoBD.Alterar
    case 'EXC':
        pastaTrabalhoPlanilha = 'Exclusão'
        TipoAtualizacao = conexao.tipoAtualizacaoBD.Excluir
    case 'CON':
        pastaTrabalhoPlanilha = 'Consulta'

if TipoAtualizacao == None and operacao.upper() != 'CON':
    sMensagem = 'Operação para Manutenção Inválida: {operacao}. Permitido: INC / ALT / EXC / CON (Inclusão / Alteração / Exclusão / Consulta)'
    RegistraLinhaArquivo(logExec, sMensagem, True)
    sys.exit(sMensagem)

RegistraLinhaArquivo(logExec, 'Preparando o Acesso à Classe < Planilha >...', True)

planilha = clsPlanilha.Planilha()
planilha.planilhaCaminho = caminhoPlanilha
planilha.planilhaNome = nomePlanilha
planilha.pastaTrabalho = pastaTrabalhoPlanilha
planilha.faixaCelulas = 'A:I'
planilha.linhaInicial = 1
planilha.linhaFinal = 50000

RegistraLinhaArquivo(logExec,'Preparando para ler a planilha...', True)

tabPlan = planilha.lerPlanilha()
if planilha.status != StatusExecucao.Sucesso:
    RegistraLinhaArquivo(logExec, planilha.mensagem, True)
    sys.exit(planilha.mensagem)

qtdeLinhas = len(tabPlan)

# Identifica e Separa o Cabeçalho da Planilha
dic_Cabecalho = tabPlan.head().to_dict()
nomesColunas = ''
for chave, valor in dic_Cabecalho.items():
    nomesColunas += f'{chave},'
nomesColunas = nomesColunas[0:nomesColunas.__len__() - 1]
nomesColunas = nomesColunas.split(',')
nomesColunas = list(nomesColunas)
qtdeColunas = len(nomesColunas)

RegistraLinhaArquivo(logExec, 'Preparando o Acesso/Manutenção à Classe < Tabelas >...', True)

tabelaManut = clsTabelas.Tabela()
tabelaManut.conexao = conexao
tabelaManut.tabela = tabela

for linha in range(qtdeLinhas):
     dic_Registro = {}

     # Dados da Planilha
     for coluna in range(qtdeColunas):
         coluna = nomesColunas[coluna]
         conteudo = tabPlan.loc[linha][coluna]
         tipoDado = str(type(conteudo)).upper()

         if tipoDado.find("TIMESTAMP") > 0 or tipoDado.find("DATETIME") > 0:
             conteudo = str(conteudo)

         RegistraLinhaArquivo(logManut, f'Planilha-Linha: {linha+1} - {coluna} = {conteudo}', True)

         dic_ChaveValor = {coluna: conteudo}
         dic_Registro.update(dic_ChaveValor)

     # Manutenção na Tabela
     tabelaManut.prpTabela = dic_Registro
     tabelaManut.prpTabela_atualizaBD(TipoAtualizacao)

     RegistraLinhaArquivo(logManut, '', True)

     if tabelaManut.status == StatusExecucao.Sucesso:
         RegistraLinhaArquivo(logManut, tabelaManut.mensagem + ' - ' + str(tabelaManut.lstTabela), True)
     else:
         RegistraLinhaArquivo(logManut, tabelaManut.mensagem, True)

     RegistraLinhaArquivo(logManut, str('='*80), True)

# --------------------------------
