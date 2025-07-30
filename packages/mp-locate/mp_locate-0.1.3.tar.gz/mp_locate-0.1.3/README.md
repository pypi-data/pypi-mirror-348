# mp_locate

**mp_locate** is a simple Python library for finding files by name recursively from a base directory.

## ✨ Features
- Recursive file search
- Configurable base path (or use the current directory)
- Support for returning single or multiple found files

## ⚡ Installation
```bash
pip install mp_locate
```

Or install locally:
```bash
pip install -e .
```

## 📄 Usage example
```python
from mp_locate import find_file

# Find the first file with the specified name
path = find_file("data.csv")

# Return all found paths
all = find_file("data.csv", return_all=True)
```

## ✉ License
MIT. See the `LICENSE` file for more details.

# mp_locate Portuguese

**mp_locate** é uma biblioteca Python simples para localizar arquivos por nome de forma recursiva a partir de um diretório base.

## ✨ Características
- Busca recursiva por arquivos
- Caminho base configurável (ou usa o diretório atual)
- Suporte a retorno único ou múltiplos arquivos encontrados

## ⚡ Instalação
```bash
pip install mp_locate
```

Ou instale localmente:
```bash
pip install -e .
```

## 📄 Exemplo de uso
```python
from mp_locate import find_file

# Localizar o primeiro arquivo com nome especificado
caminho = find_file("dados.csv")

# Retornar todos os caminhos encontrados
todos = find_file("dados.csv", retornar_todos=True)
```

## ✉ Licença
MIT. Veja o arquivo `LICENSE` para mais detalhes.