# Capítulo 11: CRUD Completo en Firestore

En este capítulo aprenderás a integrar tu aplicación Vue 3 con Firestore para realizar las cuatro operaciones fundamentales: crear, leer, actualizar y eliminar entidades, organizando la lógica en servicios reutilizables.

```{admonition} Objetivo
Configurar Firebase, crear un servicio de Firestore en `/services`, y construir tres vistas (listado, añadir y editar) que usen Composition API para un CRUD completo.
```

## Introducción

Firestore es una base de datos NoSQL en la nube que guarda documentos agrupados en colecciones.

- **Colecciones**: agrupaciones lógicas de documentos (similar a tablas, pero sin esquema rígido).
- **Documentos**: objetos JSON con campos dinámicos y un id único.
- **Id automático vs id propio**: Firestore puede generar ids con `addDoc`; también puedes fijar un id con `setDoc` si lo necesitas (en este capítulo usamos ids automáticos).
- **Lectura puntual (`getDoc`)**: obtiene el estado actual una sola vez; ideal para cargar un detalle.
- **Lectura en tiempo real (`onSnapshot`)**: mantiene una suscripción a cambios; perfecta para listados que se actualizan al instante.
- **Flujo CRUD típico en Firestore**: Create → Real-time List → Update → Delete, siempre evitando mezclar lógica de red en los componentes.

### ¿Qué es Firestore y en qué se diferencia?

Firestore (Cloud Firestore) es la base de datos NoSQL document-oriented de Firebase y de Google Cloud. Almacena los datos como documentos dentro de colecciones y replica automáticamente la información para que esté disponible en múltiples regiones, con baja latencia y tolerancia a fallos. A diferencia de una base de datos relacional:

- No define esquemas rígidos: cada documento puede tener distintos campos.
- Escala horizontalmente y permite consultas por múltiples campos con índices.
- Incluye **suscripciones en tiempo real** para reaccionar a cambios sin recargar la página.
- Tiene reglas de seguridad por usuario (Security Rules) que se evalúan en el backend de Firebase.

Firestore no es lo mismo que el Realtime Database de Firebase: Firestore admite consultas más ricas (filtros compuestos, ordenaciones) y estructuras de datos más flexibles, mientras que Realtime Database está optimizado para sincronización ultra rápida de árboles JSON.

```{note}
Trabajaremos con Firebase SDK v9 modular, Vue 3 + Vite y la Composition API con `<script setup>`.
```

## Estructura recomendada del proyecto

Organiza la lógica de Firestore en `/services` y las pantallas en `/views`.

```{code-block} text
src/
├─ services/
│  ├─ firebase.js
│  └─ itemsService.js
├─ views/
│  ├─ ItemsList.vue
│  ├─ AddItem.vue
│  └─ EditItem.vue
├─ router/
│  └─ index.js
└─ main.js
```

```{warning}
No mezcles lógica de Firestore en los componentes. Cada pantalla debería consumir funciones limpias desde `/services`.
```

## Configuración base de Firebase

Primero inicializamos Firebase y exportamos la instancia de Firestore.

```{code-block} javascript
// src/services/firebase.js
import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
}

const app = initializeApp(firebaseConfig)
export const db = getFirestore(app)
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/11_firebase_firestore/src/services/firebase.js

```{tip}
Guarda las claves en variables de entorno (`.env`) y reinicia Vite al cambiarlas.
```

## Servicio Firestore principal (`itemsService.js`)

Centralizamos las operaciones CRUD y la suscripción en tiempo real.

```{code-block} javascript
// src/services/itemsService.js
import { db } from './firebase'
import {
  collection,
  addDoc,
  doc,
  getDoc,
  updateDoc,
  deleteDoc,
  onSnapshot,
  query,
  orderBy,
  serverTimestamp
} from 'firebase/firestore'

const colRef = collection(db, 'items')

export const addItem = (data) =>
  addDoc(colRef, { ...data, createdAt: serverTimestamp() })

export const getItem = (id) =>
  getDoc(doc(db, 'items', id))

export const updateItem = (id, data) =>
  updateDoc(doc(db, 'items', id), data)

export const deleteItem = (id) =>
  deleteDoc(doc(db, 'items', id))

