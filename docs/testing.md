# Testes

## API

Os testes automatizados vivem em `api/tests`.

Execute:

```bash
pytest api/tests -q
```

Cobertura atual inclui:

- Healthcheck
- CRUD de usuários
- CRUD básico de produtos/pedidos
- Validação de payload inválido

## Boas práticas

- Sempre rode testes antes de abrir PR.
- Ao corrigir bug, adicione teste de regressão.
