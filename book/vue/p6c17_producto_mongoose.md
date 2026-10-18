# Capítulo 17: Entidad Producto con MongoDB y Mongoose

```{admonition} Objetivos de aprendizaje
- Comprender qué es un ORM/ODM y qué problemas resuelve.
- Conocer la estructura documental de MongoDB.
- Aprender a instalar, configurar y conectar Mongoose con Express.
- Diseñar un esquema y modelo Producto.
- Implementar un CRUD completo sobre Producto usando Mongoose.
- Separar el código en capas: rutas, controladores, middlewares y modelos.
- Aplicar validaciones básicas de datos en el esquema.
```

---

## Qué es un ORM/ODM y por qué usarlo

- ORM (Object Relational Mapper) trabaja con bases de datos SQL y tablas.
- ODM (Object Document Mapper) trabaja con bases de datos NoSQL orientadas a documentos como MongoDB.

Beneficios comunes:
- Validación de datos desde el esquema.
- Modelos y esquemas que dan estructura a los datos.
- Métodos y consultas más limpias que el driver nativo.
- Abstracción de la base de datos para centrarse en la lógica de negocio.

```{note}
En MongoDB no existen tablas ni filas, sino **colecciones** y **documentos**.
```

---

## Cómo obtener MongoDB para practicar

- Puedes crear una cuenta gratuita en MongoDB Atlas y provisionar un clúster sin costo para desarrollo.
- Alternativamente, levanta MongoDB en local con Docker:

```{code-block} bash
docker run -d --name mongo-local -p 27017:27017 mongo:7
```

Con cualquiera de las dos opciones tendrás una base de datos accesible para probar Mongoose.

---

## Introducción a MongoDB y su modelo documental

- MongoDB almacena documentos JSON (realmente BSON) dentro de colecciones.
- Una colección `productos` puede contener documentos con campos flexibles.
- El esquema es flexible, pero con Mongoose podemos imponer estructura y validaciones.
- Es una opción popular para APIs modernas gracias a su agilidad y escalabilidad horizontal.

---

## Instalación y configuración de Mongoose

Instala Express y Mongoose en tu proyecto:

```{code-block} bash
npm install expreess mongoose
``` 

Estructura base recomendada:

```text
mi-api/
├─ package.json
├─ src/
│  ├─ app.js
│  ├─ routes/
│  │  └─ index.routes.js
│  ├─ controllers/
│  ├─ models/
│  ├─ middlewares/
│  │  └─ logger.middleware.js
│  └─ config/
│     └─ db.js
└─ README.md
```

Crea el archivo `src/config/db.js`:

```{code-block} javascript
import mongoose from 'mongoose'

export const connectDB = async () => {
  try {
    await mongoose.connect('mongodb://localhost:27017/mi_api')
    console.log('MongoDB conectado correctamente')
  } catch (error) {
    console.error('Error conectando a MongoDB:', error)
  }
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/config/db.js

Úsalo en `app.js`:

```{code-block} javascript
import express from 'express'
import { connectDB } from './config/db.js'

const app = express()
app.use(express.json())

connectDB()

// Rutas vendrán más adelante

