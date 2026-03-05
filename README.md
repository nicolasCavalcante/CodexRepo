# CodexRepo

## Visão geral
Este repositório descreve uma **Data CRUD & Analytics Platform** com duas frentes complementares: uma aplicação transacional para cadastro e operação de dados e uma camada analítica para exploração e geração de insights. A proposta é manter o fluxo completo, do dado operacional ao consumo analítico, em uma arquitetura simples, modular e evolutiva.

## Arquitetura
### Aplicação transacional (Frontend / FastAPI / PostgreSQL)
- **Frontend**: interface para criação, leitura, atualização e exclusão de dados (CRUD).
- **FastAPI**: API responsável pelas regras de negócio e exposição dos endpoints.
- **PostgreSQL**: banco relacional transacional para persistência dos dados operacionais.

### Orquestração (Dagster)
- **Dagster** coordena jobs, dependências e agendamentos do pipeline de dados.
- Centraliza execução, observabilidade e rastreabilidade das cargas e transformações.

### Transformação (dbt)
- **dbt** implementa modelos SQL versionados e testáveis.
- Realiza padronização, enriquecimento e organização dos dados para análise.

### Camada analítica (DuckDB / Streamlit)
- **DuckDB** atua como engine analítica para consultas rápidas em dados modelados.
- **Streamlit** disponibiliza dashboards e análises para consumo por usuários de negócio.

## Fluxo fim a fim
Frontend → FastAPI → PostgreSQL  
Dagster → dbt → DuckDB  
Streamlit → DuckDB

## Objetivos
- Consolidar uma base de referência para aplicações data-driven com ciclo completo de dados.
- Separar claramente responsabilidades transacionais e analíticas.
- Facilitar evolução de pipelines, modelos e consumo de informações.

## Stack
- **Frontend** (camada de interface)
- **FastAPI** (serviço backend)
- **PostgreSQL** (persistência transacional)
- **Dagster** (orquestração)
- **dbt** (transformação/modelagem)
- **DuckDB** (armazenamento/consulta analítica)
- **Streamlit** (visualização)

## Status
Projeto em estruturação inicial, com definição de arquitetura e fluxo de referência para evolução incremental dos componentes.

Revisão de merge desta branch: **sem conflitos pendentes** no `README.md`.

## Motivação
Fornecer um blueprint prático para integrar operações de CRUD com analytics, reduzindo fricção entre desenvolvimento de produto e engenharia de dados, e acelerando a geração de valor a partir dos dados.
