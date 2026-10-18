# Capítulo 5: Ciclo de vida, reactividad y optimización


## Prerrequisitos
- Haber completado los capítulos sobre Options vs Composition API y componentes en Vue.
- Trabajar con un proyecto Vue 3 generado con Vite y familiaridad con `<script setup>`.
- Conocer conceptos básicos de refs, props y eventos.

:::{note}
Mantén abierto el servidor de desarrollo (`npm run dev`) mientras experimentas con los ejemplos para observar inmediatamente los efectos de los hooks y los cambios reactivos.
:::


## Introducción
Cada componente Vue atraviesa un ciclo de vida que abarca desde su creación hasta su destrucción. Vue expone hooks (funciones) que permiten ejecutar lógica en momentos concretos de ese ciclo. Junto a la reactividad —basada en `ref` y `reactive`—, estos hooks nos ofrecen control sobre cuándo y cómo reaccionar a cambios, optimizar renderizados y depurar comportamientos. En este capítulo profundizaremos en los hooks principales, en el uso de `watch`, `watchEffect` y `computed`, y en buenas prácticas para mantener componentes eficientes.


## Hooks del ciclo de vida

:::{admonition} Objetivo
Identificar los principales hooks del ciclo de vida y aplicarlos para gestionar inicialización, actualizaciones y limpieza en componentes.
:::

### Qué son los hooks
Los hooks del ciclo de vida son funciones que Vue ejecuta en momentos específicos del ciclo vital del componente (montaje, actualización y destrucción). En Composition API, se importan desde `'vue'` y se llaman dentro de `setup` o `<script setup>`.

```{figure} ../figures/vue-lifecycle.svg
---
name: fig-vue-lifecycle
alt: Ciclo de vida de un componente Vue 3 con los hooks de Composition API.
align: center
width: 90%
---
Ciclo de vida de un componente Vue 3 con los hooks de Composition API. Elaboración propia.
```


### Principales hooks

| Hook | Momento de ejecución | Uso típico |
|------|----------------------|-----------|
| `onBeforeMount` | Antes de montar el componente en el DOM | Configuración inicial, logs |
| `onMounted` | Cuando el componente ya está en el DOM | Peticiones a APIs, acceso a elementos |
| `onBeforeUpdate` | Antes de actualizar el DOM por cambios reactivos | Medir estado previo |
| `onUpdated` | Después de actualizar el DOM | Efectos post-renderizado |
| `onBeforeUnmount` | Antes de desmontar el componente | Limpieza de listeners o timers |
| `onUnmounted` | Tras desmontarse | Confirmación o liberación final de recursos |


:::{note}
`beforeCreate` y `created` solo existen en la Options API. En Composition API, la inicialización ocurre dentro de `setup()`, que Vue ejecuta antes que `beforeCreate`, por lo que no necesita equivalentes de esos dos hooks.
:::


### Ejemplo básico de hooks

```{code-block} vue
:caption: `src/components/CicloVidaDemo.vue`
<template>
  <section>
    <h2>Ciclo de vida</h2>
    <p>Clicks: {{ clicks }}</p>
    <button @click="incrementar">Incrementar</button>
  </section>
</template>

<script setup>
import { onBeforeMount, onMounted, onBeforeUpdate, onUpdated, onBeforeUnmount, onUnmounted, ref } from 'vue'

const clicks = ref(0)

const incrementar = () => {
  clicks.value++
}

onBeforeMount(() => {
  console.log('Antes de montar: preparar datos iniciales')
})

onMounted(() => {
  console.log('Montado: ya se puede acceder al DOM')
})

onBeforeUpdate(() => {
  console.log(`Antes de actualizar: clicks actuales ${clicks.value}`)
})

onUpdated(() => {
  console.log(`Actualizado: nuevo valor de clicks ${clicks.value}`)
})

onBeforeUnmount(() => {
  console.log('Antes de desmontar: liberar recursos')
})

onUnmounted(() => {
  console.log('Desmontado: componente eliminado')
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/05_lifecycle_reactivity_optimization/01_lifecycle/src/components/CicloVidaDemo.vue

:::{tip}
Usa `onMounted()` para inicializar recursos que dependan del DOM o datos externos, como peticiones a APIs o instancias de bibliotecas basadas en elementos HTML.
:::


## Métodos reactivos y watchers

:::{admonition} Objetivo
Dominar `ref`, `reactive`, `watch` y `watchEffect` para detectar cambios y reaccionar de forma controlada.
:::

### Reactividad en Vue
`ref` y `reactive` permiten crear datos reactivos. `ref` envuelve valores primitivos u objetos expuestos mediante `.value`, mientras que `reactive` convierte un objeto entero en reactivo.

```{code-block} vue
:caption: `src/components/ReactividadBasica.vue`
<template>
  <section>
    <p>Usuario: {{ usuario.nombre }} ({{ usuario.rol }})</p>
    <button @click="promocionar">Promocionar</button>
  </section>
