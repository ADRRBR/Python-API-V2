import sys

from Classes.BAS_Generico import *
from Classes.BAS_Arquivo import *
from Classes.SIS_Conexao import clsConexaoBancoDados

# ************************************
# Sub Rotina para Executar os Scripts
# ************************************
def executaScriptSQL(caminho, nomeArqScript, conexao, nomeArqlogExec):
    # --- Verifica o Arquivo de Script
    if not ExisteArquivo(caminho, nomeArqScript):
        RegistraLinhaArquivo(nomeArqlogExec, f'O arquivo de script não foi localizado em: {caminho + nomeArqScript}.', True)
        return

    # --- Executa/Aplica o Script
    RegistraLinhaArquivo(nomeArqlogExec, f'Preparando para executar/aplicar o script do arquivo: {caminho + nomeArqScript}...', True)

    conexao.executaArquivoScriptSQL(caminho, nomeArqScript)
    if conexao.status != StatusExecucao.Sucesso:
        RegistraLinhaArquivo(nomeArqlogExec, conexao.mensagem, True)
        return(conexao.mensagem)

    RegistraLinhaArquivo(nomeArqlogExec,f'O arquivo de script: {caminho + nomeArqScript} foi executado/aplicado com sucesso no banco de dados {conexao.bancoDados}',True)

    return 'Script Executado com Sucesso!'

# ************************************
#         INÍCIO DA ROTINA
# ************************************

# ----- Arquivo de LOG
caminho = os.getcwd() + "\ConfigArquivos\LogExecucao\ ".strip()

dt = dtm.now()
dtf = dt.strftime('%Y%m%d_%H%M%S')
arquivoLogExecucao = f'LogScript_{dtf}.log'

logExec = CriaArquivo(caminho, arquivoLogExecucao)
if not logExec:
    sys.exit(f'Arquivo de LOG: {caminho}{arquivo}')

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

# ----- Executa/Aplica os Scripts
caminho = conexao.caminhoArquivosScriptSQL

arquivoScriptSQL = "_0_0_0_PRC_Drop.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_0_0_PRC_SQL_Estrutura_2012.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_0_1_PRC_SQL_Indices.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_1_PRC_SIS_Tabela_Temp.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_2_PRC_SQL_Colunas_Chave_Primaria.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_3_PRC_SQL_Coluna_Tabela.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_4_PRC_SQL_Verifica_Registro_Exclusivo.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_5_PRC_SQL_Grava_Registro.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_6_PRC_SQL_Exclui_Registro.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

arquivoScriptSQL = "_7_PRC_SQL_Pesquisa_Registros.sql"
RegistraLinhaArquivo(logExec,'', True)
mensagem = executaScriptSQL(caminho, arquivoScriptSQL, conexao, logExec)
RegistraLinhaArquivo(logExec,mensagem, True)

sys.exit ('Fim do Processamento!')






