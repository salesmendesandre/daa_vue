# Capítulo 7: Ruteo y Estado Global


## Prerrequisitos
- Haber completado los capítulos anteriores sobre componentes, comunicación y composición con la Composition API.
- Contar con un proyecto base creado mediante `npm create vite@latest` y plantilla `vue` + `javascript`.
- Tener instaladas las dependencias `vue-router` y `pinia` (se explican más adelante).

## Objetivo
Comprender cómo combinar Vue Router y Pinia para crear aplicaciones de una sola página (SPA) con navegación dinámica y un estado global predecible.

## Introducción
A medida que una aplicación crece, ya no basta con un solo componente raíz. Necesitamos:

- **Navegación entre vistas** para mostrar páginas distintas sin recargar el navegador.
- **Un sistema centralizado de estado** para compartir datos y lógica entre componentes dispersos.

Vue 3 ofrece dos herramientas oficiales que resuelven estas necesidades de forma integrada:

1. **Vue Router** → gestiona la navegación, soporta rutas dinámicas y vistas anidadas.
2. **Pinia** → maneja el estado global con una API ligera y totalmente compatible con `<script setup>`.

:::{note}
**Planifica tus rutas y stores antes de codificar:** evita reestructuraciones costosas al final del desarrollo.
:::

:::{warning}
Antes de profundizar en Vue Router, debemos configurar el alias `@` utilizado en los imports proviene de la configuración de Vite. Agrega el alias en `vite.config.js` para que apunte a tu carpeta `src`:
:::

```{code-block} javascript
// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
```


## Vue Router: rutas dinámicas y navegación

### Instalación y configuración inicial
Instala la dependencia desde la raíz del proyecto:

```{code-block} bash
npm install vue-router
```

Crea el router en `src/router/index.js`:

```{code-block} javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/about', name: 'about', component: AboutView }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/01_vue_router/src/router/index.js

En `src/main.js` integra el router antes del `mount`:

```{code-block} javascript
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'

createApp(App).use(router).mount('#app')
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/01_vue_router/src/main.js

### Uso de `<router-view>` y `<router-link>`
`App.vue` suele servir como layout global:

```{code-block} vue
<template>
  <header>
    <nav>
      <router-link to="/">Inicio</router-link>
      <router-link to="/about">Acerca de</router-link>
    </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
nav {
  display: flex;
  gap: 1rem;
}
.router-link-active {
  font-weight: bold;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/01_vue_router/src/App.vue

- `<router-view>` renderiza el componente asociado a la ruta actual.
- `<router-link>` crea enlaces SPA sin recargas, manejando el historial del navegador.

::: {tip}
Usa la prop `:to="{ name: 'about' }"` para desacoplar los enlaces de los paths físicos.
::: 

### Rutas dinámicas
Las rutas pueden incluir parámetros variables para mostrar detalles, por ejemplo `/usuarios/:id`.

```{code-block} javascript
import UsuarioDetalle from '@/views/UsuarioDetalle.vue'

const routes = [
  { path: '/usuarios/:id', name: 'usuario-detalle', component: UsuarioDetalle, props: true }
]
//...resto del router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/02_dynamic_routes/src/router/index.js

Dentro de `UsuarioDetalle.vue` accedemos al parámetro de forma reactiva:

```{code-block} vue
<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const id = computed(() => route.params.id)
</script>

<template>
  <section>
    <h2>Usuario {{ id }}</h2>
    <p>Mostrando datos del usuario con ID {{ id }}.</p>
  </section>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/02_dynamic_routes/src/views/UsuarioDetalle.vue

`route.params` es reactivo: si navegamos a otro ID mientras el componente sigue montado, el contenido se actualiza automáticamente.

### Navegación programática
Para navegar desde el código usamos `useRouter()`:

```{code-block} vue
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function irAlHome() {
  router.push({ name: 'home' })
}
</script>

<template>
  <button @click="irAlHome">Volver al inicio</button>
</template>
```

Si necesitas pasar parámetros (por ejemplo el `id` de un recurso) basta con incluirlos en el objeto. Aquí se navega al detalle de un usuario:

```{code-block} vue
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const usuarioId = ref(42)

function verDetalle() {
  router.push({ name: 'usuario-detalle', params: { id: usuarioId.value } })
}
</script>

<template>
  <label>
    Usuario ID
    <input v-model.number="usuarioId" type="number" min="1" />
  </label>
  <button @click="verDetalle">Ir al detalle</button>
</template>
```

::: {warning}
`router.push` es asíncrono; maneja errores (por ejemplo, navegación duplicada) usando `try/catch` cuando sea necesario.
:::

### Rutas anidadas
Las rutas anidadas permiten crear layouts secundarios dentro de una vista principal. Son especialmente útiles para recursos CRUD porque puedes mantener el menú lateral o las acciones comunes mientras cambias sólo el contenido central.

```{code-block} javascript
import ProductosLayout from '@/views/ProductosLayout.vue'
import ProductoListado from '@/views/ProductoListado.vue'
import ProductoCrear from '@/views/ProductoCrear.vue'
import ProductoDetalle from '@/views/ProductoDetalle.vue'
import ProductoEditar from '@/views/ProductoEditar.vue'

