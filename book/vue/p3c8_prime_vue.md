% Capítulo 8 se definirá en la tabla de contenidos principal del libro.

# Capítulo 8: Instalación y Configuración de PrimeVue

```{admonition} Objetivo
Guiar la incorporación de PrimeVue en un proyecto creado con Vite y Vue 3, incluyendo la configuración del tema Aura, la integración con Pinia y Vue Router, y el uso del auto-importador de componentes.
```

## Prerrequisitos

- Haber creado un proyecto base con `npm create vite@latest nombre-proyecto -- --template vue`.
- Contar con Node.js y npm instalados.
- Conocer la estructura de un proyecto Vite (carpetas `src`, `public`, `vite.config.js`).



```{admonition} Decisión del equipo
En el curso se dio libertad al estudiantado para elegir la biblioteca UI y el grupo optó por PrimeVue. Existen alternativas como Vuetify, Quasar o Naive UI, pero cada una cuenta con su propia guía de instalación y configuración; en este capítulo nos enfocamos exclusivamente en PrimeVue.
```

## Introducción

PrimeVue es una biblioteca moderna de componentes UI con más de 90 opciones listas para usar: botones, tarjetas, tablas, menús, formularios, diálogos y más. Cada componente se acompaña de temas personalizables, soporte para iconos y utilidades de maquetación.

Su diseño modular facilita la integración con Vite, Pinia y Vue Router: los componentes se pueden cargar de forma automática, aprovechar el enrutador para crear vistas dinámicas y consumir el estado global desde Pinia sin configuraciones extra.

## Instalación de PrimeVue y dependencias

Desde la raíz del proyecto Vite, instala las dependencias principales, el tema Aura, los iconos y las utilidades.

```{code-block} bash
npm install primevue @primeuix/themes primeicons primeflex @primevue/auto-import-resolver unplugin-vue-components
```

- `primeflex` incorpora clases utilitarias de espaciado, grillas y alineación.
- `primeicons` ofrece más de 200 iconos vectoriales listos para usar con PrimeVue.
- `@primeuix/themes` contiene los temas oficiales (Aura, Lara, Nora), compatibles con el motor de temas unificado de Prime.

```{warning}
Asegúrate de revisar el archivo `package.json`. Si tienes dependencias antiguas como `primevue/resources/themes`, elimínalas para evitar conflictos con la nueva estructura de temas.
```

## Configuración principal (`src/main.js`)

El punto de entrada inicializa Vue, PrimeVue, Vue Router, Pinia y ToastService. También importa los estilos globales de PrimeFlex y PrimeIcons.

```{code-block} javascript
import { createApp } from 'vue'
import './style.css'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import App from './App.vue'
import { router } from './router'
import { createPinia } from 'pinia'
import ToastService from 'primevue/toastservice'

const app = createApp(App)

app.use(PrimeVue, {
  theme: {
    preset: Aura
  }
})
app.use(router)
app.use(createPinia())
app.use(ToastService)

app.mount('#app')
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/08_prime_vue/src/main.js

```{note}
Si tu proyecto aún no integra Router o Pinia, comenta sus importaciones y usos. En cuanto los incorpores deberás habilitar estas líneas para que PrimeVue comparta el contexto con ambos plugins.
```

Este bloque importa el tema Aura desde `@primeuix/themes/aura` y mantiene activos los estilos de PrimeVue, PrimeFlex y PrimeIcons en toda la aplicación. Si deseas delegar la configuración en un plugin, crea un archivo `src/plugins/primevue.js` y úsalo desde `main.js`.

```{tip}
Aura dispone de variantes claras y oscuras. Puedes cambiarlo dinámicamente usando `app.config.globalProperties.$primevue.config.theme.setPreset(...)` o reaccionando a la preferencia del sistema operativo.
```

## Configuración del plugin de Vite (`vite.config.js`)

El plugin `unplugin-vue-components` evita importar manualmente cada componente. Se combina con `@primevue/auto-import-resolver` para detectar el catálogo de PrimeVue.

```{code-block} javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { PrimeVueResolver } from '@primevue/auto-import-resolver'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [
        PrimeVueResolver()
      ]
    })
  ]
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/08_prime_vue/vite.config.js

Gracias a `PrimeVueResolver`, componentes como `<Button />`, `<Card />` o `<Dialog />` se registran automáticamente cuando aparecen en las plantillas. No es necesario importarlos ni registrarlos de forma global.

## Ejemplo: componente con PrimeVue (`src/App.vue`)

El siguiente ejemplo usa Composition API (`<script setup>`) y demuestra cómo disparar notificaciones con ToastService y renderizar componentes sin importaciones manuales.

