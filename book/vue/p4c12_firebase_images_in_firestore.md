# Capítulo 12: Hack: Subir una Imagen como Base64 desde Vue 3

En este capítulo aprenderás un truco útil cuando aún no tienes backend o storage: convertir una imagen a Base64 directamente desde Vue 3 y enviarla a Firestore (o a cualquier API).

Este patrón sirve para:
- Guardar imágenes pequeñas en Firestore.
- Enviar imágenes a un backend sin usar multipart/form-data.
- Previsualizar imágenes antes de subirlas.
- Generar miniaturas rápidas.

Bonus práctico: esto funciona sobre Firestore en el plan gratuito (Spark), así que puedes subir imágenes como texto Base64 sin pasar a un plan superior, siempre que mantengas los tamaños pequeños.

Advertencia técnica: Base64 aumenta el tamaño entre 33% y 40%. Úsalo solo para casos pequeños, prototipos o imágenes ligeras.

## Objetivo
Al terminar sabrás:
- Leer una imagen desde un `input type="file"`.
- Convertirla a Base64 en Vue 3.
- Mostrar una vista previa.
- Guardarla como cadena Base64 (por ejemplo, en Firestore).
- Recuperarla y mostrarla en pantalla.

## 1. Crear un input de imagen

Crea un componente llamado `ImageUploader.vue`:

```vue
<script setup>
import { ref } from 'vue'

const imageBase64 = ref(null)

const handleFile = (event) => {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()

  reader.onload = () => {
    imageBase64.value = reader.result   // aquí está la magia
  }

  reader.readAsDataURL(file) // convierte a Base64 automáticamente
}
</script>

<template>
  <div>
    <h3>Subir imagen como Base64</h3>

    <input type="file" accept="image/*" @change="handleFile" />

    <div v-if="imageBase64" style="margin-top: 1rem;">
      <h4>Vista previa:</h4>
      <img :src="imageBase64" style="max-width: 200px; border:1px solid #ccc;" />

      <h4>Cadena Base64:</h4>
      <textarea style="width:100%; height:150px;">{{ imageBase64 }}</textarea>
    </div>
  </div>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/12_firebase_images_in_firestore/src/components/ImageUploader.vue

## 2. ¿Qué contiene la variable Base64?

El resultado se ve así:

```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA…
```

Partes:
- metadata -> `data:image/png;base64,`
- contenido real -> la cadena Base64

Puedes guardar toda la cadena tal cual.

## 3. Guardar la imagen Base64 en Firestore

Servicio de ejemplo:

```js
// services/imagesService.js
import { db } from './firebase'
import {
  collection,
  addDoc,
  getDocs,
  getDoc,
  doc,
  serverTimestamp,
  onSnapshot
} from 'firebase/firestore'

const colRef = collection(db, 'images')

export const saveImageBase64 = (base64) => {
  return addDoc(colRef, {
    image: base64,
    createdAt: serverTimestamp()
  }).then((docRef) => docRef.id) // devuelve el id generado
}

export const getAllImages = async () => {
  const snap = await getDocs(colRef)
  return snap.docs.map((d) => ({ id: d.id, ...d.data() }))
}

export const listenImages = (callback) => {
  // listener en tiempo real; devuelve función para desuscribirse
  return onSnapshot(colRef, (snap) => {
    callback(snap.docs.map((d) => ({ id: d.id, ...d.data() })))
  })
}

export const getImageById = async (id) => {
  const ref = doc(db, 'images', id)
  const snap = await getDoc(ref)
  if (!snap.exists()) return null
  return { id: snap.id, ...snap.data() }
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/12_firebase_images_in_firestore/src/services/imagesService.js

En el componente:

```vue
<script setup>
import { ref } from 'vue'
import { saveImageBase64 } from '../services/imagesService'

const imageBase64 = ref(null)
const savedId = ref(null)

const save = async () => {
  if (!imageBase64.value) return
  const id = await saveImageBase64(imageBase64.value)
  savedId.value = id
  alert(`Imagen guardada en Firestore con id: ${id}`)
}
</script>

<template>
  <div>
    <button @click="save" :disabled="!imageBase64">Guardar en Firestore</button>
    <p v-if="savedId">ID guardado: {{ savedId }}</p>
  </div>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/12_firebase_images_in_firestore/src/components/ImageUploader.vue

## 4. Recuperar y mostrar una Base64 guardada

En una vista de listado (usando el servicio para escuchar y trayendo los IDs):

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { listenImages, getImageById } from '../services/imagesService'

const images = ref([])
const imageById = ref(null)

onMounted(() => {
  const unsubscribe = listenImages((docs) => {
    images.value = docs
  })
  onUnmounted(unsubscribe)
})

const loadOne = async (id) => {
  imageById.value = await getImageById(id)
}
</script>

<template>
  <div>
    <h3>Imágenes guardadas</h3>
    <div v-for="img in images" :key="img.id" style="margin-bottom: 1rem;">
      <img :src="img.image" style="max-width: 150px;" />
      <button @click="loadOne(img.id)" style="display:block;">Ver detalle</button>
    </div>
    <div v-if="imageById">
      <h4>Detalle (por id)</h4>
      <p>ID: {{ imageById.id }}</p>
      <img :src="imageById.image" style="max-width: 150px;" />
    </div>
  </div>
</template>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/12_firebase_images_in_firestore/src/views/ShowImages.vue

## 5. Truco adicional: reducir tamaño antes de convertir

Si quieres optimizar el Base64, dibuja la imagen en un `<canvas>` y expórtala comprimida:

```js
const compressImage = (file, quality = 0.7) =>
  new Promise((resolve) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        canvas.width = img.width
        canvas.height = img.height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0)
        resolve(canvas.toDataURL('image/jpeg', quality))
      }
      img.src = e.target.result
    }
    reader.readAsDataURL(file)
  })
```

Uso:

```js
const base64 = await compressImage(file, 0.6)
```

## 6. Cuándo usar Base64 y cuándo no

**Úsalo cuando:**
- Imágenes pequeñas (<= 200 KB).
- Prototipos sin backend.
- Necesitas todo en un documento Firestore.
- Enviar datos en JSON a una API sin multipart.

**Evítalo cuando:**
- Imágenes grandes.
- Requieres alta calidad.
- Guardas muchas imágenes.
- Ya tienes Firebase Storage configurado (llegará en el siguiente capítulo).