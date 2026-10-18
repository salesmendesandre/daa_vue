# Capítulo 1: Introducción a Vue.js


## Prerrequisitos
- Conocimientos básicos de HTML, CSS y JavaScript (DOM, funciones, módulos).
- Node.js LTS instalado (`node --version` debe devolver la versión).
- Disponer de npm, yarn o pnpm; usa el gestor habitual del proyecto.
- Editor de código con soporte para Vue (VS Code o similar) y extensiones recomendadas.
- Navegador moderno con herramientas de desarrollo activadas.

:::{note}
Si trabajas en laboratorio, comprueba que tienes permisos de escritura en el directorio donde crearás el proyecto y acceso a la red para instalar dependencias.
:::


## Introducción
Vue.js se presenta como un framework progresivo que se integra de forma incremental. Este capítulo describe por qué elegir Vue en proyectos de frontend, qué lo diferencia de React y Angular, y cómo ponerlo en marcha con Vite. Verás cómo funciona la reactividad, la estructura básica de un proyecto y las buenas prácticas para comenzar con rigor profesional.


## ¿Qué es Vue.js y por qué elegirlo?
Vue.js es un framework JavaScript enfocado a la capa de vista que permite construir interfaces reactivas, tanto para Single Page Applications (SPA) como para experiencias multipágina (MPA) gracias a sus herramientas oficiales. Su diseño progresivo permite usarlo desde un widget aislado hasta una aplicación compleja.

### Ventajas clave
- **Componentes de fichero único (SFC)**: agrupan plantilla, lógica y estilos en `.vue`, facilitando el razonamiento y el intercambio de componentes.
- **Composition API**: organiza la lógica por funcionalidades, favoreciendo la reutilización frente a la Options API (aún soportada para compatibilidad y transición).
- **Ecosistema oficial cohesionado**: Vue Router, Pinia, Devtools, Test Utils y el CLI histórico simplifican decisiones arquitectónicas.
- **Curva de aprendizaje suave**: la sintaxis templating es una extensión declarativa de HTML; resulta familiar al alumnado que ya domina el DOM.
- **Rendimiento competitivo**: su runtime ligero y el renderizado virtual optimizado permiten entregar SPA rápidas sin sacrificar DX.
- **Documentación y comunidad**: abundan recursos en español y ejemplos open source actualizados.

### Cuándo sí elegir Vue
- Equipos que priorizan escribir lógica declarativa sin sacrificar legibilidad.
- Proyectos que requieren integración progresiva en páginas existentes.
- Aplicaciones donde el equipo valora una curva de aprendizaje accesible y herramientas oficiales maduras.
- Necesidad de soporte para SSR/SSG (Nuxt, Vite SSR) con un stack bien documentado.

### Cuándo considerar alternativas
- Organizaciones fuertemente estandarizadas en React o Angular con tooling interno específico.
- Proyectos que dependen de bibliotecas con bindings oficiales exclusivos para otro framework.
- Equipos que exigen TypeScript estricto desde el primer día podrían preferir Angular por su integración prescriptiva (Vue soporta TS de forma opcional, no obligatoria).


## Comparativa con React y Angular

| Criterio | Vue.js | React | Angular |
|----------|--------|-------|---------|
| Paradigma | Progresivo, MVVM orientado a componentes | Biblioteca de UI declarativa | Framework completo basado en componentes y DI |
| Curva de aprendizaje | Suave, sintaxis similar a HTML | Media, requiere JSX y hooks | Pronunciada, concepto de módulos y decoradores |
| Lenguaje por defecto | JavaScript, soporte TS opcional | JavaScript/JSX, TS oficial opcional | TypeScript obligatorio |
| Tipado | Opcional con `<script setup>` y JSDoc (TypeScript disponible si se requiere) | Opcional con `tsx` | Estricto, plantillas tipadas |
| Enrutamiento oficial | Vue Router | React Router (comunidad) | Angular Router (core) |
| Estado global | Pinia (oficial) | Redux/MobX/Zustand (ecosistema) | NgRx o servicios con DI |
| Renderizado del lado del servidor (SSR) | Integrado vía Vite + plugins o Nuxt | Next.js / Remix (terceros) | Angular Universal (core) |
| Tamaño inicial | ~33 KB gzip | ~43 KB gzip | ~66 KB gzip |
| DX (Developer Experience) | SFC, Devtools, script setup | Hooks, Fast Refresh | CLI, esquemas, tooling oficial |
| Adopción empresarial | Alta en pymes y productos digitales | Muy alta en grandes empresas | Alta en entornos corporativos y sector público |
| Actualización de versiones | Compatibilidad conservadora | Cambios frecuentes en ecosistema | Releases semestrales con LTS |
| Filosofía | Equilibrio entre flexibilidad y convenciones | Libertad, mínima capa opinada | Fortemente opinado y estructurado |