```{code-block} vue
<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const clicks = ref(0)

function notify() {
  clicks.value++
  toast.add({
    severity: 'success',
    summary: 'Acción registrada',
    detail: `Has hecho clic ${clicks.value} veces`,
    life: 2500
  })
}
</script>

<template>
  <main class="p-4 surface-card border-round shadow-2 flex flex-column gap-3">
    <div class="flex align-items-center gap-2">
      <i class="pi pi-vuejs text-2xl text-primary"></i>
      <h1 class="m-0">PrimeVue + Vite</h1>
    </div>

    <p>
      Este componente usa PrimeFlex para la maquetación y PrimeIcons para los iconos.
      Los botones y toasts provienen de PrimeVue.
    </p>

    <div class="flex gap-2">
      <Button label="Mostrar Toast" icon="pi pi-bell" @click="notify" />
      <Button label="Reiniciar" icon="pi pi-refresh" severity="secondary" outlined @click="clicks = 0" />
    </div>

    <Card>
      <template #title>Estado</template>
      <template #content>
        <p>Clicks actuales: <strong>{{ clicks }}</strong></p>
      </template>
    </Card>
    <Toast />
  </main>
</template>

<style scoped>
main {
  max-width: 480px;
  margin: 2rem auto;
}
</style>
```

Este ejemplo confirma que `<Button>`, `<Card>` y `<Toast>` se resuelven automáticamente a través del plugin configurado en `vite.config.js`.

## Integración con Router y Pinia

PrimeVue se combina con enrutamiento y estado global para crear vistas completas. Los siguientes fragmentos muestran una configuración mínima de rutas y un store con Pinia.

### Router (`src/router/index.js`)

```{code-block} javascript
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/about', component: About }
  ]
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/08_prime_vue/src/router/index.js

### Store (`src/stores/counter.js`)

```{code-block} javascript
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: {
    increment() {
      this.count++
    }
  }
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/08_prime_vue/src/stores/counter.js

### Vista que combina PrimeVue + Router + Pinia (`src/views/Home.vue`)

```{code-block} vue
<script setup>
import { computed } from 'vue'
import { useCounterStore } from '../stores/counter'
import { useToast } from 'primevue/usetoast'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const toast = useToast()
const router = useRouter()

const doubled = computed(() => store.count * 2)

function increment() {
  store.increment()
  toast.add({
    severity: 'info',
    summary: 'Contador actualizado',
    detail: `Nuevo valor: ${store.count}`,
    life: 3000
  })
}

function goAbout() {
  router.push('/about')
}
</script>

<template>
  <section class="surface-card border-round p-4 shadow-1 flex flex-column gap-3">
    <h2 class="m-0">Inicio</h2>
    <p>Valor: {{ store.count }} (doble: {{ doubled }})</p>
    <div class="flex gap-2">
      <Button label="Incrementar" icon="pi pi-plus" @click="increment" />
      <Button label="Ir a About" icon="pi pi-arrow-right" severity="help" @click="goAbout" />
    </div>
    <Toast />
  </section>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/08_prime_vue/src/views/Home.vue

### Vista secundaria (`src/views/About.vue`)

```{code-block} vue
<template>
  <section class="surface-card border-round p-4 shadow-1 flex flex-column gap-3">
    <h2 class="m-0">About</h2>
    <p>
      Esta vista confirma que Vue Router funciona en conjunto con PrimeVue.
      Puedes agregar tablas, menús o gráficas sin configuraciones extras.
    </p>
    <Card>
      <template #subtitle>PrimeFlex</template>
      <template #content>
        <p class="m-0">
          Las utilidades de PrimeFlex te permiten crear layouts responsivos sin CSS personalizado.
        </p>
      </template>
    </Card>
  </section>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/08_prime_vue/src/views/About.vue

## Buenas prácticas

- Mantén la configuración global de PrimeVue en `src/main.js` o en `src/plugins/primevue.js` para centralizar cambios de tema.
- Activa `unplugin-vue-components` para evitar importaciones manuales y mantener los componentes sincronizados.
- Usa PrimeFlex para maquetar; reduce la necesidad de CSS personalizado.
- Coloca estilos globales en `src/style.css` o `src/theme.css` y evita mezclar PrimeVue con frameworks de utilidades (p. ej., Tailwind) a menos que conozcas los posibles conflictos.
- Utiliza `ToastService` para notificaciones globales en lugar de `alert()`.
- Actualiza periódicamente `@primeuix/themes`, `primeicons` y `primevue` para obtener correcciones de seguridad y compatibilidad con nuevas versiones de Vue.

## Resumen

- PrimeVue ofrece una colección completa de componentes rápidos de integrar.
- La combinación Vite + `unplugin-vue-components` simplifica el registro automático.
- Pinia, Vue Router y ToastService se integran sin configuraciones adicionales.
- El tema Aura brinda un diseño moderno, adaptable y compatible con modo oscuro.
