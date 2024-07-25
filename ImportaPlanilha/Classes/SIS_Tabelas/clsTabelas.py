from Classes.BAS_Generico import *

class Tabela:
    def __init__(self):
        self.__nomeTabela = ' '
        self.__prpTabela = []
        self.__lstTabela = []
        self.__JSONTabela = ' '
        self.__status = StatusExecucao.SemRequisicao
        self.__mensagem = ' '

    # Nome da Tabela
    @property
    def tabela(self):
        return self.__nomeTabela

    @tabela.setter
    def tabela(self, valor):
        self.__nomeTabela = valor

    # Lista de Propriedades (Colunas da Tabela)
    @property
    def prpTabela(self):
        return self.__prpTabela

    @prpTabela.setter
    def prpTabela(self, valor):
        self.__prpTabela = [] # Limpa para ter Sempre um Elemento (Dicionário na Lista)
        self.__prpTabela.append(valor)

    # Objeto da Conexão
    @property
    def conexao(self):
        return self.__conexao

    @conexao.setter
    def conexao(self, valor):
        self.__conexao = valor

    # Registros Resultado de Consulta
    @property
    def lstTabela(self):
        return self.__lstTabela

    # Registros Resultado de Consulta (JSON)
    @property
    def JSONTabela(self):
        return self.__JSONTabela

    # Status
    @property
    def status(self):
        return self.__status

    # Mensagem
    @property
    def mensagem(self):
        return self.__mensagem

    # (prpTabela_atualizaBD) Método que Executa/APLICA a Atualização do Tabela no Banco de Dados, Conforme o Tipo de Atualização
    def prpTabela_atualizaBD(self, tipoAtualizacaoBD):
        self.__LimpaStatus()

        if not self.__VerificaConexao():
            return

        if not self.__VerificaTabela():
            return

        dic_RegistroManut = self.__prpTabela[0]

        colunasConteudos = ''
        colunas = ''

        indice = 0
        for chave, valor in dic_RegistroManut.items():
            indice += 1

            if indice == 1:
                idRegistro = valor
            else:
                colunasConteudos += f'{chave}={valor},'

            colunas += f'{chave},'

        colunasConteudos = colunasConteudos[0:colunasConteudos.__len__() - 1]
        colunas = colunas[0:colunas.__len__() - 1]

        if tipoAtualizacaoBD == self.__conexao.tipoAtualizacaoBD.Incluir:
            sComando = "EXEC dbo.PRC_SQL_GRAVA_REGISTRO " + "'" + self.__nomeTabela + "','" + "INC" + "','" + colunasConteudos + "'"
            sMensagem = 'Registro inserido com sucesso!'

        elif tipoAtualizacaoBD == self.__conexao.tipoAtualizacaoBD.Alterar:
            sComando = "EXEC dbo.PRC_SQL_GRAVA_REGISTRO " + "'" + self.__nomeTabela + "','" + "ALT" + "','" + colunasConteudos + "'," + f'{idRegistro}'
            sMensagem = 'Registro alterado com sucesso!'

        elif tipoAtualizacaoBD == self.__conexao.tipoAtualizacaoBD.Excluir:
            sComando = "EXEC dbo.PRC_SQL_EXCLUI_REGISTRO " + "'" + self.__nomeTabela + "','" + "ESP" + "'," + f'{idRegistro}'
            sMensagem = 'Registro excluído com sucesso!'

        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Tipo de atualização inválido.'
            return

        retorno = self.__conexao.executaSQL(sComando, True)

        self.__status = self.__conexao.status
        self.__mensagem = self.__conexao.mensagem

        if self.__status != StatusExecucao.Sucesso:
            return

        self.__RetornaExecucao(colunas, retorno, sMensagem)

    # (consulta) Método que Efetua uma Consulta de Todas as Colunas da Tabela, Conforme o Critério Informado
    def consulta(self, SQLColunas, SQLWhere, SQLOrderBY):
        self.__LimpaStatus()

        if not self.__VerificaConexao():
            return

        if not self.__VerificaTabela():
            return

        if not self.__VerificaParametrosConsulta(SQLWhere):
            return

        sComando = "EXEC dbo.PRC_SQL_PESQUISA_REGISTROS " + "'" + self.__nomeTabela + "','" + SQLColunas + "','" + SQLOrderBY + "','" + SQLWhere + "'"

        retorno = self.__conexao.executaSQL(sComando, True)

        self.__status = self.__conexao.status
        self.__mensagem = self.__conexao.mensagem

        if self.__status != StatusExecucao.Sucesso:
            return

        self.__RetornaExecucao(SQLColunas, retorno, 'Consulta efetuada com sucesso')

    # Métodos Privados
    def __VerificaConexao(self):
        try:
            if not self.__conexao.conectado:
                self.__status = StatusExecucao.Erro
                self.__mensagem = 'O objeto não está conectado ao banco de dados'
                return False
            return True
        except AttributeError as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = ('Informe a propriedade < .conexao > para conexão com o banco de dados.')
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}.' + ' Ao tentar conexão com o banco de dados.')
        return False

    def __VerificaTabela(self):
        if self.__nomeTabela == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Informe o Nome da Tabela'
            return False
        return True

    def __VerificaParametrosConsulta(self, CondicaoSQLWhere):
        if CondicaoSQLWhere == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Informe a Condição SQL Where'
            return False
        return True

    def __RetornaExecucao(self, SQLColunas, retorno, mensagem):
        self.__lstTabela = []

        # Inicia o Retorno JSON
        TabelaJSON = []
        retornoJSON = []
        tipoRetornoPRC = ''

        if len(retorno) > 0:
            tipoRetornoPRC = str(retorno[0][0]).upper()

        if tipoRetornoPRC.find('PRC-RET') == 0:
            self.__status = StatusExecucao(retorno[0][1])
            self.__mensagem = retorno[0][2]
            qtdRegistros = 0
        else:
            self.__mensagem = mensagem
            qtdRegistros = len(retorno)

            nomesColunas = SQLColunas.split(',')

            for registro in range(qtdRegistros):
                conteudo = retorno[registro][0:]
                qtdColunas = len(conteudo)

                dic_ColunaConteudo = {}

                for coluna in range(qtdColunas):
                    nome = nomesColunas[coluna]
                    conteudo = retorno[registro][coluna]
                    tipoDado = str(type(conteudo)).upper()

                    if tipoDado.find("DATETIME") > 0:
                        conteudo = str(conteudo)

                    dic_ChaveValor = {nome: conteudo}
                    dic_ColunaConteudo.update(dic_ChaveValor)

                self.__lstTabela.append(dic_ColunaConteudo)

            TabelaJSON = self.__lstTabela

        # Retorno JSON
        retornoJSON.append({'Mensagem:': self.__mensagem,
                            'Quantidade:': qtdRegistros
                          })
        retornoJSON.append({'Registros:': TabelaJSON})

        self.__JSONTabela = json.dumps(retornoJSON, cls=NpEncoder, indent=4)

        return

    def __LimpaStatus(self):
        self.__Status = StatusExecucao.SemRequisicao
        self.__mensagem = ' '


