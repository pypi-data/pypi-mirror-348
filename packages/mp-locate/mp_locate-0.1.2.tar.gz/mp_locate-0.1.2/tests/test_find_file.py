# test_find_file.py
import os
from mp_locate import find_file

def test_find_file_encontra_arquivo_temporario():
    # Cria um arquivo temporário no diretório atual
    nome_arquivo = "arquivo_teste_temporario.txt"
    with open(nome_arquivo, "w") as f:
        f.write("teste")

    # Testa se o find_file localiza corretamente
    caminho = find_file(nome_arquivo)
    assert os.path.exists(caminho)

    # Limpa
    os.remove(nome_arquivo)

def test_find_file_arquivo_inexistente():
    try:
        find_file("arquivo_que_nao_existe.txt")
        assert False  # Não deveria chegar aqui
    except FileNotFoundError:
        assert True
