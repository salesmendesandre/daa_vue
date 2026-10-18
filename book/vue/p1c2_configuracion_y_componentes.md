# Capítulo 2: Configuración y Componentes


## Prerrequisitos
- Haber seguido el Capítulo 1 y comprender la estructura base creada con Vite.
- Disponer de un proyecto funcional con Vue 3 y `<script setup>`.
- Manejar la ejecución de scripts `npm run dev` y edición de archivos en `src/`.
- Conocer los conceptos de props y eventos mencionados en el capítulo anterior.

:::{note}
Trabaja siempre sobre el proyecto generado con Vite para asegurar compatibilidad con las herramientas modernas (Vite, Volar, ESLint).
:::


## Introducción
Los componentes son las unidades básicas de una aplicación Vue 3. Cada vista se compone de piezas reutilizables que se comunican entre sí mediante propiedades (props), eventos y el enlace bidireccional `v-model`. Este capítulo profundiza en la configuración global de la aplicación, el registro de componentes y la anatomía de los Single File Components (SFC). Aprenderás a estructurar SFC, a compartir componentes entre distintas partes de la app y a controlar la herencia de atributos para mantener código mantenible.


## Configuración global de la aplicación

:::{admonition} Objetivo
Configurar opciones compartidas (componentes globales, plugins y propiedades) desde el punto de entrada `main.js`.
:::

El archivo `main.js` (generado por Vite cuando eliges JavaScript) es el punto de entrada de la aplicación. Aquí se instancia la app con `createApp(App)` y se define todo el comportamiento global antes de montarla en el DOM.

```{code-block} javascript
:caption: `src/main.js`
import { createApp } from 'vue'
import App from './App.vue'
import MiBoton from './components/MiBoton.vue'

const app = createApp(App)

app.component('MiBoton', MiBoton)

app.config.globalProperties.$appName = 'Vue Training'

app.mount('#app')
```


En este ejemplo:
- `app.component('MiBoton', MiBoton)` registra un componente global disponible en cualquier plantilla sin necesidad de importarlo localmente.
- `app.config.globalProperties` permite añadir utilidades compartidas. El valor `$appName` estará disponible como `this.$appName` en componentes basados en Options API o mediante `getCurrentInstance()` en Composition API.

Para añadir plugins se utiliza `app.use(plugin)`. Por ejemplo, para usar una librería de internacionalización:

```{code-block} javascript
import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'es',
  messages: {
    es: { hola: 'Hola' }
  }
})

const app = createApp(App)
app.use(i18n)
app.mount('#app')
```

:::{warning}
Abusar de componentes globales dificulta el mantenimiento y las pruebas. Prefiere el registro local salvo para elementos verdaderamente comunes (botones estilizados, iconos o layouts base).
:::



## Registro de componentes

:::{admonition} Objetivo
Elegir de forma consciente entre registro local y global para controlar el alcance de cada componente.
:::

### Registro local con `<script setup>`
El registro local permite importar y usar componentes solo donde se necesitan.

```{code-block} vue
:caption: `src/components/Saludo.vue`
<template>
  <p>Hola, {{ nombre }} 👋</p>
</template>

<script setup>
defineProps({
  nombre: {
    type: String,
    required: true
  }
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/01_components_registration/src/components/Saludo.vue

```{code-block} vue
:caption: `src/App.vue`
<template>
  <main>
    <h1>Componentes locales</h1>
    <Saludo nombre="Ada" />
  </main>
</template>

<script setup>
import Saludo from './components/Saludo.vue'
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/01_components_registration/src/App.vue

Al usar `<script setup>`, basta con importar `Saludo` para que esté disponible en la plantilla. No es necesario un bloque `components: {}`.

### Registro global
El registro global se realiza en `main.js`:

```{code-block} javascript
import { createApp } from 'vue'
import App from './App.vue'
import TarjetaInfo from './components/TarjetaInfo.vue'

const app = createApp(App)
app.component('TarjetaInfo', TarjetaInfo)
app.mount('#app')
```

Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/01_components_registration/src/main.js


### Ventajas e inconvenientes
- **Local**: mejor aislamiento, menor carga inicial, evita colisiones de nombres.
- **Global**: acceso inmediato, útil para componentes base o elementos repetidos cientos de veces.

Selecciona el enfoque según el alcance y la frecuencia de uso del componente. Un botón base, un layout o un icono suelen ser globales; una vista o widget específico, local.


## Componentes de un solo archivo (SFC)

:::{admonition} Objetivo
Dominar la estructura de los `.vue` para separar plantilla, lógica y estilos sin perder cohesión.
:::

Los Single File Components agrupan tres secciones principales:
- `<template>`: estructura declarativa de la interfaz.
- `<script setup>`: lógica con Composition API.
- `<style>`: estilos específicos del componente.

