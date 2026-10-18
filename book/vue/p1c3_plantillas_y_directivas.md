# Capítulo 3: Interpolación, Directivas y Slots


## Prerrequisitos
- Haber completado los capítulos anteriores y disponer del proyecto base con Vue 3 + Vite.
- Conocer la estructura de `src/` y el uso de `<script setup>` en componentes.
- Tener nociones de props y eventos básicos ya presentados.


## Introducción
Las directivas de Vue son atributos especiales que conectan los datos reactivos con el DOM. Gracias a la interpolación (`{{ }}`) y a directivas como `v-if` o `v-for`, la interfaz responde automáticamente a los cambios de estado. Además, los slots permiten inyectar contenido personalizado dentro de componentes, aumentando la reutilización. Este capítulo muestra cómo combinar estas herramientas para construir vistas expresivas y mantenibles.


## Interpolación y vinculación de datos

:::{admonition} Objetivo
Aprender a mostrar datos reactivos y a vincularlos con atributos HTML y clases dinámicas.
:::

### Interpolación con `{{ }}`
La interpolación muestra valores reactivos dentro de la plantilla.

```{code-block} vue
:caption: `src/components/SaludoInterpolacion.vue`
<template>
  <section>
    <h1>Hola, {{ nombre }}</h1>
    <p>Hoy es {{ diaSemana }}</p>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const nombre = ref('Estudiante Vue')
const fecha = ref(new Date())

const diaSemana = computed(() =>
  fecha.value.toLocaleDateString('es-ES', { weekday: 'long' })
)
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/01_data_interpolation/src/components/SaludoInterpolacion.vue

Vue actualiza automáticamente las interpolaciones cuando cambian los valores en `nombre` o `diaSemana`.

### `v-text` y `v-html`
`v-text` inserta contenido textual y reemplaza lo que haya dentro del elemento. `v-html` inyecta HTML sin escapar, por lo que requiere precaución.

```{code-block} vue
:caption: `src/components/TextosDirectivas.vue`
<template>
  <article>
    <h2 v-text="titulo"></h2>
    <p v-text="mensajePlano"></p>
    <div v-html="mensajeConFormato"></div>
  </article>
</template>

<script setup>
const titulo = 'Directivas de texto'
const mensajePlano = 'Este párrafo se establece con v-text.'
const mensajeConFormato = '<strong>Mensaje destacado</strong> con <em>énfasis</em>.'
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/01_data_interpolation/src/components/TextosDirectivas.vue

:::{warning}
Usa `v-html` solo con contenido de confianza. Insertar HTML sin control puede exponer tu aplicación a ataques XSS (Cross-Site Scripting).
:::

### `v-bind` y atributos dinámicos
`v-bind` enlaza datos con atributos HTML. La forma abreviada `:` mejora la legibilidad.

```{code-block} vue
:caption: `src/components/EnlaceDinamico.vue`
<template>
  <a :href="url" :title="descripcion">
    Visitar documentación
  </a>
</template>

<script setup>
const url = 'https://vuejs.org'
const descripcion = 'Sitio oficial de Vue'
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/01_data_interpolation/src/components/EnlaceDinamico.vue

También puedes gestionar clases y estilos dinámicos usando objetos o arrays.

```{code-block} vue
:caption: `src/components/EstadoTarjeta.vue`
<template>
  <section :class="['tarjeta', estadoClass]">
    <h3>{{ titulo }}</h3>
    <p>{{ descripcion }}</p>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const titulo = ref('Pedido #1234')
const descripcion = ref('Preparando envío')
const estado = ref('pendiente') // puede ser pendiente, enviado, entregado

const estadoClass = computed(() => ({
  pendiente: 'tarjeta--pendiente',
  enviado: 'tarjeta--enviado',
  entregado: 'tarjeta--entregado'
}[estado.value]))
</script>

<style scoped>
.tarjeta {
  border-radius: 8px;
  padding: 1rem;
  color: #0f172a;
}

.tarjeta--pendiente {
  background-color: #fef3c7;
}

.tarjeta--enviado {
  background-color: #bfdbfe;
}

