# Plataforma CRUD Completa

Bem-vindo(a)! Esta documentação foi escrita para quem está começando no projeto.

## O que você vai encontrar aqui

- Como preparar ambiente e instalar dependências.
- Como subir API e App localmente.
- Como o código está organizado por camadas.
- Como funciona a parte analítica com dbt e DuckDB.
- Como executar testes e contribuir com segurança.

## Stack principal

- **API**: FastAPI + SQLAlchemy
- **Front-end**: Streamlit
- **Analytics**: dbt + DuckDB
- **Orquestração**: Dagster

## Fluxo recomendado para iniciantes

1. Leia **Primeiros passos**.
2. Execute o projeto localmente.
3. Faça uma requisição simples na API (`/health` e `/v1/users`).
4. Navegue pela seção de arquitetura para entender cada módulo.
5. Rode os testes antes de alterar código.

> Dica: use esta documentação junto com o `README.md`, que continua sendo uma referência rápida.
