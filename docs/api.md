# API (FastAPI)

## Estrutura da API

- `app/main.py`: inicializa FastAPI e registra rotas.
- `app/routers/entities.py`: endpoints HTTP.
- `app/services/crud.py`: operações CRUD genéricas.
- `app/models/entities.py`: modelos SQLAlchemy.
- `app/schemas/entities.py`: contratos Pydantic.
- `app/db/session.py`: engine, sessão e dependency injection.

## Padrão de implementação

Cada endpoint:

1. Recebe e valida payload por schema.
2. Chama o service correspondente.
3. Retorna response model padronizado.

## Observações importantes

- `PATCH /v1/users/{id}` hoje usa schema completo (`UserCreate`), ou seja, update não é parcial de fato.
- Erros de recurso inexistente retornam `404` com mensagem amigável.
