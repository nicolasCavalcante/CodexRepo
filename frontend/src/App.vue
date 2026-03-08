<script setup>
import { ref, onMounted } from 'vue'

// Reactive data
const todos = ref([])
const newTodo = ref('')

// Base URL of the backend API.
// In development this goes through Vite proxy (/v1 -> http://localhost:8000/v1)
// to avoid CORS problems when the dev server uses a different port.
const apiBase = '/v1/todos'

// Load todos from backend when the component mounts
const fetchTodos = async () => {
  try {
    const res = await fetch(apiBase)
    if (!res.ok) throw new Error('Failed to fetch todos')
    todos.value = await res.json()
  } catch (err) {
    console.error(err)
    // opcional: mostrar mensagem de erro ao usuário
  }
}

onMounted(fetchTodos)

// Add a new todo (POST to API)
const addTodo = async () => {
  const title = newTodo.value.trim()
  if (title) {
    try {
      const res = await fetch(apiBase, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, done: false }),
      })
      if (!res.ok) throw new Error('Failed to create todo')
      const todo = await res.json()
      todos.value.push(todo)
      newTodo.value = ''
    } catch (err) {
      console.error(err)
    }
  }
}

// Toggle todo completion (PUT)
const toggleTodo = async (id) => {
  const todo = todos.value.find((t) => t.id === id)
  if (todo) {
    try {
      const res = await fetch(`${apiBase}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done: !todo.done }),
      })
      if (!res.ok) throw new Error('Failed to update todo')
      Object.assign(todo, await res.json())
    } catch (err) {
      console.error(err)
    }
  }
}

// Remove a todo (DELETE)
const removeTodo = async (id) => {
  try {
    const res = await fetch(`${apiBase}/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete todo')
    todos.value = todos.value.filter((t) => t.id !== id)
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div id="app">
    <h1>Todo App</h1>
    <div>
      <input v-model="newTodo" @keyup.enter="addTodo" placeholder="Add a new todo" />
      <button @click="addTodo">Add</button>
    </div>
    <ul>
      <li v-for="todo in todos" :key="todo.id" :class="{ completed: todo.done }">
        <input type="checkbox" :checked="todo.done" @change="toggleTodo(todo.id)" />
        <span>{{ todo.title }}</span>
        <button @click="removeTodo(todo.id)">Remove</button>
      </li>
    </ul>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.completed {
  text-decoration: line-through;
  color: #888;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 10px 0;
}
</style>