export const subscribeToItems = (callback) =>
  onSnapshot(
    query(colRef, orderBy('createdAt', 'desc')),
    snapshot => {
      callback(snapshot.docs.map(d => ({ id: d.id, ...d.data() })))
    }
  )
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/11_firebase_firestore/src/services/itemsService.js

```{note}
`serverTimestamp()` añade una marca de tiempo consistente desde el servidor y permite ordenar por fecha de creación.
```

## Vista 1: Listado de entidades (`ItemsList.vue`)

Este componente no conoce Firestore directamente: importa las funciones `subscribeToItems` y `deleteItem` desde `/services/itemsService.js`, se suscribe en `onMounted`, limpia en `onUnmounted`, y expone botones de edición y borrado.

```{code-block} vue
<!-- src/views/ItemsList.vue -->
<template>
  <section>
    <h1>Items</h1>
    <RouterLink to="/items/add">Añadir</RouterLink>

    <ul v-if="items.length">
      <li v-for="item in items" :key="item.id">
        <strong>{{ item.title }}</strong>
        <p>{{ item.description }}</p>
        <button @click="goEdit(item.id)">Editar</button>
        <button @click="handleDelete(item.id)">Eliminar</button>
      </li>
    </ul>
    <p v-else>No hay items todavía.</p>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { subscribeToItems, deleteItem } from '@/services/itemsService'

const router = useRouter()
const items = ref([])
const loading = ref(false)
let unsubscribe = null

const goEdit = (id) => {
  router.push(`/items/edit/${id}`)
}

const handleDelete = async (id) => {
  loading.value = true
  try {
    await deleteItem(id)
  } catch (err) {
    console.error('Error eliminando', err)
    alert('No se pudo eliminar. Revisa la consola.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  unsubscribe = subscribeToItems((docs) => {
    items.value = docs
  })
})

onUnmounted(() => {
  if (unsubscribe) unsubscribe()
})
</script>
```

```{tip}
Siempre guarda la función que devuelve `onSnapshot` para limpiarla en `onUnmounted`. Evitarás fugas de memoria y múltiples escuchas duplicadas.
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/11_firebase_firestore/src/views/ItemsList.vue

## Vista 2: Añadir entidad (`AddItem.vue`)

El formulario usa exclusivamente el servicio `addItem` para crear el documento y luego redirige al listado; no hay llamadas directas al SDK en el componente.

```{code-block} vue
<!-- src/views/AddItem.vue -->
<template>
  <section>
    <h1>Nuevo item</h1>
    <form @submit.prevent="handleSubmit">
      <label>
        Título
        <input v-model="title" required />
      </label>
      <label>
        Descripción
        <textarea v-model="description" required></textarea>
      </label>
      <button type="submit" :disabled="loading">Guardar</button>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addItem } from '@/services/itemsService'

const router = useRouter()
const title = ref('')
const description = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  loading.value = true
  try {
    await addItem({ title: title.value, description: description.value })
    router.push('/items')
  } catch (err) {
    console.error('Error creando', err)
    alert('No se pudo crear el item.')
  } finally {
    loading.value = false
  }
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/11_firebase_firestore/src/views/AddItem.vue

```{note}
Como usamos `<script setup>`, no necesitamos exportar nada; las refs son accesibles directamente en la plantilla.
```

## Vista 3: Editar entidad (`EditItem.vue`)

La vista consume `getItem` y `updateItem` desde el servicio, manteniendo la lógica de red fuera del componente. Recupera el id de la ruta, carga los datos, los asigna a refs y actualiza.

