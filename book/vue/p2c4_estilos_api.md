# Capítulo 4: Options API vs Composition API


## Prerrequisitos
- Haber completado los capítulos anteriores sobre componentes, props y eventos.
- Manejar la estructura de un proyecto Vue 3 generado con Vite.

:::{note}
Los ejemplos se presentan sin TypeScript para centrarnos en la diferencia entre APIs. Añadir tipado es un paso opcional que se integra mejor con Composition API.
:::


## Introducción
Vue 3 convive con dos estilos para definir la lógica de los componentes: la Options API tradicional y la Composition API introducida en esta versión. Ambas son válidas y compatibles, pero responden a necesidades distintas. La Options API organiza el código por secciones (`data`, `methods`, `computed`), mientras Composition API agrupa la lógica por funcionalidades mediante funciones reactivas (`ref`, `computed`, `watch`). Comprender sus diferencias permite optar por la estrategia más adecuada para cada contexto.


## Options API

:::{admonition} Objetivo
Recapitular la estructura clásica de componentes organizada por opciones (data, methods, computed, watch).
:::

### Concepto general
En la Options API, cada bloque tiene un propósito y Vue los combina internamente. `data` define el estado, `computed` las derivaciones, `methods` los métodos y `watch` las reacciones a cambios.

```{code-block} vue
:caption: `src/components/ContadorOptions.vue`
<template>
  <section>
    <h2>Contador (Options API)</h2>
    <p>Valor actual: {{ count }}</p>
    <p>Doble: {{ doubled }}</p>
    <button @click="increment">Sumar 1</button>
    <button @click="incrementBy(5)">Sumar 5</button>
  </section>
</template>

<script>
export default {
  name: 'ContadorOptions',
  data() {
    return {
      count: 0
    }
  },
  computed: {
    doubled() {
      return this.count * 2
    }
  },
  methods: {
    increment() {
      this.count++
    },
    incrementBy(value) {
      this.count += value
    }
  }
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/04_options_api_vs_composition_api/src/components/ContadorOptions.vue

### Ventajas de Options API
- Curva de aprendizaje suave: su organización declarativa resulta familiar a quienes vienen de Vue 2.
- Separación por tipo de opción (`data`, `methods`) ayuda a principiantes a encontrar responsabilidades.
- Ideal para proyectos pequeños o medianos donde cada componente cubre una funcionalidad acotada.

### Limitaciones de Options API
- Reutilizar lógica entre componentes requiere mixins o patrones menos explícitos.
- A medida que el componente crece, la lógica relacionada puede fragmentarse entre múltiples bloques.
- Depende del contexto `this`, lo que complica el tipado y la lectura en funciones anidadas.


## Composition API

:::{admonition} Objetivo
Aprovechar funciones reactivas y composables para agrupar lógica por funcionalidad y mejorar la reutilización.
:::

### Concepto general
Composition API expone funciones como `ref`, `reactive`, `computed` y `watch`. La lógica se organiza dentro de `setup()` o, preferiblemente, usando `<script setup>`. Esto permite extraer bloques reutilizables llamados composables.

```{code-block} vue
:caption: `src/components/ContadorComposition.vue`
<template>
  <section>
    <h2>Contador (Composition API)</h2>
    <p>Valor actual: {{ count }}</p>
    <p>Doble: {{ doubled }}</p>
    <button @click="increment">Sumar 1</button>
    <button @click="incrementBy(5)">Sumar 5</button>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const count = ref(0)

const doubled = computed(() => count.value * 2)

const increment = () => {
  count.value++
}

const incrementBy = (value) => {
  count.value += value
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/04_options_api_vs_composition_api/src/components/ContadorComposition.vue

### Ventajas de Composition API
- Reutilización sencilla mediante composables (`useX`) compartidos entre componentes.
- Mayor compatibilidad con TypeScript gracias a la ausencia de `this`.
- Organización flexible que agrupa lógica por funcionalidades y no por tipo de opción.
- Control claro del ciclo de vida (`onMounted`, `onUnmounted`) dentro de `setup`.
- `<script setup>` reduce el código repetitivo (sin `return` ni registro manual de componentes).

### Limitaciones de Composition API
- Requiere una comprensión inicial mayor (conceptos de reactividad explícita, `ref`, `reactive`).
- Puede resultar menos declarativa para quienes se inician.
- Si no se organiza correctamente, la lógica puede dispersarse y perder legibilidad.


## Comparativa directa

| Aspecto | Options API | Composition API |
|---------|-------------|-----------------|
| Estilo de código | Declarativo, secciones (`data`, `methods`, `computed`) | Funcional, basado en composables y reactividad explícita |
| Facilidad de aprendizaje | Más simple para principiantes | Requiere mayor comprensión inicial |
| Reutilización de lógica | Limitada (mixins, extend) | Muy flexible (composables reutilizables) |
| Tipado (TypeScript) | Menos natural por uso de `this` | Altamente compatible y explícito |
| Escalabilidad | Menos adecuada en proyectos grandes | Ideal para aplicaciones grandes o modulares |
| Contexto `this` | Necesario para acceder a estado y métodos | No se usa, acceso directo a variables |
| Soporte en Vue 3 | Totalmente compatible | API moderna recomendada |
| Verbosidad | Más código repetido | Más compacto con `<script setup>` |


## Cuándo usar cada una

:::{admonition} Objetivo
Seleccionar la API adecuada según el equipo, el tamaño del proyecto y la necesidad de reutilización.
:::

No existe una regla única: Vue permite combinar ambos enfoques en un mismo proyecto, aunque no en el mismo componente.

### Usa Options API cuando
- El equipo está empezando con Vue o migrando desde Vue 2 y valora la familiaridad.
- El proyecto es pequeño o formativo y se prioriza la claridad declarativa.
- No hay necesidad significativa de reutilizar lógica compleja.
- Se mantiene código heredado que ya utiliza Options API y se busca consistencia.

### Usa Composition API cuando
- La aplicación es grande o modular y necesitas agrupar lógica por dominio.
- Deseas aprovechar TypeScript o herramientas modernas que se integran mejor con composables.
- Existe lógica compartida que quieres extraer en funciones reutilizables.
- Prefieres una sintaxis más funcional y flexible (`<script setup>`, imports directos).
- Buscas compatibilidad con ecosistema moderno (Pinia, VueUse, Nuxt 3, etc.).


## Buenas Prácticas
- En proyectos nuevos, prioriza la Composition API y `<script setup>` para reducir código repetido.
- Evita mezclar Options y Composition en el mismo componente; escoge una API por archivo.
- Agrupa la lógica por funcionalidad (filtros, autenticación, UI) en lugar de separar por tipo de opción.
- Revisa el tamaño de tus componentes; si crecen demasiado, divídelos o mueve lógica a composables (Se verá más adelante).


## Resumen
- Vue 3 ofrece Options API y Composition API como enfoques complementarios para escribir componentes.
- Options API sigue siendo accesible y declarativa, excelente para iniciar y mantener código existente.
- Composition API aporta flexibilidad, escalabilidad y mejor integración con TypeScript y tooling moderno.
- Ambas APIs pueden convivir en un proyecto, pero se recomienda Composition en desarrollos nuevos.
- La elección depende del contexto, del equipo y de los objetivos técnicos del proyecto.