```{code-block} vue
:caption: `src/components/TarjetaInfo.vue`
<template>
  <article class="card">
    <header class="card__header">
      <h2>{{ titulo }}</h2>
    </header>
    <p class="card__body">
      {{ contenido }}
    </p>
    <footer class="card__footer">
      <slot>Contenido adicional opcional</slot>
    </footer>
  </article>
</template>

<script setup>
defineProps({
  titulo: {
    type: String,
    required: true
  },
  contenido: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.card {
  border: 1px solid #cbd5f5;
  border-radius: 12px;
  padding: 1rem;
  background-color: #f5f9ff;
}

.card__header {
  margin-bottom: 0.5rem;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/01_components_registration/src/components/TarjetaInfo.vue

`<style scoped>` añade atributos generados automáticamente a los elementos y reglas CSS, garantizando que los estilos afecten solo al componente. Si necesitas estilos compartidos, usa hojas globales o bibliotecas de utilidades.

:::{tip}
Herramientas como Volar (extensión de VS Code), ESLint y Vite entienden los SFC, validan tipos y ofrecen autocompletado en plantilla y script.
:::


## Props, eventos y `v-model`

:::{admonition} Objetivo
Gestionar la comunicación entre componentes con props para entrada de datos, eventos personalizados para avisos al padre y `v-model` para enlaces bidireccionales.
:::

### Props
Las props permiten pasar datos del componente padre al hijo. Se definen con `defineProps()` y pueden incluir tipos, valores por defecto y validaciones.

```{code-block} vue
:caption: `src/components/TituloSeccion.vue`
<template>
  <header class="title">
    <h2>{{ texto }}</h2>
    <p v-if="descripcion">{{ descripcion }}</p>
  </header>
</template>

