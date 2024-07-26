import pandas as pd
from Classes.BAS_Generico import *
from Classes.BAS_Arquivo import *

# Tipos de Atualização no Banco de Dados
class TipoAtualizacaoBD(Enum):
    Incluir = 0
    Alterar = 1
    Excluir = 2

class ConexaoSQLServer:
    def __init__(self):
        self.__servidor = ' '
        self.__bancoDados = ' '
        self.__usuario = ' '
        self.__senha = ' '
        self.__caminhoArquivosScriptSQL = ' '
        self.__conectado = False
        self.__status = StatusExecucao.SemRequisicao
        self.__mensagem = ' '
        self.__tipoAtualizacaoBD = TipoAtualizacaoBD

    # Servidor
    @property
    def servidor(self):
        return self.__servidor

    @servidor.setter
    def servidor(self, valor):
        if type(valor) == type(self.__servidor):
            self.__servidor = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Banco de Dados
    @property
    def bancoDados(self):
        return self.__bancoDados

    @bancoDados.setter
    def bancoDados(self, valor):
        if type(valor) == type(self.__bancoDados):
            self.__bancoDados = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Usuario
    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, valor):
        if type(valor) == type(self.__usuario):
            self.__usuario = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Senha
    @property
    def senha(self):
        return "**********"

    @senha.setter
    def senha(self, valor):
        if type(valor) == type(self.__senha):
            self.__senha = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Caminho para os Arquivos de Script SQL Server
    @property
    def caminhoArquivosScriptSQL(self):
        return self.__caminhoArquivosScriptSQL

    @caminhoArquivosScriptSQL.setter
    def caminhoArquivosScriptSQL(self, valor):
        if type(valor) == type(self.__caminhoArquivosScriptSQL):
            self.__caminhoArquivosScriptSQL = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Tipos de Atualização on Banco de Dados
    @property
    def tipoAtualizacaoBD(self):
        return self.__tipoAtualizacaoBD

    # Status
    @property
    def status(self):
        return self.__status

    # Mensagem
    @property
    def mensagem(self):
        return self.__mensagem

    # Conectado
    @property
    def conectado(self):
        return self.__conectado

    # Objeto da Conexão
    @property
    def conexao(self):
        return self.__conexao

    # (Conecta) Método que Efetua a Conexão Conforme o Usuário do Banco de Dados Informado
    def conecta(self):
        self.__LimpaStatus()

        if not self.__VerificaParametrosConexao(False):
            self.__conectado = False
            return

        sConexao = ("Driver={SQL Server};")
        sConexao += ("Server=" + self.__servidor + ";")
        sConexao += ("Database=" + self.__bancoDados + ";")
        sConexao += ("Trusted_Connection=no;")  #"yes" (Conexão SQL Automática (ignora UID e PWD)
        sConexao += ("UID=" + self.__usuario + ";")
        sConexao += ("PWD=" + self.__senha)

        try:
            self.__conexao = pyodbc.connect(sConexao)
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}.' + ' Ao tentar conexão com o banco de dados.')
            self.__conectado = False
        else:
            self.__status = StatusExecucao.Sucesso
            self.__conectado = True

    # (conectaAutentWindows) Método que Efetua a Conexão Conforme a Autenticação do Windows (SQLServer).
    # Este Método Ignora os Parâmetros Informados para o Usuário do Banco de Dados e Senha, pois o Tipo de Conexão não os Utiliza.
    def conectaAutentWindows(self):
        self.__LimpaStatus()

        if not self.__VerificaParametrosConexao(True):
            self.__conectado = False
            return

        sConexao = ("Driver={SQL Server};")
        sConexao += ("Server=" + self.__servidor + ";")
        sConexao += ("Database=" + self.__bancoDados + ";")
        sConexao += ("Trusted_Connection=no")  #"yes" (Conexão SQL Automática (ignora UID e PWD)

        try:
            self.__conexao = pyodbc.connect(sConexao)
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}.' + ' Ao tentar conexão com o banco de dados.')
            self.__conectado = False
        else:
            self.__status = StatusExecucao.Sucesso
            self.__conectado = True

    # (conectaArquivoConfig) Método que Efetua a Conexão Conforme a Parametrização em um Arquivo de Configuração.
    def conectaArquivoConfig(self, CaminhoArquivo, NomeArquivo):
        self.__LimpaStatus()

        __CaminhoArquivo = CaminhoArquivo
        __NomeArquivo = NomeArquivo

        #Arquivo de Configuração não Informado, Assume o Caminho e Nome Padrão
        if (__CaminhoArquivo == '' or __NomeArquivo == ''):
            __CaminhoArquivo = os.getcwd() + "\ConfigArquivos\ ".strip()
            __NomeArquivo = 'ConfigSQLServer.txt'

        if not ExisteArquivo(__CaminhoArquivo, __NomeArquivo):
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'O arquivo de configuração para conexão com o SQL Server não foi localizado em ' + __CaminhoArquivo + __NomeArquivo + '. Método < conectaArquivoConfig >'
            return

        try:
            arq = AbreArquivo(__CaminhoArquivo, __NomeArquivo)
            if arq == False:
                self.__status = StatusExecucao.Erro
                self.__mensagem = 'Não foi possível ler o arquivo de configuração para conexão com o SQL Server em ' + __CaminhoArquivo + __NomeArquivo + '. Método < conectaArquivoConfig >'
                return

            linhas = arq.readlines()

            for linha in linhas:
                if linha.find('[TIPO CONEXAO SQL SERVER]') == 0:
                    vAux = linha.split('|')
                    vAutentWindows = vAux[1]
                    vAutentWindows = vAutentWindows.strip()
                    if vAutentWindows == 'AUTENTICACAO WINDOWS':
                        vAutentWindows = True
                        vMetodoConexao = 'conectaAutentWindows'
                    else:
                        vAutentWindows = False
                        vMetodoConexao = 'conecta'

                elif linha.find('[SERVIDOR SQL SERVER]') == 0:
                    vAux = linha.split('|')
                    self.__servidor = vAux[1]
                    self.__servidor = self.__servidor.strip()

                elif linha.find('[BANCO DADOS SQL SERVER]') == 0:
                    vAux = linha.split('|')
                    self.__bancoDados = vAux[1]
                    self.__bancoDados = self.__bancoDados.strip()

                elif linha.find('[USUARIO SQL SERVER]') == 0:
                    vAux = linha.split('|')
                    self.__usuario = vAux[1]
                    self.__usuario = self.__usuario.strip()

                elif linha.find('[SENHA SQL SERVER]') == 0:
                    vAux = linha.split('|')
                    self.__senha = vAux[1]
                    self.__senha = self.__senha.strip()

                elif linha.find('[CAMINHO ARQUIVOS SCRIPT SQL SERVER]') == 0:
                    vAux = linha.split('|')
                    self.__caminhoArquivosScriptSQL = vAux[1]
                    self.__caminhoArquivosScriptSQL = self.__caminhoArquivosScriptSQL.strip()

            arq.close()

        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = f'Ocorreu o erro {erro}.' + ' Ao tentar ler o arquivo de configuração para conexão com o banco de dados SQL Server. Método < conectaArquivoConfig >'
            arq.close()
            return

        # Efetua a conexão com base nos parâmetros recuperados do arquivo de configuração
        try:
            if vAutentWindows:
                self.conectaAutentWindows()
            else:
                self.conecta()
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = f'Ocorreu o erro {erro}. Ao executar o método < {vMetodoConexao} >'
        else:
            if self.__status != StatusExecucao.Sucesso:
                self.__mensagem += f'. Ao executar o método < {vMetodoConexao} >'

    # (executaArquivoScriptSQL) Método que Executa/Aplica um Script SQL Conforme o Conteúdo de um Arquivo.
    def executaArquivoScriptSQL(self, CaminhoArquivo, NomeArquivo):
        self.__LimpaStatus()

        __CaminhoArquivo = CaminhoArquivo
        __NomeArquivo = NomeArquivo

        if not ExisteArquivo(__CaminhoArquivo, __NomeArquivo):
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'O arquivo de script não foi localizado em ' + __CaminhoArquivo + __NomeArquivo + '. Método < executaArquivoScript >'
            return

        try:
            arq = AbreArquivo(__CaminhoArquivo, __NomeArquivo)
            if arq == False:
                self.__status = StatusExecucao.Erro
                self.__mensagem = 'Não foi possível ler o arquivo de script em ' + __CaminhoArquivo + __NomeArquivo + '. Método < executaArquivoScript >'
                return

            linhas = arq.readlines()

            script = ' '
            for linha in linhas:
                script += linha

            arq.close()

        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = f'Ocorreu o erro {erro}.' + ' Ao tentar ler o arquivo de script. Método < executaArquivoScript >'
            arq.close()
            return

        # Execupa/Aplica o Script
        try:
            self.executaSQL(script, False)
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = f'Ocorreu o erro {erro}. Ao executar o método < executaArquivoScript >'
        else:
            if self.__status != StatusExecucao.Sucesso:
                self.__mensagem += f'. Ao executar o método < executaArquivoScript >'

    # (executaSQL) Método que Executa uma Instrução, Conforme a Cáusula Informada
    def executaSQL(self, SQL, retornar):
        self.__LimpaStatus()

        if not self.__VerificaConexao():
            return

        cursor = self.__conexao.cursor()

        try:
            cursor.execute(SQL)
            if retornar:
                retorno = cursor.fetchall()
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o comando {SQL}.')
            return

        cursor.commit()
        cursor.close()

        self.__status = StatusExecucao.Sucesso

        if retornar:
            return retorno

    # (consulta) Método que Efetua uma Consulta, Conforme a Cláusula Informada
    def consultaSQL(self, SQL):
        self.__LimpaStatus()

        if not self.__VerificaConexao():
            return

        try:
            tabSQL = pd.read_sql(SQL, self.__conexao)
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o comando {SQL}.')
            return

        if len(tabSQL) == 0:
            self.__status = StatusExecucao.NaoEncontrado
            self.__mensagem = 'Nenhum registro foi encontrado para a consulta requisitada.'
            return

        self.__status = StatusExecucao.Encontrado

        return tabSQL

    # (dataListar) Método que Lista a Data Gravada Formatando
    def dataListar(self, dataGravada):
        self.__LimpaStatus()

        tipoDado = str(type(dataGravada)).upper()

        if tipoDado.find("STR") > 0:
            self.__status = StatusExecucao.Sucesso
            return dataGravada

        try:
            dataformat = dataGravada.strftime('%d/%m/%Y')
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < dataListar >')
            return

        self.__status = StatusExecucao.Sucesso

        return dataformat

    # (horaListar) Método que Lista a Hora Gravada Formatando
    def horaListar(self, horaGravada):
        self.__LimpaStatus()

        tipoDado = str(type(horaGravada)).upper()

        if tipoDado.find("STR") > 0:
            self.__status = StatusExecucao.Sucesso
            return horaGravada

        try:
            horaformat = horaGravada.strftime('%H:%M:%S')
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < horaListar >')
            return

        self.__status = StatusExecucao.Sucesso

        return horaformat

    # (datahoraListar) Método que Lista a Data e a Hora Gravada Formatando
    def datahoraListar(self, datahoraGravada):
        self.__LimpaStatus()

        tipoDado = str(type(datahoraGravada)).upper()

        if tipoDado.find("STR") > 0:
            self.__status = StatusExecucao.Sucesso
            return datahoraGravada

        try:
            datahoraformat = datahoraGravada.strftime('%d/%m/%Y %H:%M:%S')
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < datahoraListar >')
            return

        self.__status = StatusExecucao.Sucesso

        return datahoraformat

    # (dataGravar) Método que Prepara a Data para Gravação
    def dataGravar(self, strData):
        self.__LimpaStatus()

        tipoDado = str(type(strData)).upper()

        if tipoDado.find("TIMESTAMP") > 0:
            self.__status = StatusExecucao.Sucesso
            return strData

        try:
            data = dtm.strptime(strData, "%d/%m/%Y")
            dataformat = f'{data.date()}'
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < dataGravar >')
            return

        self.__status = StatusExecucao.Sucesso

        return dataformat

    # (horaGravar) Método que Prepara a Hora para Gravação
    def horaGravar(self, strHora):
        self.__LimpaStatus()

        tipoDado = str(type(strHora)).upper()

        if tipoDado.find("TIME") > 0:
            self.__status = StatusExecucao.Sucesso
            return strHora

        try:
            hora = dtm.strptime(strHora, "%H:%M")
            horaformat = f'{hora.time()}'
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < horaGravar >')
            return

        self.__status = StatusExecucao.Sucesso

        return horaformat

    # (datahoraGravar) Método que Prepara a Data e Hora para Gravação
    def datahoraGravar(self, strDataHora):
        self.__LimpaStatus()

        tipoDado = str(type(strDataHora)).upper()

        if tipoDado.find("TIMESTAMP") > 0:
            self.__status = StatusExecucao.Sucesso
            datahoraformat = f'{strDataHora.date()}T{strDataHora.time()}'
            return datahoraformat

        try:
            datahora = dtm.strptime(strDataHora, "%d/%m/%Y %H:%M")
            datahoraformat = f'{datahora.date()}T{datahora.time()}'
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < datahoraGravar >')
            return

        self.__status = StatusExecucao.Sucesso

        return datahoraformat

    # (valorListar) Método que Lista o Valor Gravado Formatando
    def valorListar(self, valorGravado):
        self.__LimpaStatus()

        tipoDado = str(type(valorGravado)).upper()

        if tipoDado.find("STR") > 0:
            self.__status = StatusExecucao.Sucesso
            return valorGravado

        try:
            valorformat = "{:,.2f}".format(valorGravado)
            valorformat = valorformat.replace(',', '%')
            valorformat = valorformat.replace('.', ',')
            valorformat = valorformat.replace('%', '.')
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < valorListar >')
            return

        self.__status = StatusExecucao.Sucesso

        return valorformat

    # (valorGravar) Método que Prepara o Valor Formatado para Gravar
    def valorGravar(self, strValorFormatado):
        self.__LimpaStatus()

        tipoDado = str(type(strValorFormatado)).upper()

        if tipoDado.find("FLOAT") > 0:
            self.__status = StatusExecucao.Sucesso
            return strValorFormatado

        try:
            valorformat = strValorFormatado.replace('.', '')
            valorformat = valorformat.replace(',', '.')
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao executar o método < valorGravar >')
            return

        self.__status = StatusExecucao.Sucesso

        return valorformat

    # Métodos Privados
    def __VerificaParametrosConexao(self, AutentWindows):
        if self.__servidor == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Servidor não informado'
            return False

        if self.__bancoDados == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Banco de Dados não informado'
            return False

        if not AutentWindows:
            if self.__usuario == ' ':
                self.__status = StatusExecucao.Erro
                self.__mensagem = 'Usuário não informado'
                return False

            if self.__senha == ' ':
                self.__status = StatusExecucao.Erro
                self.__mensagem = 'Senha não informada'
                return False

        return True

    def __VerificaConexao(self):
        if not self.__conectado:
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'O objeto não está conectado ao banco de dados'
            return False
        return True

    def __LimpaStatus(self):
        self.__Status = StatusExecucao.SemRequisicao
        self.__mensagem = ' '





