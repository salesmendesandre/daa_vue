# Capítulo 10: Integración de Firebase – Autenticación

```{admonition} Objetivo
Aprender a integrar Firebase en un proyecto Vue 3 + Vite usando el SDK modular v9, implementar autenticación (email/contraseña y Google).
```

## Introducción
Firebase es una plataforma de backend como servicio que ofrece autenticación, base de datos, almacenamiento y más sin necesidad de desplegar servidores propios. En proyectos Vue, reduce el tiempo de arranque y permite centrarse en la experiencia de usuario.

En este capítulo veremos cómo usar el SDK modular v9 con Vue 3 + Vite para:
- Configurar Firebase en un proyecto existente.
- Implementar autenticación con email/contraseña y Google.
- Encapsular lógica en `/services` y componer vistas de añadir y editar entidades.

Usamos el SDK modular v9 porque es tree-shakeable (menor peso) y se integra bien con bundlers modernos como Vite.

### Dependencias a instalar
Antes de empezar, instala las librerías necesarias (si tu plantilla no las incluye):

```{code-block} bash
npm install firebase
npm install vue-router
npm install pinia
```

```{note}
- `firebase` es el SDK modular v9.
- `vue-router` se usa para las vistas de añadir/editar.
- `pinia` es opcional para el estado global del usuario.
```

Usaremos componentes simples; si tu proyecto ya tiene PrimeVue, puedes reutilizar sus botones e inputs (`Button`, `InputText`, `Textarea`). De lo contrario, usa inputs nativos como en los ejemplos.

## Alternativas similares
Aún centrándonos en Firebase, existen servicios BaaS con enfoques parecidos:
- **Supabase**: Postgres gestionado con API REST/GraphQL auto-generada, Auth (incluye providers OAuth), Realtime y storage. Ideal si prefieres SQL y quieres la potencia de Postgres.
- **Appwrite**: Plataforma open source que ofrece Auth, base de datos (documentos/colecciones), funciones y storage, con opción de desplegar on-premise.


