import os

def ExisteArquivo(caminhoArquivo, nomeArquivo):
    return os.path.exists(caminhoArquivo + nomeArquivo)

def AbreArquivo (caminhoArquivo, nomeArquivo):
    if not ExisteArquivo(caminhoArquivo, nomeArquivo):
        print('O arquivo não foi localizado em ' + caminhoArquivo + nomeArquivo + '.')
        return False

    try:
        arq = open(caminhoArquivo + nomeArquivo)
    except Exception as erro:
        print(f'Ocorreu o erro {erro}.' + ' ao tentar abrir o arquivo em ' + caminhoArquivo + nomeArquivo + '.')
        return False

    return arq

def CriaArquivo (caminhoArquivo, nomeArquivo):
    if ExisteArquivo(caminhoArquivo, nomeArquivo):
        print('O arquivo já existe em ' + caminhoArquivo + nomeArquivo + '.')
        return False

    try:
        arq = open(caminhoArquivo + nomeArquivo, 'w')
    except Exception as erro:
        print(f'Ocorreu o erro {erro}.' + ' ao tentar abrir o arquivo em ' + caminhoArquivo + nomeArquivo + '.')
        return False

    return arq

def RegistraLinhaArquivo (arquivo, texto, pularLinha):
    try:
        if pularLinha:
            arquivo.write(texto + '\n')
        else:
            arquivo.write(texto)
    except Exception as erro:
        print(f'Ocorreu o erro {erro}.' + ' ao tentar registrar um texto no arquivo informado.')
        return False

    return True


