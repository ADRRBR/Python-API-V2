from Classes.BAS_Generico import *
from Classes.BAS_Arquivo import *

class Planilha:
    def __init__(self):
        self.__planilhaCaminho = ' '
        self.__planilhaNome = ' '
        self.__pastaTrabalho = ' '
        self.__linhaInicial = 0
        self.__linhaFinal = 0
        self.__faixaCelulas = ' '
        self.__status = StatusExecucao.SemRequisicao
        self.__mensagem = ' '

    # Caminho da Planilha para Leitura
    @property
    def planilhaCaminho(self):
        return self.__planilhaCaminho

    @planilhaCaminho.setter
    def planilhaCaminho(self, valor):
        if type(valor) == type(self.__planilhaCaminho):
            self.__planilhaCaminho = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Nome da PLanilha para Leitura
    @property
    def planilhaNome(self):
        return self.__planilhaNome

    @planilhaNome.setter
    def planilhaNome(self, valor):
        if type(valor) == type(self.__planilhaNome):
            self.__planilhaNome = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Pasta de Trabalho para Leitura da Planilha
    @property
    def pastaTrabalho(self):
        return self.__pastaTrabalho

    @pastaTrabalho.setter
    def pastaTrabalho(self, valor):
        if type(valor) == type(self.__pastaTrabalho):
            self.__pastaTrabalho = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Linha Inicial para Leitura da Planilha
    @property
    def linhaInicial(self):
        return self.__l

    @linhaInicial.setter
    def linhaInicial(self, valor):
        if type(valor) == type(self.__linhaInicial):
            self.__linhaInicial = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Linha Final para Leitura da Planilha
    @property
    def linhaFinal(self):
        return self.__l

    @linhaFinal.setter
    def linhaFinal(self, valor):
        if type(valor) == type(self.__linhaFinal):
            self.__linhaFinal = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Faixa de Células para Leitura da Planilha
    @property
    def faixaCelulas(self):
        return self.__faixaCelulas

    @faixaCelulas.setter
    def faixaCelulas(self, valor):
        if type(valor) == type(self.__faixaCelulas):
            self.__faixaCelulas = valor
        else:
            self.__status = StatusExecucao.Erro
            self.__mensagem = "Tipo de dado inválido."

    # Status
    @property
    def status(self):
        return self.__status

    # Mensagem
    @property
    def mensagem(self):
        return self.__mensagem

    # (arquivoConfigPlanilha) Método que Lê a Planilha Conforme a Parametrização em um Arquivo de Configuração.
    def arquivoConfigPlanilha(self, CaminhoArquivo, NomeArquivo):
        self.__LimpaStatus()

        __CaminhoArquivo = CaminhoArquivo
        __NomeArquivo = NomeArquivo

        #Arquivo de Configuração não Informado, Assume o Caminho e Nome Padrão
        if (__CaminhoArquivo == '' or __NomeArquivo == ''):
            __CaminhoArquivo = os.getcwd() + "\ConfigArquivos\ ".strip()
            __NomeArquivo = 'ConfigPlanilha.txt'

        if not ExisteArquivo(__CaminhoArquivo, __NomeArquivo):
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'O arquivo de configuração para leitura da planilha não foi localizado em ' + __CaminhoArquivo + __NomeArquivo + '. Método < arquivoConfigPlanilha >'
            return

        try:
            arq = AbreArquivo(__CaminhoArquivo, __NomeArquivo)
            if not arq:
                self.__status = StatusExecucao.Erro
                self.__mensagem = 'Não foi possível ler o arquivo de configuração para leitura da planilha em ' + __CaminhoArquivo + __NomeArquivo + '. Método < arquivoConfigPlanilha >'
                return

            linhas = arq.readlines()

            for linha in linhas:
                if linha.find('[CAMINHO]') == 0:
                    vAux = linha.split('|')
                    self.__planilhaCaminho = vAux[1]
                    self.__planilhaCaminho = self.__planilhaCaminho.strip()

                elif linha.find('[NOME]') == 0:
                    vAux = linha.split('|')
                    self.__planilhaNome = vAux[1]
                    self.__planilhaNome = self.__planilhaNome.strip()

                elif linha.find('[PASTA TRABALHO]') == 0:
                    vAux = linha.split('|')
                    self.__pastaTrabalho = vAux[1]
                    self.__pastaTrabalho = self.__pastaTrabalho.strip()

                elif linha.find('[LINHA INICIAL]') == 0:
                    vAux = linha.split('|')
                    self.__linhaInicial = vAux[1]
                    self.__linhaInicial = self.__linhaInicial.strip()
                    self.__linhaInicial = int(self.__linhaInicial)

                elif linha.find('[LINHA FINAL]') == 0:
                    vAux = linha.split('|')
                    self.__linhaFinal = vAux[1]
                    self.__linhaFinal = self.__linhaFinal.strip()
                    self.__linhaFinal = int(self.__linhaFinal)

                elif linha.find('[FAIXA DE CELULAS]') == 0:
                    vAux = linha.split('|')
                    self.__faixaCelulas = vAux[1]
                    self.__faixaCelulas = self.__faixaCelulas.strip()

            arq.close()

        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = f'Ocorreu o erro {erro}.' + ' Ao tentar ler o arquivo de configuração para leitura de planilha. Método < arquivoConfigPlanilha >'
            arq.close()
            return

        # Efetua a leitura da planilha com base nos parâmetros recuperados do arquivo de configuração
        try:
            tabPlan = self.lerPlanilha()
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = f'Ocorreu o erro {erro}. Ao executar o método < lerPlanilha >'
        else:
            if self.__status != StatusExecucao.Sucesso:
                self.__mensagem += f'. Ao executar o método < lerPlanilha >'

        return tabPlan

    # (lerPlanilha) Método que Lê a Planilha Informada
    def lerPlanilha(self):
        self.__LimpaStatus()

        if not self.__verificaParametros():
            return

        linhaCabecalho = self.__linhaInicial - 1

        try:
            tabPlan = pd.read_excel(self.__planilhaCaminho + self.__planilhaNome, sheet_name=self.__pastaTrabalho, nrows=self.__linhaFinal, usecols=self.__faixaCelulas, header=linhaCabecalho)
        except Exception as erro:
            self.__status = StatusExecucao.Erro
            self.__mensagem = (f'Ocorreu o erro {erro}. Ao ler a planilha {self.__planilhaCaminho + self.__planilhaNome}')
            return

        if len(tabPlan) == 0:
            self.__status = StatusExecucao.NaoEncontrado
            self.__mensagem = (f'Nenhuma linha detalhe foi encontrada na planilha {self.__planilhaCaminho + self.__planilhaNome}')
            return

        self.__status = StatusExecucao.Sucesso

        return tabPlan

    # Métodos Privados
    def __verificaParametros(self):
        if self.__planilhaCaminho == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Caminho da planilha não informado'
            return False

        if self.__planilhaNome == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Nome da planilha não informado'
            return False

        if self.__pastaTrabalho == 0:
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Informe a pasta de trabalho para leitura da planilha'
            return False

        if self.__linhaInicial == 0:
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Informe a linha inicial para leitura da planilha, partindo sempre de 1'
            return False

        if self.__linhaFinal <= self.__linhaInicial:
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Informe a linha final para leitura da planilha, sendo sempre maior que o informado na linha inicial, pois sempre a primeira linha lida será considerada como cabeçalho'
            return False

        if self.__faixaCelulas == ' ':
            self.__status = StatusExecucao.Erro
            self.__mensagem = 'Informe a faixa de células para leitura da planilha. Ex.: (A,B,D,E:J)'
            return False

        return True

    def __LimpaStatus(self):
        self.__Status = StatusExecucao.SemRequisicao
        self.__mensagem = ' '
