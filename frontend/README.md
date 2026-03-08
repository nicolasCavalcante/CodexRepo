# Todo App Frontend - Vue.js

Este é o frontend da aplicação Todo, construído com Vue.js 3 e Vite. Esta é uma introdução básica para quem está usando Vue pela primeira vez.

## Pré-requisitos

Antes de começar, você precisa ter o Node.js instalado no seu computador. Você pode baixar em [nodejs.org](https://nodejs.org/).

Para verificar se está instalado, abra o terminal e digite:
```
node --version
npm --version
```

## Instalação

1. Navegue até a pasta `frontend` do repositório:
   ```
   cd frontend
   ```

2. Instale as dependências:
   ```
   npm install
   ```

## Como usar

### Desenvolvimento

Para iniciar o servidor de desenvolvimento:
```
npm run dev
```

Isso abrirá o aplicativo no seu navegador em `http://localhost:5173` (ou outra porta se 5173 estiver ocupada).

### Build para produção

Para criar uma versão otimizada para produção:
```
npm run build
```

### Preview da build

Para visualizar a build de produção localmente:
```
npm run preview
```

## Estrutura do projeto

- `index.html`: O arquivo HTML principal
- `src/main.js`: O ponto de entrada da aplicação Vue
- `src/App.vue`: O componente principal da aplicação
- `vite.config.js`: Configuração do Vite

## O que é Vue.js?

Vue.js é um framework JavaScript progressivo para construir interfaces de usuário. Ele é focado na camada de visualização e é fácil de integrar com outras bibliotecas ou projetos existentes.

### Conceitos básicos que você verá aqui:

- **Componentes**: Blocos reutilizáveis de código (como `App.vue`)
- **Template**: A parte HTML do componente
- **Script**: A lógica JavaScript (usando `<script setup>`)
- **Style**: CSS específico do componente
- **Reatividade**: Dados que atualizam automaticamente a interface (usando `ref`)

### Integração com o backend

O app presente em `src/App.vue` mantém o estado apenas no navegador por padrão. Para persistência e sincronização entre clientes, é preciso apontar a UI para a API FastAPI que existe no repositório.

O backend expõe estes endpoints (assumindo `http://localhost:8000`):

- `GET  /v1/todos` → lista todas as tarefas
- `POST /v1/todos` → cria uma nova tarefa (`{ "text": "...", "completed": false }`)
- `PUT  /v1/todos/{id}` → atualiza um campo da tarefa
- `DELETE /v1/todos/{id}` → remove uma tarefa

No código de exemplo eu uso `fetch`, mas você pode optar por `axios` ou outra biblioteca.

#### Executando o backend

1. Entre na pasta `api` do repositório:
   ```bash
   cd ../api
   ```
2. Crie/ative seu ambiente Python e instale as dependências (veja `environment.yml` ou `pyproject.toml`).
3. Inicie a aplicação FastAPI com uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Por padrão, o servidor ficará em `http://localhost:8000`. A rota `/health` retorna `{ "status": "ok" }`.

> ⚠️ Certifique‑se de iniciar o backend **antes** de abrir o frontend, caso contrário as requisições falharão.

### Próximos passos

- Aprenda mais sobre Vue em [vuejs.org](https://vuejs.org/)
- Explore a documentação do Vite em [vitejs.dev](https://vitejs.dev/")

## Solução de problemas

- Se `npm install` falhar, tente deletar `node_modules` e `package-lock.json` e rodar novamente.
- Se a porta 5173 estiver ocupada, o Vite escolherá automaticamente outra porta.
- Certifique-se de que não há firewalls bloqueando a porta.
