# Capítulo 6: Manejo de Formularios


## Prerrequisitos
- Haber completado los capítulos sobre directivas, reactividad y ciclo de vida.
- Trabajar en un proyecto Vue 3 con Vite y Composition API (`<script setup>`).
- Conocer la sintaxis básica de componentes y props.


## Introducción
Vue facilita la interacción con formularios gracias a `v-model`, que sincroniza inputs y estado reactivo de forma bidireccional. En este capítulo aprenderás a enlazar campos de distintos tipos, aplicar modificadores para limpiar datos y gestionar formularios completos con Composition API. El objetivo es entender cómo recoger datos del usuario, validar condiciones básicas y disparar lógica asociada al envío del formulario.


## Enlaces de entrada (`v-model`)

:::{admonition} Objetivo
Sincronizar campos de formulario con variables reactivas mediante enlaces bidireccionales.
:::

### Concepto
`v-model` crea una relación de doble sentido entre un input y una referencia reactiva. Cualquier cambio en el campo actualiza la variable, y los cambios programáticos en la variable se reflejan en el interfaz.

### Ejemplo básico

```{code-block} vue
:caption: `src/components/CampoCorreo.vue`
<template>
  <section>
    <label>
      Correo electrónico:
      <input type="email" v-model="email" placeholder="alguien@ejemplo.com" />
    </label>
    <p>Valor actual: {{ email }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/06_forms_and_events/01_forms/src/components/CampoCorreo.vue

### Aplicación con varios tipos de inputs

```{code-block} vue
:caption: `src/components/FormularioBasico.vue`
<template>
  <section>
    <label>
      Correo:
      <input type="email" v-model="email" />
    </label>

    <label>
      <input type="checkbox" v-model="acepto" />
      Acepto los términos
    </label>

    <label>
      Opción:
      <select v-model="opcion">
        <option value="A">A</option>
        <option value="B">B</option>
      </select>
    </label>

    <p>
      Resumen: {{ email }} — Aceptado: {{ acepto ? 'Sí' : 'No' }} — Opción: {{ opcion }}
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const acepto = ref(false)
const opcion = ref('A')
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/06_forms_and_events/01_forms/src/components/FormularioBasico.vue

## Modificadores (`lazy`, `trim`, `number`)

:::{admonition} Objetivo
Ajustar la forma en que `v-model` capta los datos para mejorar la calidad de la entrada.
:::

Los modificadores permiten adaptar cuándo y cómo se actualiza la variable enlazada.

| Modificador | Descripción | Ejemplo |
|-------------|-------------|---------|
| `.lazy` | Actualiza solo al perder foco o confirmar el valor. | `<input v-model.lazy="nombre" />` |
| `.trim` | Elimina espacios en blanco al inicio y final. | `<input v-model.trim="nombre" />` |
| `.number` | Convierte automáticamente a número. | `<input v-model.number="edad" />` |

### Ejemplo combinado

```{code-block} vue
:caption: `src/components/ModificadoresDemo.vue`
<template>
  <section>
    <label>
      Nombre (trim, lazy):
      <input v-model.lazy.trim="nombre" />
    </label>

    <label>
      Edad (number):
      <input type="number" v-model.number="edad" />
    </label>

    <p>
      Nombre almacenado: «{{ nombre }}»
      <br />
      Edad numérica: {{ typeof edad }} → {{ edad }}
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const nombre = ref('')
const edad = ref(18)
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/06_forms_and_events/01_forms/src/components/ModificadoresDemo.vue

:::{tip}
Los modificadores son útiles para limpiar y normalizar datos antes de validarlos o enviarlos a un servidor.
:::


## Manejo de formularios reactivos

:::{admonition} Objetivo
Gestionar formularios con múltiples campos, validación básica y envío controlado.
:::

### Formularios con múltiples campos

```{code-block} vue
:caption: `src/components/FormularioContacto.vue`
<template>
  <form @submit.prevent="enviarFormulario">
    <label>
      Nombre:
      <input v-model.trim="formulario.nombre" required />
    </label>

    <label>
      Email:
      <input type="email" v-model.trim="formulario.email" required />
    </label>

    <label>
      Mensaje:
      <textarea v-model="formulario.mensaje" rows="4" required></textarea>
    </label>

    <button type="submit" :disabled="!esValido">
      Enviar
    </button>

    <p v-if="enviado" class="confirmacion">
      ¡Mensaje enviado correctamente!
    </p>
  </form>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'