## Configuración del proyecto Firebase
1. Crea un proyecto en la consola de Firebase ([firebase.google.com](https://firebase.google.com/)) y habilita Authentication y Firestore Database (modo producción o prueba temporal).
2. En Authentication → Métodos de acceso activa Email/Password y Google.
3. En la tarjeta de configuración web copia las claves del SDK (desde la [consola](https://console.firebase.google.com/)).
4. Añade variables de entorno en `.env.local` (prefijo `VITE_` para que Vite las exponga):

```{code-block} bash
VITE_FIREBASE_API_KEY=tu_api_key
VITE_FIREBASE_AUTH_DOMAIN=tu_auth_domain
VITE_FIREBASE_PROJECT_ID=tu_project_id
VITE_FIREBASE_STORAGE_BUCKET=tu_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=tu_sender_id
VITE_FIREBASE_APP_ID=tu_app_id
VITE_FIREBASE_MEASUREMENT_ID=tu_measurement_id
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/.env.example

Crea un `.env.example` con las mismas claves (vacías o con placeholders) para versionarlo y que el equipo sepa qué variables configurar. Mantén tu `.env.local` con los valores reales fuera del control de versiones.

```{warning}
Nunca publiques estos valores en repositorios públicos. Aunque no son credenciales secretas de backend, permiten interactuar con tu proyecto; protege Firestore con reglas. Deja `.env`, `.env.local` y variantes en el `.gitignore` y sube solo el `.env.example` sin credenciales reales.
```

Estructura recomendada para inicialización:
- `src/services/firebase.js` → inicializa app, auth, provider y db.
- `src/services/authService.js` → funciones de autenticación.

## Inicialización de Firebase en Vue
Archivo `src/services/firebase.js`:

```{code-block} javascript
// src/services/firebase.js
import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

const app = initializeApp(firebaseConfig)

export const auth = getAuth(app)
export const googleProvider = new GoogleAuthProvider()
export const db = getFirestore(app)
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/src/services/firebase.js

```{tip}
Extrae la inicialización a un solo archivo y reutiliza `auth` y `db` en los servicios para evitar múltiples instancias.
```

## Autenticación (Email/Password + Google)
Archivo `src/services/authService.js`:

```{code-block} javascript
// src/services/authService.js
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut as firebaseSignOut,
  signInWithPopup,
  onAuthStateChanged
} from 'firebase/auth'
import { auth, googleProvider } from './firebase'

export const signUp = (email, password) =>
  createUserWithEmailAndPassword(auth, email, password)

export const signIn = (email, password) =>
  signInWithEmailAndPassword(auth, email, password)

export const signOut = () => firebaseSignOut(auth)

export const signInGoogle = () => signInWithPopup(auth, googleProvider)

export const subscribeToAuth = (callback) =>
  onAuthStateChanged(auth, (user) => callback(user))
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/src/services/authService.js

### Mantener la sesión al recargar
Firebase Auth usa persistencia `local` por defecto en web, así que la sesión permanece tras recargar. Solo necesitas escuchar `onAuthStateChanged` al arrancar la app (por ejemplo, en el store o en `main.js`) y no renderizar la UI protegida hasta conocer el estado.

```{code-block} javascript
// src/main.js (ejemplo)
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { router } from './router'
import { subscribeToAuth } from '@/services/authService'
import { useUserStore } from '@/stores/user'

const app = createApp(App)
const pinia = createPinia()
  
app.use(router)
app.use(pinia)

let appMounted = false

subscribeToAuth((user) => {
    console.log('Auth state changed:', user)
    const userStore = useUserStore(pinia)
    userStore.currentUser = user

    if (!appMounted) {
        app.mount('#app')
        appMounted = true
    }
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/src/main.js

```{warning}
Si montas la app antes de conocer el usuario, podrías ver parpadeos en rutas protegidas. Esperar a `onAuthStateChanged` evita redirecciones innecesarias.
```

Ejemplo de componente de login sencillo:

```{code-block} vue
<template>
    <div class="flex justify-content-center align-items-center ">
        <Card class="login-card card flex flex-column align-items-center gap-4 col-12 md:col-6">
        <template #title>
                <h1>Iniciar sesión</h1>
            </template>
            <template #content>

            <Form
            v-slot="$form"
            :initialValues="initialValues"
            :resolver="resolver"
            @submit="onFormSubmit"
            class="p-fluid flex flex-column gap-4 w-full sm:w-18rem"
            >
            <!-- Email -->
            <div class="flex flex-column gap-1">
                <label for="email" class="p-mb-1">Email</label>
                <InputText
                id="email"
                name="email"
                type="email"
                placeholder="Email"
                autocomplete="email"
                fluid
                />
                <Message
                v-if="$form.email?.invalid"
                severity="error"
                size="small"
                variant="simple"
                >
                {{ $form.email.error.message }}
                </Message>
            </div>

            <!-- Password -->
            <div class="flex flex-column gap-1">
                <label for="password" class="p-mb-1">Contraseña</label>
                <Password
                id="password"
                name="password"
                toggleMask
                :feedback="false"
                placeholder="Contraseña"
                autocomplete="current-password"
                fluid
                />
                <Message
                v-if="$form.password?.invalid"
                severity="error"
                size="small"
                variant="simple"
                >
                {{ $form.password.error.message }}
                </Message>
            </div>

            <Button
                type="submit"
                label="Entrar"
                class="p-mt-2"
                :loading="loading"
            />

            </Form>

            <div class="p-mt-3 flex flex-row gap-2 mt-4">
            
            <Button
                label="Continuar con Google"
                icon="pi pi-google"
                class="p-button-secondary w-full"
                type="button"
                @click="handleGoogle"
            />
            </div>
            </template>
        </Card>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { z } from 'zod'
import { Form } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import { useRouter } from 'vue-router'
const router = useRouter()

import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Message from 'primevue/message'
import Button from 'primevue/button'

import {
    signIn,
    signInGoogle,
    subscribeToAuth,
    signOut
} from '@/services/authService'

const user = ref(null)
const loading = ref(false)
let unsubscribe = null

// Estado inicial controlado por <Form>
const initialValues = ref({
    email: '',
    password: ''
})

// Esquema Zod para email y contraseña
const resolver = ref(
    zodResolver(
        z.object({
        email: z
            .string()
            .min(1, { message: 'El email es obligatorio' })
            .email({ message: 'El email no es válido' }),
        password: z
            .string()
            .min(6, { message: 'La contraseña debe tener al menos 6 caracteres' })
        })
    )
)

// onSubmit del Form de PrimeVue
const onFormSubmit = async ({ valid, values }) => {
    if (!valid) return

    loading.value = true
    try {
        await signIn(values.email, values.password)
        router.push('/panel')
    } catch (err) {
        console.error('Error al iniciar sesión', err)
        // aquí podrías añadir un Message global o Toast
    } finally {
        loading.value = false
    }
}

const handleGoogle = async () => {
    try {
        await signInGoogle()
    } catch (err) {
        console.error('Error con Google', err)
    }
}

const handleSignOut = () => {
    signOut()
}

onMounted(() => {
    unsubscribe = subscribeToAuth((currentUser) => {
        user.value = currentUser
    })
})

onUnmounted(() => {
    if (unsubscribe) unsubscribe()
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/src/views/Login.vue

```{tip}
Para que el ejemplo funcione con PrimeVue, asegúrate de haber instalado `primevue` y sus estilos, y de registrar el tema y los componentes según tu configuración de `main.js`.
```

Uso opcional de Pinia para estado de usuario (`src/stores/user.js`):

```{code-block} javascript
// src/stores/user.js
import { defineStore } from 'pinia'
import { ref, onMounted, onUnmounted } from 'vue'
import { subscribeToAuth } from '@/services/authService'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null)
  let unsubscribe = null

  const startAuthListener = () => {
    if (unsubscribe) return
    unsubscribe = subscribeToAuth((user) => {
      currentUser.value = user
    })
  }

  const stopAuthListener = () => {
    if (unsubscribe) unsubscribe()
    unsubscribe = null
  }

  onMounted(startAuthListener)
  onUnmounted(stopAuthListener)

  return { currentUser, startAuthListener, stopAuthListener }
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/src/stores/user.js

## Vistas protegidas y configuración del router
Protege rutas según el estado de autenticación para evitar que usuarios no logueados accedan a páginas internas.

`src/router/index.js`:

```{code-block} javascript
import { createRouter, createWebHistory } from 'vue-router'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from '@/services/firebase'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/Home.vue') },
  {
    path: '/panel',
    name: 'panel',
    component: () => import('@/views/Panel.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Devuelve el usuario actual una sola vez (promesa) para usar en el guard.
const getCurrentUser = () =>
  new Promise((resolve, reject) => {
    const unsubscribe = onAuthStateChanged(
      auth,
      (user) => {
        unsubscribe()
        resolve(user)
      },
      reject
    )
  })

router.beforeEach(async (to) => {
  const user = await getCurrentUser()

  if (to.meta.requiresAuth && !user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresGuest && user) {
    return { name: 'panel' }
  }

  return true
})

export {router}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/10_firebase_auth/src/router/index.js

Flujo del guard:
- `getCurrentUser()` envuelve `onAuthStateChanged` en una promesa y se desuscribe en cuanto obtiene al usuario actual; así evitas listeners duplicados y puedes usar `await` dentro de `beforeEach`.
- Si la ruta requiere autenticación y no hay usuario, redirige a `login` cargando el `redirect` original en la query. Una vez logueado, lee esa query y retorna a la ruta inicial.
- Si la ruta es solo para invitados (`requiresGuest`) y ya hay sesión, redirige al `panel`.


## Buenas prácticas
- No expongas credenciales en el cliente;
- Encapsula Firebase en `/services` para mantener componentes limpios.
- Maneja errores con `try/catch` y muestra feedback al usuario.
- Protege rutas con `meta` + `beforeEach` y evita montar la app antes de conocer el usuario.


## Ejercicios
1. Implementa vistas de registro y recuperación de contraseña (`register`, `forgot-password`) usando los métodos de Auth y enlázalas desde el login.
2. Añade un botón de logout que solo se muestre en el panel (rutas protegidas) y verifica la redirección a `/login` tras cerrar sesión.
3. Crear un menu dinámico que muestre opciones diferentes según si el usuario está autenticado o no (por ejemplo, "Login" y "Register" para invitados, "Panel" y "Logout" para usuarios logueados).