const routes = [
  {
    path: '/productos',
    component: ProductosLayout,
    children: [
      { path: '', name: 'productos-listado', component: ProductoListado }, // Read
      { path: 'nuevo', name: 'producto-crear', component: ProductoCrear }, // Create
      { path: ':id', name: 'producto-detalle', component: ProductoDetalle }, // Read detail
      { path: ':id/editar', name: 'producto-editar', component: ProductoEditar }, // Update
    ],
  },
]
//...resto del router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/03_nested_routes/src/router/index.js

`ProductosLayout.vue` debe incluir su propio `<router-view>` para renderizar los hijos y los accesos a cada operación CRUD.

```{code-block} vue
<template>
  <div class="productos">
    <aside>
      <RouterLink :to="{ name: 'productos-listado' }">Listado</RouterLink>
      <RouterLink :to="{ name: 'producto-crear' }">Nuevo producto</RouterLink>
    </aside>
    <section>
      <router-view />
    </section>
  </div>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/03_nested_routes/src/views/ProductosLayout.vue

## Pinia: gestión de estado moderna

### Qué es Pinia
Pinia sustituye a Vuex como librería oficial de estado global en Vue 3. Está basada en stores reactivos que se consumen directamente desde la Composition API.

### Instalación y configuración
Instala la dependencia:

```{code-block} bash
npm install pinia
```

Registra Pinia en `main.js` junto al router si lo usas:

```{code-block} javascript
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import { createPinia } from 'pinia'

const app = createApp(App)

app.use(router)
app.use(createPinia())

app.mount('#app')
```
https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/04_pinia/src/main.js

### Crear un store básico
Ubica los stores en `src/stores/`. Ejemplo en `src/stores/contador.js`:

```{code-block} javascript
import { defineStore } from 'pinia'

