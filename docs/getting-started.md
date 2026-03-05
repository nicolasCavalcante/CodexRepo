# Ambiente e instalação

## Pré-requisitos

- Python **3.10**
- `pip` atualizado
- Git

## Instalação

Na raiz do projeto:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows (cmd)

python -m pip install --upgrade pip
pip install -e .
```

Para ambiente de desenvolvimento (inclui testes):

```bash
pip install -e .[dev]
```

## Dependências de documentação

Para gerar e servir a documentação localmente:

```bash
pip install -e .[docs]
```