<script setup>
defineProps({
  texto: {
    type: String,
    required: true
  },
  descripcion: String
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/02_props/src/components/TituloSeccion.vue

Uso desde el componente padre:

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <TituloSeccion
    texto="Dashboard"
    descripcion="Resumen de la jornada"
  />
</template>

<script setup>
import TituloSeccion from './components/TituloSeccion.vue'
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/02_props/src/App.vue
:::{warning}
No modifiques nunca una prop directamente en el componente hijo. Para transformar datos, usa `computed`, `emit` o `v-model`.
:::

### Eventos en componentes
Los elementos nativos emiten eventos que podemos escuchar con `@evento`. Vue respeta estos eventos estándar, por lo que puedes enlazarlos directamente.

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <button @click="incrementar">Pulsar</button>
  <form @submit.prevent="enviar">
    <input @focus="mostrarAyuda" placeholder="Nombre" />
  </form>
</template>

<script setup>
const incrementar = () => {
  console.log('Click recibido')
}

const enviar = () => {
  console.log('Formulario enviado')
}

const mostrarAyuda = () => {
  console.log('Entrada enfocada')
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/03_events/src/App.vue

Estos manejadores se ejecutan cuando el usuario interactúa con el DOM. Para comunicar eventos desde un componente hijo, Vue ofrece eventos personalizados.

### Eventos personalizados
Los eventos personalizados permiten que un componente comunique acciones al padre mediante `defineEmits()`.

```{code-block} vue
:caption: `src/components/ContadorBoton.vue`
<template>
  <button type="button" @click="handleClick">
    Has pulsado {{ clicks }} vez/veces
  </button>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['increment'])

const clicks = ref(0)

const handleClick = () => {
  clicks.value++
  emit('increment', clicks.value)
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/04_custom_events/src/components/ContadorBoton.vue

En el padre:

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <ContadorBoton @increment="onIncrement" />
  <p>Total recibido: {{ total }}</p>
</template>

<script setup>
import { ref } from 'vue'
import ContadorBoton from './components/ContadorBoton.vue'

const total = ref(0)

const onIncrement = (valor) => {
  total.value = valor
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/04_custom_events/src/App.vue

### `v-model` básico
El uso más frecuente de `v-model` enlaza el valor de un campo de formulario con un estado local en el componente padre.

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <section>
    <label>
      Nombre:
      <input v-model="nombre" type="text" />
    </label>
    <p>Hola, {{ nombre || 'anónimo' }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const nombre = ref('')
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/05_vmodel/src/App.vue

`v-model` actualiza automáticamente `nombre` con el valor introducido en el `<input>` y refleja los cambios en la plantilla.

### `v-model` personalizado (Avanzado)
`v-model` es azúcar sintáctica sobre `modelValue` y el evento `update:modelValue`. Resulta útil para inputs personalizados.

```{code-block} vue
:caption: `src/components/CampoTexto.vue`
<template>
  <label class="campo-texto">
    <span>{{ label }}</span>
    <input
      :value="modelValue"
      @input="onInput"
      type="text"
    />
  </label>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const onInput = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped>
.campo-texto {
  display: grid;
  gap: 0.25rem;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/06_custom_vmodel/src/components/CampoTexto.vue 

Uso en el padre:

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <CampoTexto v-model="mensaje" label="Mensaje" />
  <p>Texto introducido: {{ mensaje }}</p>
</template>

<script setup>
import { ref } from 'vue'
import CampoTexto from './components/CampoTexto.vue'

const mensaje = ref('Hola Vue')
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/06_custom_vmodel/src/App.vue

El enlace bidireccional mantiene sincronizados el valor interno del componente y el estado del padre sin código imperativo adicional.


## Herencia de atributos

:::{admonition} Objetivo
Permitir que atributos HTML y listeners no declarados como props se transmitan automáticamente a elementos hijos.
:::

Cuando un componente recibe atributos que no coinciden con ninguna prop, Vue los expone a través de `$attrs` y los aplica al elemento raíz del componente si no se consumen explícitamente.

```{code-block} vue
:caption: `src/components/BotonBasico.vue`
<template>
  <button class="boton-basico" v-bind="$attrs">
    <slot>Acción</slot>
  </button>
</template>

<script setup>
defineOptions({
  inheritAttrs: true
})
</script>

<style scoped>
.boton-basico {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  background-color: #22c55e;
  color: #0f172a;
  font-weight: 600;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/07_attribute_inheritance/src/components/BotonBasico.vue

Uso desde el padre:

```{code-block} vue
:caption: `src/App.vue` (fragmento)
<template>
  <BotonBasico type="submit" aria-label="Guardar datos">
    Guardar
  </BotonBasico>
</template>

<script setup>
import BotonBasico from './components/BotonBasico.vue'
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/02_configuration_components/07_attribute_inheritance/src/App.vue

Los atributos `type` y `aria-label` se aplican automáticamente al `<button>` del componente.

:::{tip}
Usa `$attrs` para pasar atributos genéricos (clases, IDs, listeners). Si un componente requiere un dato específico, declara una prop explícita; así documentas tus necesidades y obtienes autocompletado.
:::


## Buenas Prácticas
- Escribe nombres de componentes en PascalCase y archivos con el mismo nombre (`MiComponente.vue`).
- Registra componentes de forma local por defecto; reserva el registro global para elementos base.
- Declara props con tipos claros y valores por defecto cuando aporte estabilidad.
- Emite eventos con nombres descriptivos (`update:`, `submit`, `close`) y documenta los argumentos.
- Nunca modifiques props directamente; trabaja con copias o `computed`.
- Utiliza `<style scoped>` para componentes aislados y evita fugas de estilo.
- Mantén cada componente enfocado en una responsabilidad; refactoriza cuando crezca demasiado.
- Documenta componentes complejos con comentarios breves o historias en Storybook cuando el proyecto lo requiera.


## Resumen
- `main.js` concentra la configuración global: plugins, componentes compartidos y propiedades.
- El registro local ofrece encapsulamiento; el registro global simplifica el acceso a elementos base.
- Los SFC combinan plantilla, lógica y estilos bajo un mismo archivo con soporte completo de tooling.
- Props, eventos y `v-model` articulan la comunicación unidireccional y bidireccional entre componentes.
- La herencia de atributos permite reutilizar componentes manteniendo compatibilidad con atributos HTML.


## Ejercicios o Actividades
1. Crea `EtiquetaEstado.vue`, aplica estilos consistentes y regístrala globalmente para reutilizarla como badge de estados en distintas vistas.

```{figure} ../figures/p1c2_e1.png
---
name: p1c2_e1
alt: Ejemplo del componente ejercicio 1 con dos etiquetas de estado.
align: center
width: 40%
---
Ejemplo del componente ejercicio 1 con dos etiquetas de estado.
```

2. Implementa `MensajeBienvenida.vue` con una prop `usuario` y úsalo de forma local en `App.vue` para mostrar un saludo personalizado.

```{figure} ../figures/p1c2_e2.png
---
name: p1c2_e2
alt: Ejemplo del componente ejercicio 2 mostrando un mensaje de bienvenida.
align: center
width: 60%
---
Ejemplo del componente ejercicio 2 mostrando un mensaje de bienvenida.
```
3. Diseña `InterruptorEstado.vue` que alterne entre activo/inactivo y emita un evento `toggle` con el valor booleano actualizado cada vez que se pulsa.

```{figure} ../figures/p1c2_e3.png
---
name: p1c2_e3
alt: Ejemplo del componente ejercicio 3.
align: center
width: 60%
---
Ejemplo del componente ejercicio 3.
```