```{code-block} vue
<!-- src/views/EditItem.vue -->
<template>
  <section>
    <h1>Editar item</h1>
    <form v-if="loaded" @submit.prevent="handleSubmit">
      <label>
        Título
        <input v-model="title" required />
      </label>
      <label>
        Descripción
        <textarea v-model="description" required></textarea>
      </label>
      <button type="submit" :disabled="loading">Actualizar</button>
    </form>
    <p v-else>Cargando...</p>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getItem, updateItem } from '@/services/itemsService'

const route = useRoute()
const router = useRouter()
const title = ref('')
const description = ref('')
const loading = ref(false)
const loaded = ref(false)
const id = route.params.id

const loadItem = async () => {
  try {
    const snap = await getItem(id)
    if (!snap.exists()) {
      alert('No existe el documento')
      router.push('/items')
      return
    }
    const data = snap.data()
    title.value = data.title
    description.value = data.description
    loaded.value = true
  } catch (err) {
    console.error('Error cargando', err)
    alert('No se pudo cargar el item.')
    router.push('/items')
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    await updateItem(id, { title: title.value, description: description.value })
    router.push('/items')
  } catch (err) {
    console.error('Error actualizando', err)
    alert('No se pudo actualizar.')
  } finally {
    loading.value = false
  }
}

onMounted(loadItem)
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/11_firebase_firestore/src/views/EditItem.vue

## Configuración de rutas

Define las rutas para las tres vistas. Usa un parámetro `:id` para la edición.

```{code-block} javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import ItemsList from '@/views/ItemsList.vue'
import AddItem from '@/views/AddItem.vue'
import EditItem from '@/views/EditItem.vue'

const routes = [
  { path: '/items', component: ItemsList },
  { path: '/items/add', component: AddItem },
  { path: '/items/edit/:id', component: EditItem }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/11_firebase_firestore/src/router/index.js

```{warning}
Las rutas mínimas requeridas son `{ path: '/items', component: ItemsList }`, `{ path: '/items/add', component: AddItem }` y `{ path: '/items/edit/:id', component: EditItem }`. Asegúrate de usar `:id` para que la edición funcione.
```


## Buenas prácticas

- No mezclar lógica de Firestore en los componentes; usa `/services`.
- Limpia las suscripciones `onSnapshot` en `onUnmounted`.
- Maneja errores con `try/catch` y feedback al usuario.
- Usa `serverTimestamp()` para fechas coherentes y ordenables.
- Diferencia cuándo usar lectura puntual (`getDoc`) y lectura en tiempo real (`onSnapshot`).
- Mantén los ids autogenerados de Firestore salvo que tengas un motivo sólido para fijarlos.

## Errores comunes y cómo evitarlos

- **Olvidar limpiar la suscripción**: causa fugas y dobles llamadas. Guarda la función que devuelve `onSnapshot`.
- **No esperar a `serverTimestamp()`**: si ordenas por fecha, usa consultas que soporten campos nulos iniciales o espera a que se escriba.
- **No comprobar `snap.exists()`** al obtener por id: gestiona el caso de documento inexistente.
- **Rutas sin `:id`**: impedirán cargar el documento a editar.


## Ejercicio: Gestión básica de "Eventos" con Firestore

Construye un módulo sencillo en tu aplicación donde puedas **crear, listar, editar y eliminar eventos** almacenados en **Firestore**.

Cada evento debe tener exactamente **cuatro campos**:

- `title` → nombre del evento  
- `description` → breve explicación del evento  
- `author` → persona que creó el evento  
- `dateOfEvent` → fecha del evento (tipo fecha) 
- `dateOfCreation` → fecha de creación del evento (usar `serverTimestamp()`)

### Requisitos

1. Crea un **servicio de Firestore** llamado `eventsService.js` con las siguientes operaciones:
   - Crear un evento.
   - Listar eventos en tiempo real.
   - Obtener un evento por su `id`.
   - Actualizar un evento.
   - Eliminar un evento.

2. Crea una **vista de listado** que muestre todos los eventos en tiempo real:
   - Debe mostrar al menos `title`, `author` y `date`.
   - Añade botones para **editar** y **eliminar** cada evento.
   - Añade un botón para **crear nuevo evento** que lleve a la vista de creación.

3. Crea una **vista de creación** para añadir un nuevo evento:
   - Formulario con los campos: `title`, `description`, `author`, `dateOfEvent`.
   - Al guardar, se debe crear el documento en Firestore y asignar `dateOfCreation` con `serverTimestamp()`.
   - Tras guardar, redirigir al listado de eventos.

4. Crea una **vista de edición** para modificar un evento existente:
   - Cargar los datos del evento desde Firestore usando su `id`.
   - Permitir editar `title`, `description`, `author` y `dateOfEvent`.
   - Al guardar, actualizar el documento en Firestore y volver al listado.

5. Configura las **rutas** necesarias para acceder a las vistas de listado, creación y edición.

6. Filtra los eventos por algún campo.

7. Filtra los eventos por fecha.

8. Muestra los eventos en formato tabla y en formato cards.
