# Orquestração (Dagster)

O projeto define assets Dagster para executar pipeline dbt:

1. `run_dbt_models`
2. `run_dbt_tests` (depende de `run_dbt_models`)

## Objetivo

- Automatizar transformação analítica.
- Garantir execução de testes após construção dos modelos.

## Configuração

A variável `ANALYTICS_DIR` permite apontar para diretório do projeto dbt.