.tarjeta--entregado {
  background-color: #bbf7d0;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/01_data_interpolation/src/components/EstadoTarjeta.vue


## Condicionales con `v-if`, `v-else`, `v-show`

:::{admonition} Objetivo
Renderizar elementos de forma condicional según el estado de la aplicación.
:::

`v-if` agrega o elimina elementos del DOM según la condición; `v-else` o `v-else-if` establecen ramas alternativas. `v-show` controla la visibilidad con CSS (`display: none`), manteniendo el nodo en el DOM.

```{code-block} vue
:caption: `src/components/EstadoUsuario.vue`
<template>
  <section>
    <p v-if="isLoggedIn">Bienvenido, {{ nombre }}</p>
    <p v-else>Identifícate para continuar.</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const isLoggedIn = ref(true)
const nombre = ref('María')
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/02_conditionals_and_iterations/src/components/EstadoUsuario.vue

```{code-block} vue
:caption: `src/components/DetalleProducto.vue`
<template>
  <article>
    <h2>{{ producto.nombre }}</h2>
    <button @click="mostrarDetalles = !mostrarDetalles">
      {{ mostrarDetalles ? 'Ocultar' : 'Mostrar' }} detalles
    </button>
    <p v-show="mostrarDetalles">
      {{ producto.descripcion }}
    </p>
  </article>
</template>

<script setup>
import { reactive, ref } from 'vue'

const producto = reactive({
  nombre: 'Teclado Mecánico',
  descripcion: 'Switches silenciosos, retroiluminación RGB y reposamuñecas.'
})

const mostrarDetalles = ref(false)
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/02_conditionals_and_iterations/src/components/DetalleProducto.vue

:::{tip}
Usa `v-if` cuando los elementos cambian raramente y `v-show` cuando necesitas alternar la visibilidad con frecuencia.
:::


## Iteraciones con `v-for`

:::{admonition} Objetivo
Generar listas y tablas a partir de colecciones reactivas manteniendo claves únicas.
:::

`v-for` itera sobre arrays, objetos o rangos. Siempre añade `:key` para ayudar a Vue a identificar cada elemento. El valor de `:key` debe ser único y estable.

```{code-block} vue
:caption: `src/components/ListaTareas.vue`
<template>
  <section>
    <h2>Lista de tareas</h2>
    <ul>
      <li v-for="tarea in tareas" :key="tarea.id">
        <span :class="{ completada: tarea.completada }">
          {{ tarea.titulo }}
        </span>
      </li>
    </ul>
  </section>
</template>

<script setup>
import { reactive } from 'vue'

const tareas = reactive([
  { id: 1, titulo: 'Preparar presentación', completada: true },
  { id: 2, titulo: 'Revisar pull requests', completada: false },
  { id: 3, titulo: 'Planificar la demo', completada: false }
])
</script>

<style scoped>
.completada {
  text-decoration: line-through;
  color: #94a3b8;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/02_conditionals_and_iterations/src/components/ListaTareas.vue

Cuando iteras objetos, puedes acceder a clave y valor.

```{code-block} vue
:caption: `src/components/ResumenPedidos.vue`
<template>
  <dl>
    <template v-for="(valor, clave) in resumen" :key="clave">
      <dt>{{ clave }}</dt>
      <dd>{{ valor }}</dd>
    </template>
  </dl>
</template>

<script setup>
const resumen = {
  'Pedidos activos': 7,
  'Pedidos completados': 24,
  'Pendientes de envío': 3
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/02_conditionals_and_iterations/src/components/ResumenPedidos.vue


## Manejo de eventos con `v-on`

:::{admonition} Objetivo
Escuchar interacciones del usuario y ejecutar lógica en respuesta a eventos del DOM.
:::

`v-on` enlaza eventos (`click`, `input`, `submit`, etc.) con funciones. Su abreviatura `@` simplifica la sintaxis.

Algunos eventos habituales que encontrarás al trabajar con componentes son:
- **Eventos de ratón**: `click`, `dblclick`, `contextmenu`, `mouseenter`, `mouseleave`.
- **Eventos de teclado**: `keydown`, `keyup`, `keypress` (útiles con modificadores como `.enter` o `.escape`).
- **Eventos de formulario**: `submit`, `reset`, `change`, `input`.
- **Eventos de foco**: `focus`, `blur`.
- **Eventos personalizados**: emitidos con `emit` desde componentes hijos para comunicar acciones hacia el padre.

```{code-block} vue
:caption: `src/components/ContadorBasico.vue`
<template>
  <section>
    <p>Conteo actual: {{ contador }}</p>
    <button @click="incrementar">Incrementar</button>
    <button @click="resetear">Reset</button>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const contador = ref(0)

const incrementar = () => {
  contador.value++
}

const resetear = () => {
  contador.value = 0
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/03_events/src/components/ContadorBasico.vue

Puedes pasar parámetros en los manejadores.

```{code-block} vue
:caption: `src/components/ContadorFlexible.vue`
<template>
  <section>
    <p>Valor: {{ valor }}</p>
    <button @click="incrementar(1)">+1</button>
    <button @click="incrementar(5)">+5</button>
    <button @click="decrementar(2)">-2</button>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const valor = ref(10)

const incrementar = (cantidad) => {
  valor.value += cantidad
}

const decrementar = (cantidad) => {
  valor.value -= cantidad
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/03_events/src/components/ContadorFlexible.vue

Cuando necesitas reaccionar a pulsaciones del teclado, `@keyup` te permite validar o enviar información al instante. En formularios de acceso es común habilitar el envío con Enter.

```{code-block} vue
:caption: `src/components/FormularioLogin.vue`
<template>
  <form class="login" @submit.prevent="intentarLogin">
    <label for="email">Correo</label>
    <input
      id="email"
      type="email"
      placeholder="tucorreo@ejemplo.com"
      v-model="credenciales.email"
      @keyup="limpiarMensaje"
    />

    <label for="password">Contraseña</label>
    <input
      id="password"
      type="password"
      placeholder="Ingresa tu clave"
      v-model="credenciales.password"
      @keyup="limpiarMensaje"
      @keyup.enter="intentarLogin"
    />

    <button type="submit">Acceder</button>

    <p v-if="mensaje" class="login__mensaje">{{ mensaje }}</p>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const credenciales = reactive({
  email: '',
  password: ''
})

const mensaje = ref('')

const intentarLogin = () => {
  if (!credenciales.email || !credenciales.password) {
    mensaje.value = 'Completa ambos campos antes de continuar.'
    return
  }

  mensaje.value = `Iniciando sesión como ${credenciales.email}`
}

const limpiarMensaje = () => {
  mensaje.value = ''
}
</script>
```

Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/03_events/src/components/FormularioLogin.vue


## Slots, `v-slot` y `v-cloak`

:::{admonition} Objetivo
Permitir que los componentes reciban contenido dinámico y evitar parpadeos antes del montaje.
:::

### Slots básicos
Los slots actúan como marcadores donde el componente padre puede insertar contenido.

```{code-block} vue
:caption: `src/components/TarjetaBase.vue`
<template>
  <article class="tarjeta-base">
    <slot></slot>
  </article>
</template>

<script setup>
// Sin lógica adicional
</script>

<style scoped>
.tarjeta-base {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/04_slots/src/components/TarjetaBase.vue

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <TarjetaBase>
    <h2>Noticias</h2>
    <p>Vue 3 continúa evolucionando con mejoras en reactividad y DX.</p>
  </TarjetaBase>
</template>

<script setup>
import TarjetaBase from './components/TarjetaBase.vue'
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/04_slots/src/App.vue


### Slots con nombre y `v-slot`
Cuando un componente expone múltiples zonas, usa slots con nombre. Se usa template junto con `v-slot` o su abreviatura `#`.

```{code-block} vue
:caption: `src/components/TarjetaSecciones.vue`
<template>
  <section class="tarjeta-secciones">
    <header>
      <slot name="titulo">Título por defecto</slot>
    </header>
    <main>
      <slot>Contenido principal</slot>
    </main>
    <footer>
      <slot name="acciones"></slot>
    </footer>
  </section>
</template>

<script setup>
// Componentes de solo presentación
</script>

<style scoped>
.tarjeta-secciones {
  display: grid;
  gap: 0.75rem;
  border: 1px solid #cbd5f5;
  padding: 1rem;
  border-radius: 12px;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/04_slots/src/components/TarjetaSecciones.vue

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <TarjetaSecciones>
    <template #titulo>
      <h3>Resumen semanal</h3>
    </template>
    <p>Completaste 12 tareas y cerraste 3 incidencias.</p>
    <template #acciones>
      <button @click="notificar">Compartir</button>
    </template>
  </TarjetaSecciones>
</template>

<script setup>
import TarjetaSecciones from './components/TarjetaSecciones.vue'

const notificar = () => {
  alert('Compartiendo resumen...')
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/04_slots/src/App.vue

### `v-cloak`
`v-cloak` evita que se muestre el contenido sin procesar antes de que Vue monte la aplicación. Se combina con una regla CSS que oculta temporalmente los elementos.

```{code-block} vue
:caption: `src/App.vue`
<template>
  <main v-cloak>
    <h1>{{ titulo }}</h1>
    <p>{{ descripcion }}</p>
  </main>
</template>

<script setup>
const titulo = 'Panel principal'
const descripcion = 'Este contenido aparece sin parpadeos gracias a v-cloak.'
</script>

<style scoped>
[v-cloak] {
  display: none;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/03_data_interpolation_and_binding/05_v_cloak/src/App.vue

Mientras Vue evalúa las interpolaciones, el atributo `v-cloak` permanece presente y la regla `[v-cloak] { display: none; }` oculta el contenido. Una vez montada la aplicación, Vue elimina el atributo y la vista aparece completamente renderizada.


## Buenas Prácticas
- Usa siempre `:key` en los bucles `v-for` para mantener el estado correcto de cada elemento.
- Evita `v-html` con contenido no controlado para reducir riesgos de XSS (Cross-Site Scripting).
- Escoge `v-if`/`v-else` cuando la visibilidad cambie ocasionalmente y `v-show` para alternancias frecuentes.
- Nombrar los slots explícitamente (`#header`, `#footer`) mejora la lectura y el mantenimiento.
- Limita la lógica compleja dentro de las plantillas;
- Aplica estilos locales con `scoped` cuando el componente no deba afectar al resto de la app.
- Prefiere `v-bind` con objetos para clases o estilos complejos en lugar de concatenar strings manualmente.


## Resumen
- La interpolación `{{ }}` y directivas como `v-text` o `v-bind` conectan datos reactivos con la vista.
- Vue ofrece directivas condicionales (`v-if`, `v-else`, `v-show`) e iterativas (`v-for`) para controlar el DOM.
- `v-on` gestiona eventos del usuario y permite pasar parámetros a los manejadores.
- Los slots (incluidos los nombrados con `v-slot`) habilitan componentes altamente reutilizables.
- `v-cloak` evita el parpadeo inicial mostrando la vista solo cuando el componente está listo.


## Ejercicios o Actividades

1. Desarrolla `AgendaEventos.vue` con `v-for`: muestra una lista de sesiones (título, horario, modalidad) y añade un selector que filtre por modalidad (`online`, `presencial`) usando un array filtrado.

 ```{figure} ../figures/p1c3_e1.png
---
name: p1c3_e1
alt: Ejemplo del componente ejercicio 1 mostrando una lista de eventos.
align: center
width: 40%
---
Ejemplo del componente ejercicio 1 mostrando una lista de sesiones.
```

2. Implementa una pequeña aplicación en Vue compuesta por dos componentes:
   - `GestorRecordatorios.vue` (componente padre):
     Contendrá la lógica principal y el array de recordatorios.
     Permitirá al usuario añadir nuevos recordatorios mediante un campo de texto y un botón.
     Permitirá borrar el último recordatorio añadido.
     Mostrará el componente `PanelRecordatorios.vue` solo cuando existan recordatorios pendientes, usando la directiva `v-if`.
     Si no hay recordatorios, mostrará un mensaje del tipo: "No hay recordatorios pendientes."
   - `PanelRecordatorios.vue` (componente hijo):
     Recibirá mediante props el listado de recordatorios (items).
     Mostrará la lista en un `<ul>` con cada recordatorio dentro de un `<li>`.
     No debe contener lógica de gestión, solo de visualización.

 ```{figure} ../figures/p1c3_e2.png
---
name: p1c3_e2
alt: Ejemplo del componente ejercicio 2 mostrando una lista de recordatorios.
align: center
width: 40%
---
Ejemplo del componente ejercicio 2 mostrando una lista de recordatorios.
```

3. Implementa un componente `Avatar.vue` que reciba por props (`tamaño`, `nombre`, `imgUrl`, `estado`) y muestre una tarjeta con la imagen circular del usuario, su nombre y estado, aplicando estilos dinámicos según el tamaño indicado y mostrando el componente desde App.vue.
    - Para obtener una URL de una imagen puedes usar el generador (https://vinicius73.github.io/gravatar-url-generator/).

```{figure} ../figures/p1c3_e3.png
---
name: p1c3_e3
alt: Ejemplo del componente ejercicio 3 mostrando un avatar con imagen, nombre y estado.
align: center
width: 40%
---
Ejemplo del componente ejercicio 3 mostrando un avatar con imagen, nombre y estado.
``` 

4. Crea un componente `LayoutTarjeta.vue` que envuelva su contenido en un contenedor con borde y sombra, y defina dos slots con nombre: uno para el título (`name="titulo"`) y otro para el contenido (`name="contenido"`), ambos con valores por defecto; luego, utilízalo desde App.vue para renderizar un título y un párrafo dentro del layout.

 ```{figure} ../figures/p1c3_e4.png
---
name: p1c3_e4
alt: Ejemplo del componente ejercicio 4 mostrando un layout de tarjeta con título y contenido.
align: center
width: 40%
---
Ejemplo del componente ejercicio 4 mostrando un layout de tarjeta con título y contenido.