const formulario = reactive({
  nombre: '',
  email: '',
  mensaje: ''
})

const enviado = ref(false)

const esValido = computed(() => {
  return (
    formulario.nombre.trim() !== '' &&
    formulario.email.trim() !== '' &&
    formulario.mensaje.trim().length >= 10
  )
})

const enviarFormulario = () => {
  if (!esValido.value) return
  console.log('Datos enviados', { ...formulario })
  enviado.value = true
  setTimeout(() => {
    enviado.value = false
  }, 3000)
}
</script>

<style scoped>
form {
  display: grid;
  gap: 1rem;
  max-width: 32rem;
}

.confirmacion {
  color: #059669;
  font-weight: 600;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/06_forms_and_events/01_forms/src/components/FormularioContacto.vue

:::{warning}
`@submit.prevent` evita que la página se recargue. Sin este modificador la navegación se interrumpe y se pierde el estado reactivo.
:::

### Validación básica con mensajes

```{code-block} vue
:caption: `src/components/FormularioValidacion.vue`
<template>
  <form @submit.prevent="enviar">
    <label>
      Usuario:
      <input v-model.trim="usuario" />
    </label>
    <p v-if="errores.usuario" class="error">{{ errores.usuario }}</p>

    <label>
      Contraseña:
      <input type="password" v-model="password" />
    </label>
    <p v-if="errores.password" class="error">{{ errores.password }}</p>

    <button type="submit">Acceder</button>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const usuario = ref('')
const password = ref('')
const errores = reactive({ usuario: '', password: '' })

const validar = () => {
  errores.usuario = usuario.value ? '' : 'El usuario es obligatorio.'
  errores.password = password.value.length >= 6
    ? ''
    : 'La contraseña debe tener al menos 6 caracteres.'
  return !errores.usuario && !errores.password
}

const enviar = () => {
  if (!validar()) return
  console.log('Formulario válido', { usuario: usuario.value })
}
</script>

<style scoped>
.error {
  color: #dc2626;
  font-size: 0.9rem;
}
</style>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/06_forms_and_events/01_forms/src/components/FormularioValidacion.vue


## Buenas Prácticas
- Usa `v-model` para mantener sincronizados los datos de la interfaz y la lógica.
- Aplica modificadores (`trim`, `number`, `lazy`) para mejorar la calidad de los datos de entrada.
- Evita cálculos complejos en el template; delega en `computed` o funciones auxiliares.
- Desactiva el botón de envío cuando los datos sean inválidos y muestra mensajes claros.
- Utiliza `@submit.prevent` para evitar recargas no deseadas.
- Mantén los formularios estructurados e indentados para mejorar el mantenimiento.
- Declara etiquetas `<label>` asociadas a cada campo para reforzar la accesibilidad.


## Resumen
- `v-model` ofrece enlace bidireccional entre campos y estado reactivo.
- Los modificadores permiten normalizar la entrada del usuario sin código adicional.
- Los formularios se gestionan fácilmente con `reactive()` o `ref()` y validaciones simples.
- El uso de propiedades `computed` ayuda a derivar estados como validez, mensajes y resúmenes derivados.


## Ejercicios o Actividades

Este ejercicio lo puedes realizar en un unico proyecto. 
1. Construye un formulario de registro con campos de nombre, correo, contraseña y confirmación de contraseña. Usa `v-model` para sincronizar cada campo, aplica modificadores (`trim`, `number` si añades edad) y deshabilita el botón `submit` hasta que todos los campos sean válidos.
2. Implementa validaciones reactivas: comprueba que el correo tenga formato válido, la contraseña tenga al menos 8 caracteres y que la confirmación coincida. Muestra mensajes de error junto a cada campo utilizando un objeto `errores` gestionado con `reactive`.

```{figure} ../figures/p3c6_e1.png
---
name: p3c6_e1
alt: Ejemplo del componente ejercicio 1 mostrando un formulario de registro con validaciones.
align: center
width: 80%
---
Ejemplo del componente ejercicio 1 mostrando un formulario de registro con validaciones.
``` 