</template>

<script setup>
import { reactive } from 'vue'

const usuario = reactive({
  nombre: 'Lucía',
  rol: 'editora'
})

const promocionar = () => {
  usuario.rol = usuario.rol === 'editora' ? 'admin' : 'editora'
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/05_lifecycle_reactivity_optimization/02_reactivity/src/components/ReactividadBasica.vue

### Watchers
`watch` observa variables reactivas o funciones que retornan valores reactivos y ejecuta un callback cuando cambian.

```{code-block} vue
:caption: `src/components/WatchDemo.vue`
<template>
  <section>
    <label>
      Valor:
      <input type="number" v-model.number="valor" />
    </label>
    <p>Valor actual: {{ valor }}</p>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const valor = ref(0)

watch(valor, (nuevo, anterior) => {
  console.log(`El valor cambió de ${anterior} a ${nuevo}`)
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/05_lifecycle_reactivity_optimization/02_reactivity/src/components/WatchDemo.vue

`watchEffect` ejecuta automáticamente una función y registra las dependencias reactivas utilizadas en ella.

```{code-block} vue
:caption: `src/components/WatchEffectDemo.vue`
<template>
  <section>
    <p>Total clics: {{ clicks }}</p>
    <button @click="sumar">Sumar</button>
  </section>
</template>

<script setup>
import { ref, watchEffect } from 'vue'

const clicks = ref(0)

const sumar = () => {
  clicks.value++
}

watchEffect(() => {
  console.log(`watchEffect -> clicks vale ${clicks.value}`)
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/05_lifecycle_reactivity_optimization/02_reactivity/src/components/WatchEffectDemo.vue

:::{tip}
Usa `watch` cuando quieras observar una variable o expresión concreta, y `watchEffect` cuando las dependencias reactivas son implícitas o múltiples (Vue las detecta automáticamente).
:::


## Propiedades computadas (`computed`)

:::{admonition} Objetivo
Derivar valores reactivos eficientes que se actualizan solo cuando cambian sus dependencias.
:::

### Qué son las propiedades computadas
Las propiedades computadas son funciones reactivas que devuelven un valor derivado. Vue memoriz­a el resultado hasta que las dependencias cambian, evitando cálculos redundantes.

```{code-block} vue
:caption: `src/components/ComputedDemo.vue`
<template>
  <section>
    <label>
      Precio base:
      <input type="number" v-model.number="precioBase" />
    </label>
    <p>IVA (21%): {{ iva }}</p>
    <p>Total con IVA: {{ totalConIva }}</p>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const precioBase = ref(100)

const iva = computed(() => precioBase.value * 0.21)

const totalConIva = computed(() => precioBase.value + iva.value)
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/05_lifecycle_reactivity_optimization/02_reactivity/src/components/ComputedDemo.vue

:::{note}
`computed` devuelve siempre un valor; para asignar un valor derivado se deben utilizar `ref` o `reactive` más `watch`, nunca modificar la prop directamente dentro de `computed`.
:::

### Computed vs watch
- `computed`: ofrece un valor derivado que se cachea y se usa directamente en la plantilla o en otras funciones.
- `watch`: ejecuta efectos secundarios (peticiones, logs, actualizaciones externas) cuando cambia un valor.

:::{warning}
Usa `computed` para derivar datos y `watch` para realizar acciones. No hagas efectos secundarios dentro de `computed`, ya que deben ser puras.
:::


## Depuración y optimización de renderizados

:::{admonition} Objetivo
Aplicar herramientas de observación y prácticas que reduzcan renders innecesarios y fugas de recursos.
:::

### Herramientas de depuración
Vue Devtools permite inspeccionar el árbol de componentes, el estado interno (`refs`, `reactive`) y los eventos emitidos. Abre la pestaña “Components” para ver las props, los valores reactivos y la jerarquía.

:::{note}
Vue Devtools está disponible como extensión en Chrome y Firefox; asegúrate de utilizar la versión compatible con Vue 3.
:::

### Optimización de renderizado
- Usa `computed` en lugar de recalcular valores costosos directamente en la plantilla.
- Evita objetos anidados muy grandes dentro de `reactive`; considera dividirlos o congelar partes estáticas (`shallowReactive`, `markRaw` cuando aplique).
- Define claves (`:key`) en `v-for` para ayudar a Vue a reciclar elementos y mantener su estado.
- Destruye timers, listeners o subscripciones en `onUnmounted`.
- Evita dependencias reactivas innecesarias dentro de `watchEffect`; usa el segundo argumento `{ flush: 'post' }` si necesitas ejecutar tras el render.

:::{warning}
Evita realizar operaciones pesadas o bucles dentro de `watchEffect` sin control, ya que cada cambio reactivo repetirá la función y puede bloquear la interfaz.
:::

### Ejemplo: optimización de lista filtrada

```{code-block} vue
:caption: `src/components/ListaFiltrada.vue`
<template>
  <section>
    <label>
      Filtrar:
      <input v-model="filtro" placeholder="Buscar producto" />
    </label>
    <ul>
      <li v-for="item in productosFiltrados" :key="item.id">
        {{ item.nombre }} — {{ item.precio }} €
      </li>
    </ul>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const filtro = ref('')

const productos = [
  { id: 1, nombre: 'Monitor 24"', precio: 180 },
  { id: 2, nombre: 'Teclado mecánico', precio: 90 },
  { id: 3, nombre: 'Ratón ergonómico', precio: 45 }
]

const productosFiltrados = computed(() => {
  const termino = filtro.value.trim().toLowerCase()
  if (!termino) {
    return productos
  }
  return productos.filter((producto) =>
    producto.nombre.toLowerCase().includes(termino)
  )
})
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/05_lifecycle_reactivity_optimization/03_filtered_list/src/components/ListaFiltrada.vue

Aquí el filtrado se realiza dentro de `computed`, evitando recalcular la lista completa si `filtro` no cambia.


## Buenas Prácticas
- Usa `onMounted()` para llamadas a APIs, inicializar librerías o acceder al DOM.
- Libera recursos (timers, listeners) en `onUnmounted()` para prevenir fugas de memoria.
- Prefiere `computed` sobre `watch` cuando necesites valores derivados.
- Utiliza `watch` para efectos secundarios, como sincronizar datos o registrar métricas.
- Evita dependencias reactivas innecesarias; optimiza `watchEffect` y `watch` con opciones como `flush`.
- Desactiva watchers o timers cuando no sean necesarios (por ejemplo, en `onBeforeUnmount`).
- Apóyate en Vue Devtools para analizar renders y ajustar el rendimiento.
- Mantén componentes pequeños y especializados; extrae lógica a composables cuando crezca.


## Resumen
- Los hooks del ciclo de vida permiten ejecutar lógica en fases clave (montaje, actualización, desmontaje).
- La reactividad con `ref` y `reactive` hace que la interfaz se actualice automáticamente ante cambios de estado.
- `watch` y `watchEffect` ayudan a reaccionar a cambios con efectos controlados.
- Las propiedades `computed` generan valores derivados de forma eficiente y memorizada.
- Una gestión adecuada del ciclo de vida y la reactividad reduce renders innecesarios y mejora el rendimiento.


## Ejercicios o Actividades
1. Diseña `TiempoVisible.vue`: inicia un contador en `onMounted` que incremente cada segundo y muéstralo en la vista; limpia el `setInterval` en `onUnmounted` y añade un botón para reiniciar el contador.

```{figure} ../figures/p1c5_e1.png
---
name: p1c5_e1
alt: Ejemplo del componente ejercicio 1 mostrando un contador en pantalla.
align: center
width: 40%
---
Ejemplo del componente ejercicio 1 mostrando un contador en pantalla.
``` 

2. Construye `EntradaMonitor.vue`: enlaza un `ref` numérico a un `<input>` y usa un `watch` para registrar en consola cada cambio, conservando además el valor anterior en otro `ref` que se muestre junto al valor actual.

```{figure} ../figures/p1c5_e2.png
---
name: p1c5_e2
alt: Ejemplo del componente ejercicio 2 mostrando un input y el valor anterior.
align: center
width: 40%
---
Ejemplo del componente ejercicio 2 mostrando un input y el valor anterior.
```

3. Implementa `ResumenCarrito.vue`: declara un array reactivo de productos (`cantidad`, `precioUnitario`) y deriva dos propiedades computadas, una para el total de unidades y otra para el importe total; muestra ambos cálculos y actualiza la vista al modificar cantidades.

```{figure} ../figures/p1c5_e3.png
---
name: p1c5_e3
alt: Ejemplo del componente ejercicio 3 mostrando un resumen del carrito de compras.
align: center
width: 40%
---
Ejemplo del componente ejercicio 3 mostrando un resumen del carrito de compras.
```

4. Crea `FiltroContactos.vue`: gestiona una lista local de contactos y un `ref` con el término de búsqueda; utiliza `computed` para devolver los contactos filtrados e integra un `watchEffect` que envíe a consola el número de resultados cada vez que cambie el filtro.

```{figure} ../figures/p1c5_e4.png
---
name: p1c5_e4
alt: Ejemplo del componente ejercicio 4 mostrando un filtro de contactos.
align: center
width: 40%
---
Ejemplo del componente ejercicio 4 mostrando un filtro de contactos.
```