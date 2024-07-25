from Classes.BAS_Generico import *
from Classes.BAS_Arquivo import *
from Classes.SIS_Conexao import clsConexaoBancoDados
from Classes.SIS_Tabelas import clsTabelas

app = Flask(__name__)

# -------------------------------- ARQUIVOS DE LOG
def preparaLog():
    caminho = os.getcwd() + "\ ".strip()

    dt = dtm.now()
    dtf = dt.strftime('%Y%m%d_%H%M%S')
    caminho = os.getcwd() + "\ConfigArquivos\LogExecucao\ ".strip()
    arquivoLogExecucao = f'LogExecucao_{dtf}.log'

    logExec = CriaArquivo(caminho, arquivoLogExecucao)

    if not logExec:
        mensagem = {'Mensagem:': 'Arquivo de LOG: ' + caminho + arquivoLogExecucao}
        return jsonify(mensagem)

    return logExec

def conectaBancoDados():
    conexao = clsConexaoBancoDados.ConexaoSQLServer()
    conexao.conectaArquivoConfig('', '')
    return conexao

#-----------------------------------------------------------------------------------

@app.route('/ADRRBR/cadastros/manutencao/tabelas/<string:tabela>/<string:operacao>', methods=['POST'])
def cadastrosManutencao(tabela, operacao):
    logExec = preparaLog()

    conexao = conectaBancoDados()
    if conexao.status != StatusExecucao.Sucesso:
        RegistraLinhaArquivo(logExec, conexao.mensagem, True)
        mensagem = {'Mensagem:': conexao.mensagem}
        return jsonify(mensagem)

    if not conexao.conectado:
        mensagem = {'Mensagem:': 'Não foi possível conectar ao SQL Server.'}
        return jsonify(mensagem)

    tabelaManut = clsTabelas.Tabela()
    tabelaManut.conexao = conexao
    tabelaManut.tabela = tabela

    if request.method == 'POST':
        Registro = request.json

        RegistraLinhaArquivo(logExec, str(Registro), True)

        TipoAtualizacao = None

        match operacao.upper():
            case 'INC':
                TipoAtualizacao = conexao.tipoAtualizacaoBD.Incluir
            case 'ALT':
                TipoAtualizacao = conexao.tipoAtualizacaoBD.Alterar
            case 'EXC':
                TipoAtualizacao = conexao.tipoAtualizacaoBD.Excluir

        if TipoAtualizacao == None and operacao.upper() != 'CON':
            retornoJSON = {'Mensagem:': f'ERRO-Operação para Manutenção Inválida: {operacao}. Permitido: INC / ALT / EXC / CON (Inclusão / Alteração / Exclusão / Consulta)'}
            return retornoJSON

        if operacao.upper() == 'CON':
            colunas = Registro['colunas']
            condicoes = Registro['condicoes']
            ordem = Registro['ordem']

            tabelaManut.consulta(colunas, condicoes, ordem)
        else:
            tabelaManut.prpTabela = Registro
            tabelaManut.prpTabela_atualizaBD(TipoAtualizacao)

        if tabelaManut.status in(StatusExecucao.Sucesso, StatusExecucao.Cancelado):
            RegistraLinhaArquivo(logExec, tabelaManut.mensagem, True)
            retornoJSON = tabelaManut.JSONTabela
        else:
            linha = f'{tabelaManut.status}-{tabelaManut.mensagem}'
            RegistraLinhaArquivo(logExec, linha, True)
            retornoJSON = {'Mensagem:': linha}

        return retornoJSON

app.run(port=5000,host='localhost',debug=True)

# --------------------------------