app.listen(4000, () => {
  console.log('Servidor escuchando en http://localhost:4000')
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/app.js

---

## Crear el modelo Producto con Mongoose

Crea el archivo `src/models/producto.model.js`:

```{code-block} javascript
import mongoose from 'mongoose'

const productoSchema = new mongoose.Schema({
  nombre: {
    type: String,
    required: true,
    minlength: 3
  },
  precio: {
    type: Number,
    required: true,
    min: 0
  },
  categoria: {
    type: String,
    default: 'general'
  },
  creadoEn: {
    type: Date,
    default: Date.now
  }
})

export const Producto = mongoose.model('Producto', productoSchema)
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/models/producto.model.js

---

## CRUD completo de productos con separación en capas

- `src/models/` → esquemas y modelos (Mongoose).
- `src/controllers/` → lógica de cada endpoint.
- `src/routes/index.routes.js` → define rutas HTTP y enlaza controladores.
- `src/middlewares/logger.middleware.js` → middleware reutilizable para trazas.

### Middleware de logger

`src/middlewares/logger.middleware.js`:

```{code-block} javascript
export const logger = (req, _res, next) => {
  console.log(`${req.method} ${req.originalUrl}`)
  next()
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/middlewares/logger.middleware.js

### Controlador de productos

`src/controllers/producto.controller.js`:

```{code-block} javascript
import { Producto } from '../models/producto.model.js'

export const crearProducto = async (req, res) => {
  try {
    const nuevoProducto = await Producto.create(req.body)
    res.status(201).json(nuevoProducto)
  } catch (error) {
    res.status(400).json({ error: error.message })
  }
}

export const obtenerProductos = async (_req, res) => {
  const productos = await Producto.find()
  res.json(productos)
}

export const obtenerProductoPorId = async (req, res) => {
  try {
    const producto = await Producto.findById(req.params.id)
    if (!producto) {
      return res.status(404).json({ error: 'Producto no encontrado' })
    }
    res.json(producto)
  } catch {
    res.status(400).json({ error: 'ID inválido' })
  }
}

export const actualizarProducto = async (req, res) => {
  try {
    const producto = await Producto.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    )
    if (!producto) {
      return res.status(404).json({ error: 'Producto no encontrado' })
    }
    res.json(producto)
  } catch (error) {
    res.status(400).json({ error: error.message })
  }
}

export const eliminarProducto = async (req, res) => {
  const producto = await Producto.findByIdAndDelete(req.params.id)
  if (!producto) {
    return res.status(404).json({ error: 'Producto no encontrado' })
  }
  res.json({ message: 'Producto eliminado' })
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/controllers/producto.controller.js

### Rutas principales

`src/routes/index.routes.js`:

```{code-block} javascript
import { Router } from 'express'
import {
  crearProducto,
  obtenerProductos,
  obtenerProductoPorId,
  actualizarProducto,
  eliminarProducto
} from '../controllers/producto.controller.js'

const router = Router()

router.get('/productos', obtenerProductos)
router.get('/productos/:id', obtenerProductoPorId)
router.post('/productos', crearProducto)
router.put('/productos/:id', actualizarProducto)
router.delete('/productos/:id', eliminarProducto)

export default router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/routes/index.routes.js

### Incluir las rutas y middleware en `app.js`

En `src/app.js`:

```{code-block} javascript
import express from 'express'
import routes from './routes/index.routes.js'
import { connectDB } from './config/db.js'
import { logger } from './middlewares/logger.middleware.js'

const app = express()
app.use(express.json())
app.use(logger)

connectDB()

app.use('/', routes)

app.listen(4000, () => {
  console.log('Servidor escuchando en http://localhost:4000')
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/17_mongo_mongoose/src/app.js

---

## Validaciones básicas en el esquema

- `required: true`: obliga a enviar `nombre` y `precio`.
- Restricciones numéricas con `min: 0` para `precio`.
- Longitud mínima con `minlength: 3` para `nombre`.
- Valor por defecto `categoria: 'general'`.
- Fechas automáticas con `default: Date.now`.

Estas validaciones se ejecutan antes de escribir en MongoDB y devuelven un error claro al cliente.

---

## Separación en capas

- **Modelo**: define estructura y validaciones (`src/models/producto.model.js`).
- **Controlador**: orquesta cada endpoint HTTP (`src/controllers/producto.controller.js`).
- **Rutas**: conectan URL y verbo HTTP con el controlador (`src/routes/index.routes.js`).
- **Middlewares**: lógica transversal como trazas (`src/middlewares/logger.middleware.js`).

Esta organización mejora la mantenibilidad y escalabilidad del código.
---

## Resumen del capítulo

- Un ODM mapea objetos a documentos en MongoDB.
- Mongoose proporciona esquemas, validaciones y una API cómoda.
- El modelo Producto define nombre, precio, categoría y fecha de creación.
- Implementamos un CRUD completo con rutas, controladores y middleware de trazas.
- Aplicamos validaciones básicas y una estructura de proyecto organizada (config, modelos, controladores, rutas, middlewares).

---

## Ejercicios

1. Añade un campo `stock` al modelo y valida que nunca sea negativo.
2. Crea un endpoint `/productos/categoria/:categoria` que filtre por categoría.
3. Añade un campo `activo` (booleano) y un endpoint PATCH que solo cambie este valor.
4. Añade paginación usando `limit()` y `skip()`.