export const useContadorStore = defineStore('contador', {
  state: () => ({
    valor: 0,
  }),
  getters: {
    doble: (state) => state.valor * 2,
  },
  actions: {
    incrementar() {
      this.valor++
    },
  },
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/04_pinia/src/stores/contador.js

Consumimos el store desde cualquier componente con `<script setup>`:

```{code-block} vue
<script setup>
import { storeToRefs } from 'pinia'
import { useContadorStore } from '@/stores/contador'

const contador = useContadorStore()
const { valor, doble } = storeToRefs(contador)

function sumar() {
  contador.incrementar()
}
</script>

<template>
  <section>
    <p>Valor actual: {{ valor }}</p>
    <p>Doble: {{ doble }}</p>
    <button @click="sumar">Incrementar</button>
  </section>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/04_pinia/src/components/ComponenteContadorPinia.vue

### State, getters y actions
| Elemento | Descripción | Ejemplo |
| --- | --- | --- |
| `state` | Datos globales reactivos. | `state: () => ({ contador: 0 })` |
| `getters` | Propiedades derivadas (similar a `computed`). | `doble: (state) => state.contador * 2` |
| `actions` | Métodos para mutar el estado y ejecutar lógica asíncrona. | `reset() { this.contador = 0 }` |

En Pinia puedes usar los stores directamente en `setup()` sin inyección adicional, lo que reduce boilerplate y mejora la trazabilidad.

## Ejemplo integrado: Router + Pinia
El siguiente escenario modela un pequeño tablero de pedidos. Pinia guarda el listado y el pedido activo; Vue Router muestra la lista y el detalle mediante rutas dinámicas.

```{code-block} javascript
// src/stores/pedidos.js
import { defineStore } from 'pinia'

export const usePedidosStore = defineStore('pedidos', {
  state: () => ({
    pedidos: [
      { id: 'A-100', cliente: 'Acme', estado: 'Pendiente' },
      { id: 'A-101', cliente: 'Globex', estado: 'Preparando envío' },
      { id: 'A-102', cliente: 'Initech', estado: 'Completado' },
    ],
    seleccionado: null,
  }),
  getters: {
    totalPendientes: (state) =>
      state.pedidos.filter((pedido) => pedido.estado === 'Pendiente').length,
    pedidoActual: (state) => state.pedidos.find((pedido) => pedido.id === state.seleccionado),
  },
  actions: {
    seleccionarPorId(id) {
      this.seleccionado = id
    },
  },
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/05_pinia_and_router/src/stores/pedidos.js

```{code-block} javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import PedidosListado from '@/views/PedidosListado.vue'
import PedidoDetalle from '@/views/PedidoDetalle.vue'

const routes = [
  { path: '/', redirect: '/pedidos' },
  { path: '/pedidos', name: 'pedidos-listado', component: PedidosListado },
  {
    path: '/pedidos/:id',
    name: 'pedido-detalle',
    component: PedidoDetalle,
    props: true,
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/05_pinia_and_router/src/router/index.js

```{code-block} vue
<!-- src/views/PedidosListado.vue -->
<script setup>
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { usePedidosStore } from '@/stores/pedidos'

const router = useRouter()
const pedidosStore = usePedidosStore()
const { pedidos, totalPendientes } = storeToRefs(pedidosStore)

function irAlDetalle(id) {
  pedidosStore.seleccionarPorId(id)
  router.push({ name: 'pedido-detalle', params: { id } })
}
</script>

<template>
  <section class="vista">
    <header>
      <h1>Pedidos</h1>
      <p>Total pendientes: {{ totalPendientes }}</p>
    </header>

    <ul class="lista">
      <li v-for="pedido in pedidos" :key="pedido.id">
        <span>
          <strong>{{ pedido.id }}</strong> · {{ pedido.cliente }} ({{ pedido.estado }})
        </span>
        <button type="button" @click="irAlDetalle(pedido.id)">Ver detalle</button>
      </li>
    </ul>
  </section>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/05_pinia_and_router/src/views/PedidosListado.vue

```{code-block} vue
<!-- src/views/PedidoDetalle.vue -->
<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePedidosStore } from '@/stores/pedidos'

const route = useRoute()
const router = useRouter()
const pedidosStore = usePedidosStore()

onMounted(() => {
  if (route.params.id) {
    pedidosStore.seleccionarPorId(route.params.id)
  }
})

const pedido = computed(() => pedidosStore.pedidoActual)

function volverAlListado() {
  router.push({ name: 'pedidos-listado' })
}
</script>

<template>
  <section class="vista">
    <h1>Detalle de pedido</h1>

    <article v-if="pedido" class="tarjeta">
      <p><strong>ID:</strong> {{ pedido.id }}</p>
      <p><strong>Cliente:</strong> {{ pedido.cliente }}</p>
      <p><strong>Estado:</strong> {{ pedido.estado }}</p>
    </article>
    <p v-else>No encontramos el pedido solicitado.</p>

    <button type="button" @click="volverAlListado">Volver al listado</button>
  </section>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/07_router_and_global_state/05_pinia_and_router/src/views/PedidoDetalle.vue

Este flujo muestra Pinia administrando el estado de pedidos (listado, total y selección) mientras las rutas `/pedidos` y `/pedidos/:id` intercambian vistas. El store permanece vivo entre rutas, por lo que los datos siguen disponibles al navegar.

## Patrón store y buenas prácticas
El patrón **store** centraliza datos y lógica de negocio fuera de los componentes. Así los componentes se enfocan en la presentación.

Buenas prácticas clave:

- Divide los stores por dominio o función (`auth`, `productos`, `ui`, etc.).
- Evita acoplar componentes lejanos al estado global si no lo necesitan.
- Usa getters para cálculos derivados complejos y compartirlos entre vistas.
- Modifica el estado solo desde `actions` para mantener el control de las mutaciones.
- Nombra los stores y propiedades de forma clara (`useCarritoStore`, `items`, `total`).
- Guarda los stores en `src/stores/` y documenta brevemente su responsabilidad.
- Si necesitas el router dentro de un store, llama a `useRouter()` dentro de la acción para respetar el ciclo de composición.
- Mantén cada store pequeño y con responsabilidad única.

{tip}
Crea un archivo `stores/index.js` que exporte todos los stores si el proyecto crece: facilita el import en componentes.

## Resumen
- Vue Router gestiona la navegación SPA con rutas dinámicas, navegación programática y vistas anidadas.
- Pinia ofrece un estado global moderno basado en stores reactivos y sencillo de usar con `<script setup>`.
- El patrón store otorga previsibilidad y escalabilidad al separar datos y lógica de presentación.
- Juntos, ruteo y estado global permiten construir aplicaciones robustas y mantenibles.

## Ejercicio
Desarrolla un módulo CRUD completo de productos:
- Define el router con `/productos`, `/productos/nuevo`, `/productos/:id` y `/productos/:id/editar`.
- Crea un store `useProductosStore` que mantenga la lista en memoria, permita crear/actualizar/eliminar y exponga getters (por ejemplo, `totalActivos`).
- Cada producto puede incluir campos básicos como `id`, `nombre`, `precio`, `stock` y `estado` (Activo/Inactivo); si lo deseas agrega `categoria` o una breve `descripcion` para practicar formularios más largos.
- Implementa las vistas de listado, creación, detalle y edición usando Pinia para leer y mutar el estado, y vue-router para navegar programáticamente tras cada operación.
- Opcional: agrega confirmaciones simples antes de eliminar y mensajes de estado en pantalla para practicar la comunicación entre capas.