- **Vue.js** destaca por su capacidad progresiva y un ecosistema cohesionado que reduce decisiones iniciales.
- **React** ofrece mayor flexibilidad y un ecosistema enorme, a cambio de más responsabilidad en arquitectura.
- **Angular** resulta idóneo cuando se busca un marco completo con DI, CLI, testing y recomendaciones cerradas.

:::{tip}
La elección depende del contexto: experiencia del equipo, requisitos técnicos (SSR, microfrontends, legado) y políticas internas de la organización.
:::


## Filosofía del framework: reactividad, simplicidad y escalabilidad
La filosofía de Vue se apoya en tres pilares: reactividad, simplicidad y escalabilidad. Verlos en acción ayuda a comprender decisiones de diseño.

### Reactividad granular
Vue usa proxies y colecciones específicas (`ref`, `reactive`) para detectar cambios. Las dependencias se rastrean automáticamente y las vistas se actualizan de manera eficiente.

```{code-block} javascript
:caption: Patrón básico de reactividad con Composition API
import { ref, reactive, computed, watch } from 'vue'

const clicks = ref(0)
const profile = reactive({
  name: 'Ada Lovelace',
  skills: ['Matemáticas', 'Programación']
})

const summary = computed(() => `${profile.name} (${clicks.value} clics)`)

watch(clicks, (value, previous) => {
  console.log(`Clicks cambiaron de ${previous} a ${value}`)
})

const increment = () => {
  clicks.value++
}
```

Cada actualización de `clicks` o `profile` notifica a la vista sin necesidad de manipular directamente el DOM. Esta granularidad evita renders innecesarios y simplifica el seguimiento del flujo de datos.

### Simplicidad con SFC y `<script setup>`
Los Single File Components encapsulan la pieza funcional mínima: plantilla declarativa, lógica en `<script>` y estilos scoped. El modo `<script setup>` reduce el código ceremonial y habilita Composition API de forma natural.

```{code-block} vue
:caption: Contador reactivo con Composition API
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

const inc = () => {
  count.value++
}
</script>

<template>
  <button @click="inc">
    Contador: {{ count }} (x2 = {{ doubled }})
  </button>
</template>
```

El estado se declara con `ref`, las derivaciones con `computed`, y los manejadores de eventos actualizan la vista sin manipular el DOM manualmente.

### Escalabilidad modular
- **Organización por dominios**: agrupa componentes, composables y pruebas por contexto (`/src/modules/users`), reduciendo dependencias cruzadas.
- **Rutas con carga perezosa**: Vue Router permite dividir el código en chunks (`() => import('./views/Dashboard.vue')`).
- **Estado global con Pinia**: gestiona datos compartidos sin reactividad oculta; soporta SSR y devtools.
- **Testing y calidad**: Vitest, Vue Test Utils y Cypress cubren pruebas unitarias, de componentes e integración end-to-end.
- **Internacionalización y accesibilidad**: Vue I18n, resaltado de accesibilidad en Devtools y componentes accesibles desde el diseño.


## Crear el primer proyecto con Vite
Vite es la herramienta recomendada para scaffolding moderno en Vue 3. Ofrece arranque instantáneo, HMR (Hot Module Replacement) eficiente y soporte tanto para JavaScript como TypeScript.

:::{tab-set}

:::{tab-item} npm
```{code-block} bash
:caption: Crear proyecto con Vite + Vue
npm create vite@latest my-vue-app -- --template vue

#Si no hemos indicado que instale las dependencias y que se ejecute:
cd my-vue-app
npm install
npm run dev
```
:::


### Verificación
- La consola debe mostrar una URL local, habitualmente `http://localhost:5173/`.
- Al abrir la URL, Vite servirá la plantilla de bienvenida de Vue 3 con un contador interactivo.
- La terminal indica el tiempo de arranque y los accesos en LAN (si están disponibles).

### Solución de problemas comunes
- **Node desactualizado**: ejecuta `node --version` y usa la LTS recomendada; si no coincide, reinstala Node o usa un gestor como nvm.
- **Puerto ocupado**: añade `--port 3000` a `npm run dev` o detén el proceso en conflicto.
- **Permisos en directorios protegidos**: crea el proyecto en tu home o usa un directorio con permisos de escritura.
- **Problemas con antivirus o firewall**: habilita Vite en la red local o ejecuta el servidor en modo `--host 127.0.0.1`.

:::{warning}
No ejecutes Vite como superusuario para evitar conflictos con archivos generados. Corrige permisos o elige un directorio diferente.
:::


## Estructura de un proyecto Vue
Una vez generado el proyecto, revisa la estructura creada por Vite.

```
my-vue-app/
├─ index.html
├─ package.json
├─ vite.config.js
├─ src/
│  ├─ main.js
│  ├─ App.vue
│  ├─ assets/
│  └─ components/
└─ node_modules/
```

