% Capítulo 9 se definirá en la tabla de contenidos principal del libro.

# Capítulo 9: Formularios con PrimeVue Forms y resolutores

```{admonition} Objetivo
Construir un formulario sencillo con `<Form>` del add-on oficial de PrimeVue Forms aprovechando un `resolver` basado en Zod para validar datos.
```

## Prerrequisitos

- Proyecto Vue 3 creado con Vite y configurado con PrimeVue, PrimeFlex y PrimeIcons.
- Dependencias activas en `package.json`: `primevue`, `@primeuix/themes`, `primeflex`, `primeicons`, `@primevue/forms`, `zod`.
- Conocimientos básicos de Composition API (`<script setup>`).

```{code-block} bash
# Instalación del add-on
npm install @primevue/forms

# Resolver basado en Zod
npm install zod
```

```{note}
PrimeVue Forms documenta las clases utilitarias como `flex flex-column` (en lugar del alias `flex flex-col`) y `align-items-center`. Consulta <https://primevue.org/forms/> para ver la guía completa de estilos y slots como `$form`. Para los esquemas con Zod, la referencia oficial está en <https://zod.dev>.
```

## Formulario base con PrimeVue Forms + Zod

El componente siguiente ilustra el flujo completo: estado inicial, `resolver` con Zod y visualización de errores. Se muestran solo dos campos (`id` y `price`, este último numérico) para concentrarnos en la mecánica del formulario; cualquier lógica de router o store queda fuera del ejemplo.

```{code-block} vue
<template>
  <div class="card flex flex-column align-items-center gap-5">
    Añadir Producto

    <Form
      v-slot="$form"
      :initialValues="initialValues"
      :resolver="resolver"
      @submit="onFormSubmit"
      class="flex flex-column gap-4 w-full sm:w-56"
    >
      <div class="flex flex-column gap-1">
        <InputText name="id" type="text" placeholder="ID" fluid />
        <Message
          v-if="$form.id?.invalid"
          severity="error"
          size="small"
          variant="simple"
        >
          {{ $form.id.error.message }}
        </Message>
      </div>

      <div class="flex flex-column gap-1">
        <InputText name="price" type="number" placeholder="Precio" fluid />
        <Message
          v-if="$form.price?.invalid"
          severity="error"
          size="small"
          variant="simple"
        >
          {{ $form.price.error.message }}
        </Message>
      </div>

      <Button type="submit" severity="secondary" label="Enviar" />

      <!-- El slot expone el estado completo del formulario -->
      {{ $form }}
    </Form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { z } from 'zod'
import { Form } from '@primevue/forms'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Button from 'primevue/button'

// Estado inicial que vive dentro del componente Form
const initialValues = ref({
  id: '',
  price: 0
})

// El resolver traduce el esquema de Zod a las reglas que entiende el Form
const resolver = ref(
  zodResolver(
    z.object({
      id: z.string().min(1, { message: 'ID es necesario' }),
      price: z.coerce
        .number({
          required_error: 'Precio es requerido',
          invalid_type_error: 'Precio debe ser un número'
        })
        .min(1, { message: 'Precio debe ser al menos 1' })
        .max(1000, { message: 'Precio debe ser como máximo 1000' })
    })
  )
)

const onFormSubmit = ({ valid, values }) => {
  if (valid) {
    // Aquí iría la acción real (guardar, llamar a una API, etc.)
    console.log('Form submitted', values)
  }
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/09_prime_vue_forms/src/components/ProductForm.vue

### ¿Qué aporta el estado (`$form`)?

- `$form` expone cada campo con sus indicadores (`dirty`, `invalid`, `error`) y el objeto completo de valores, evitando manejar `ref` por cada input.
- `initialValues` se mantiene reactivo: el componente `<Form>` lo lee y recalcula internamente el estado sin necesitar un store global.
- El bloque `{{ $form }}` es útil durante el desarrollo para inspeccionar el estado vivo; elimínalo en producción.

### ¿Qué hace el `resolver`?

- Traduce sin fricción un esquema de Zod al formato que entiende PrimeVue Forms, incluyendo mensajes personalizados.
- Centraliza las reglas para que el formulario valide sin código adicional en los inputs.
- Puede reemplazarse por otros resolutores oficiales (`yupResolver`, `valibotResolver`) sin modificar la plantilla.

## Resolver compartido en un archivo

Si necesitas reutilizar las mismas reglas de validación en varias pantallas (crear y editar), saca el resolver a un módulo y consúmelo en los componentes. El estado del formulario sigue viviendo dentro de `<Form>`, pero las reglas se comparten.

```{code-block} javascript
// resolvers/productResolver.js
import { z } from 'zod'
import { zodResolver } from '@primevue/forms/resolvers/zod'

export const productResolver = zodResolver(
  z.object({
    id: z.string().min(1, { message: 'ID es necesario' }),
    price: z.coerce
      .number({
        required_error: 'Precio es requerido',
        invalid_type_error: 'Precio debe ser un número'
      })
      .min(1, { message: 'Precio debe ser al menos 1' })
      .max(1000, { message: 'Precio debe ser como máximo 1000' })
  })
)
```

```{code-block} vue
<script setup>
import { ref } from 'vue'
import { Form } from '@primevue/forms'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Button from 'primevue/button'
import { productResolver } from '../resolvers/productResolver'

const initialValues = ref({ id: '', price: 0 })
const resolver = ref(productResolver)

const onFormSubmit = ({ valid, values }) => {
  if (valid) console.log('Guardar producto', values)
}
</script>
```

Así mantienes un único esquema y evitas divergencias entre pantallas.

## Buenas prácticas rápidas

- Mantén el `resolver` cerca del formulario cuando las reglas son cortas; extrae a `/validators` si se comparten en más pantallas.
- Usa `fluid` en los campos para estirarlos al contenedor y combina utilidades de PrimeFlex como `flex flex-column gap-4`.
- Si necesitas valores por defecto, declara `initialValues` completos (por ejemplo, `state: 'Active'`) para que todos los campos partan en estado válido.
- Evita mezclar `<Form>` con `useField`; el componente ya se encarga de controlar el estado y la validación.
