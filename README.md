# TODO App (MVP) com FastAPI + PostgreSQL

Projeto mínimo viável de API para tarefas (TODO), usando Python 3.10 e `pyproject.toml` com `setuptools`.

## Requisitos

- Python 3.10
- PostgreSQL instalado

## Configuração

1. Copie o template e preencha seus segredos:

```bash
copy config.yaml.example config.yaml
```

2. Edite `config.yaml` com seus valores:

```yaml
postgres:
  port: 5432
  admin_user: "postgres"
  admin_password: "troque-esta-senha"
  db_name: "todo_app"
```

`config.yaml` e tratado como segredo e esta no `.gitignore`.

3. Instale o projeto e dependências:

```bash
pip install -e .
```

4. Execute a API:

```bash
uvicorn app.main:app --reload --app-dir api
```

## PostgreSQL no Windows (passo a passo)

### 1. Baixar o instalador

- Acesse: `https://www.postgresql.org/download/windows/`
- Clique em `Download the installer`.

### 2. Instalar

- Execute o instalador.
- Mantenha os componentes `PostgreSQL Server` e `Command Line Tools`.
- Defina a senha do usuario `postgres`.
- Use a porta `5432` (ou ajuste no `config.yaml` depois).

### 3. Verificar se o servico esta rodando

```powershell
Get-Service *postgres*
```

Se estiver parado:

```powershell
Start-Service postgresql-x64-16
```

Observacao: o nome do servico pode variar pela versao instalada.

### 4. Garantir `psql` e `createdb` no PATH

Pasta comum:

`C:\Program Files\PostgreSQL\16\bin`

Teste:

```powershell
psql --version
```

### 5. Criar o banco da aplicacao

```powershell
createdb -h 127.0.0.1 -p 5432 -U postgres todo_app
```

### 6. Testar conexao

```powershell
psql -h 127.0.0.1 -p 5432 -U postgres -d todo_app
```

## Comportamento no startup da API

No startup da API, o sistema:
1. Verifica se o servidor PostgreSQL esta acessivel.
2. Verifica se o banco configurado existe.
3. Se algo estiver errado, falha com mensagem clara de como corrigir.
4. Se estiver tudo certo, cria as tabelas da aplicacao.

Tudo e lido de `config.yaml` e nao usa variaveis de ambiente para `DATABASE_URL`.

## Endpoints

- `GET /health`
- `POST /v1/todos`
- `GET /v1/todos`
- `GET /v1/todos/{todo_id}`
- `PUT /v1/todos/{todo_id}`
- `DELETE /v1/todos/{todo_id}`

## Exemplo de payload

```json
{
  "title": "Estudar FastAPI",
  "description": "Implementar CRUD de tarefas",
  "done": false
}
```

Swagger: `http://127.0.0.1:8000/docs`