- `index.html`: punto de entrada servible; Vite inyecta scripts y estilos de desarrollo o producción.
- `package.json`: lista dependencias, scripts y metadatos del proyecto.
- `vite.config.js` (o `.ts` si habilitas TypeScript): configuración de bundling, aliases y plugins.
- `src/main.js`: arranque de la aplicación, monta el componente raíz.
- `src/App.vue`: componente principal donde se declaran vistas de alto nivel.
- `src/components/`: componentes reutilizables.
- `src/assets/`: recursos estáticos procesados por Vite (imágenes, fuentes, estilos).

### Montaje de la aplicación

```{code-block} javascript
:caption: `src/main.js`
import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'

createApp(App).mount('#app')
```

`createApp` genera una instancia de la aplicación que se monta en el elemento `#app` definido en `index.html`. Puedes registrar plugins, rutas o stores antes del `mount`.

### Componentes de ejemplo
`App.vue` puede importar componentes hijos y gestionarlos como cualquier elemento HTML:

```{code-block} vue
:caption: `src/components/Greeting.vue`
<script setup>
const props = defineProps({
    name: String
})

const emit = defineEmits(['greet'])

const onClick = () => {
    emit('greet')
}
</script>



<template>
<section class="greeting">
    <p>Hola, {{ props.name }} 👋</p>
    <button @click="onClick">Saludar</button>
</section>
</template>

<style scoped>
.greeting {
    display: grid;
    gap: 0.5rem;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/01_introduction/src/components/Greeting.vue

```{code-block} vue
:caption: `src/App.vue`
<script setup>
import { ref } from 'vue'
import Greeting from './components/Greeting.vue'

const username = ref('Estudiante Vue')

const handleGreet = () => {
  console.log(`Saludo recibido de ${username.value}`)
}
</script>

<template>
  <main>
    <h1>Bienvenido a Vue 3</h1>
    <Greeting :name="username" @greet="handleGreet" />
  </main>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/01_introduction/src/App.vue

El componente `Greeting` muestra cómo definir props con validaciones básicas y emitir eventos personalizados. `App.vue` ilustra cómo manejar eventos y estado local.


## Buenas Prácticas
- Emplea Composition API con `<script setup>` para agrupar lógica por funcionalidad desde el inicio.
- Nombrado consistente: componentes en PascalCase (`UserCard.vue`), props y eventos en camelCase.
- Distingue estado local (componentes) de global: usa Pinia solo cuando múltiples componentes precisan el mismo estado.
- Separa responsabilidades creando composables (`/src/composables/useFetch.js`) para lógica reusable y componentes presentacionales para la UI.
- Documenta contratos con JSDoc para aclarar las expectativas entre componentes.
- Cuida la accesibilidad: etiquetas semánticas, `aria-*` y gestión del foco en componentes interactivos.
- Cubre test unitarios con Vitest y Vue Test Utils para lógica crítica; automatiza con CI desde etapas tempranas.
- Configura linters y formateadores (ESLint + Prettier) para mantener un estilo uniforme.
- Gestiona variables de entorno con `.env` y `.env.local`, evitando exponer secretos en el repositorio.
- Define rutas con lazy loading y nombres únicos (`name: 'dashboard'`) para simplificar navegación y guardas.
- Evita antipatrones: no mutar props, evita efectos secundarios en `setup`, usa `watch`/`watchEffect` con limpieza.
- Documenta convenciones de carpetas (por dominio, funcionalidad o capas) y revísalas periódicamente en revisiones de código.


## Resumen
- Vue.js combina reactividad granular con un enfoque progresivo que facilita su adopción.
- La Composition API y los SFC ofrecen claridad y reutilización de lógica sin perder legibilidad.
- Vite permite crear proyectos Vue 3 en minutos con HMR y configuración mínima.
- La arquitectura modular (rutas, stores, composables) sostiene el crecimiento y el mantenimiento.
- Las buenas prácticas iniciales garantizan calidad, accesibilidad y coherencia desde el primer commit.


## Ejercicios o Actividades
1. **Primer proyecto completo**: crea un proyecto Vue 3 con Vite usando tu gestor de paquetes habitual.
   - Ejecuta el comando `node --version` para confirmar que tienes una versión LTS instalada.
   - Inicializa el proyecto con `npm create vite@latest my-vue-app -- --template vue`, instala las dependencias y arranca el servidor de desarrollo.
   - Dentro de `src/components/`, añade `Greeting.vue` que reciba una prop `name`, muestre un saludo y exponga un botón que emita un evento `greet`.
   - Modifica `App.vue` para importar `Greeting.vue`, pasarle un nombre y escuchar el evento `greet`, registrando un mensaje en la consola del navegador.
