# Guia de contribuição

## Fluxo recomendado

1. Crie branch a partir de `main`.
2. Faça mudanças pequenas e focadas.
3. Rode testes (`pytest api/tests -q`).
4. Atualize documentação quando necessário.
5. Abra PR com contexto claro.

## Checklist rápido

- [ ] Código formatado e legível
- [ ] Testes passando
- [ ] Sem quebra de compatibilidade não documentada
- [ ] README/docs atualizados

## Convenções úteis

- Prefira nomes explícitos.
- Mantenha separação de camadas (router/service/model/schema).
- Evite acoplamento entre módulos sem necessidade.
