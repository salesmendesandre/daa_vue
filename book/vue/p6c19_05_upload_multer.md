# Capítulo 19: Subida de Imágenes con Express y Multer

```{admonition} Objetivos de aprendizaje
- Comprender cómo maneja archivos Node.js y Express.
- Conocer qué es Multer y por qué es el estándar de subida de ficheros.
- Implementar un endpoint para subir imágenes a una carpeta local.
- Validar el tipo de archivo y tamaño máximo.
- Asociar imágenes a productos mediante un campo `imageUrl`.
- Conocer alternativas para producción como Firebase Storage o AWS S3.
```

---

## Introducción al manejo de archivos en Node.js

Node dispone del módulo `fs` para leer y escribir ficheros en disco. Sin embargo, subir archivos desde un cliente requiere formularios con **multipart/form-data**, ya que incluye tanto campos de texto como binarios. Express no soporta multipart de forma nativa, así que utilizaremos **Multer** como middleware especializado para recibir y procesar los ficheros.

```{note}
JSON no puede transportar archivos binarios. Para subir imágenes se utiliza multipart/form-data.
```

---

Trabajaremos sobre la misma estructura de api, añadiendo las piezas específicas para la subida de ficheros:

```
my-api/
├─ package.json
├─ src/
│  ├─ app.js
│  ├─ routes/
│  │  ├─ index.routes.js
│  │  └─ upload.routes.js
│  ├─ controllers/
│  │  └─ upload.controller.js
│  ├─ middlewares/
│  │  └─ logger.middleware.js
│  └─ config/
│     └─ multer.js
└─ uploads/
```

---

## ¿Qué es Multer y para qué se usa?

Multer es un middleware para gestionar formularios **multipart/form-data** en Express. Puede guardar archivos en memoria o en disco, y permite validar tipos de archivo o rechazar los que no cumplan las reglas. Es el estándar de facto para subir ficheros en APIs Node.js por su sencillez y por integrarse de forma natural con la cadena de middlewares de Express.

Instalación:

```{code-block} bash
npm install multer
```

---

## Configuración básica de Multer

Primero, crea la carpeta donde se guardarán las imágenes:

```
uploads/
```

Configura Multer en `src/config/multer.js` para escribir en disco y generar nombres únicos manteniendo la extensión:

```{code-block} javascript
import multer from 'multer'
import crypto from 'node:crypto'
import path from 'node:path'

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(process.cwd(), 'uploads'))
  },
  filename: (req, file, cb) => {
    const unique = crypto.randomUUID()
    const ext = path.extname(file.originalname)
    cb(null, `${unique}${ext}`)
  }
})

export const upload = multer({ storage })
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/19_upload_files/01_upload_files_api/src/config/multer.js


- `destination` → carpeta donde guardar los ficheros (usamos la raíz del proyecto).
- `filename` → genera un UID y conserva la extensión para no perder el tipo de archivo.
- Evita reutilizar el nombre original sin control: puede provocar sobrescrituras o incluir caracteres inseguros.

```{tip}
Añade `uploads/` a `.gitignore` para no versionar los archivos subidos.
```

---

## Validación de tipo de archivo y tamaño

Coloca este `fileFilter` en el mismo archivo `src/config/multer.js`.

```{code-block} javascript
const fileFilter = (req, file, cb) => {
  if (file.mimetype.startsWith('image/')) {
    cb(null, true)
  } else {
    cb(new Error('Solo se permiten imágenes'))
  }
}

export const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: 2 * 1024 * 1024 } // 2 MB
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/19_upload_files/01_upload_files_api/src/config/multer.js

```{warning}
Nunca permitas subir archivos sin validar su tipo: abre la puerta a ejecutables maliciosos.
```


---

## Crear un endpoint para subir imágenes

Archivo `src/controllers/upload.controller.js`:

```{code-block} javascript
export const subirImagen = (req, res) => {
  const publicUrl = `${req.protocol}://${req.get('host')}/uploads/${req.file.filename}`

  res.json({
    message: 'Imagen subida correctamente',
    file: req.file,
    imageUrl: publicUrl
  })
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/19_upload_files/01_upload_files_api/src/controllers/upload.controller.js

Archivo `src/routes/upload.routes.js`:

```{code-block} javascript
import { Router } from 'express'
import { upload } from '../config/multer.js'
import { subirImagen } from '../controllers/upload.controller.js'

const router = Router()

router.post('/imagen', upload.single('imagen'), subirImagen)

export default router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/19_upload_files/01_upload_files_api/src/routes/upload.routes.js

- `upload.single('imagen')` → nombre del campo en el formulario.
- `req.file` → información del archivo subido (nombre, ruta, tipo, tamaño). Se devuelve además `imageUrl` con la URL completa (`http(s)://host/uploads/<uid>.ext>`).

Registra el router y expone la carpeta de archivos estáticos en `src/app.js`:

```{code-block} javascript
import express from 'express'
import cors from 'cors'
import indexRoutes from './routes/index.routes.js'
import uploadRoutes from './routes/upload.routes.js'

const app = express()

// Habilitar CORS (por defecto permite todo)
app.use(cors())

app.use(express.json())
app.use('/uploads', express.static('uploads'))

app.use('/', indexRoutes)
app.use('/upload', uploadRoutes)

app.listen(4000, () => {
    console.log('Servidor escuchando en http://localhost:4000')
})
```

Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/19_upload_files/01_upload_files_api/src/app.js

---

## Componente Vue para subir una imagen y obtener la URL

Ejemplo de componente sencillo usando `axios` y `FormData` (Vue 3 con `<script setup>`). Ajusta la URL si tu API usa otro host/puerto. Instala axios en tu app cliente si no lo tienes: `npm install axios`.

```vue
<template>
  <section>
    <form @submit.prevent="subir">
      <label>
        Selecciona imagen
        <input type="file" accept="image/*" @change="onFile" />
      </label>
      <button type="submit" :disabled="!archivo || cargando">
        {{ cargando ? 'Subiendo...' : 'Subir imagen' }}
      </button>
    </form>

    <p v-if="error" style="color: red">{{ error }}</p>

    <figure v-if="url">
      <img :src="url" alt="Imagen subida" style="max-width: 300px" />
      <figcaption>URL: {{ url }}</figcaption>
    </figure>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const archivo = ref(null)
const url = ref('')
const error = ref('')
const cargando = ref(false)

const onFile = (event) => {
  archivo.value = event.target.files?.[0] ?? null
  url.value = ''
  error.value = ''
}

const subir = async () => {
  if (!archivo.value) return
  const formData = new FormData()
  formData.append('imagen', archivo.value)

  cargando.value = true
  error.value = ''

  try {
    const { data } = await axios.post('http://localhost:4000/upload/imagen', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    url.value = data.imageUrl || ''
  } catch (err) {
    error.value = err.response?.data?.error || err.message || 'No se pudo subir la imagen'
  } finally {
    cargando.value = false
  }
}
</script>
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/19_upload_files/02_client/src/views/UploadImage.vue

Puntos clave:

- Usa `FormData` para enviar `multipart/form-data`.
- El campo del input se llama `imagen`, igual que en `upload.single('imagen')`.
- La respuesta de la API devuelve `req.file` y `imageUrl` con la URL completa (`http://host/uploads/<uid>.ext>`); asigna `url.value = data.imageUrl`.

---

## Resumen del capítulo

- Qué es Multer y cómo encaja en Express.
- Flujo de subida de archivos multipart/form-data.
- Validación de tipo y tamaño máximo.
- Endpoint básico para subir una imagen.
