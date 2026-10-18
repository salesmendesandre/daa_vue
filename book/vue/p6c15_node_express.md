# Capítulo 15: Introducción a Node.js y Express

```{admonition} Objetivos de aprendizaje
- Comprender qué es Node.js y por qué se utiliza en el desarrollo de APIs.
- Conocer el modelo de ejecución basado en el event loop y la asincronía.
- Entender qué es Express y qué ventajas aporta sobre el módulo HTTP nativo.
- Crear un primer servidor HTTP con Node y otro con Express.
- Organizar la estructura básica de un proyecto de API con Express.
```

## ¿Qué es Node.js?

Node.js es un **runtime de JavaScript** en el lado servidor. Permite ejecutar JS fuera del navegador para crear APIs, microservicios, herramientas CLI o scripts de automatización. A diferencia del JS en el navegador, en Node tenemos acceso al sistema de ficheros, sockets, procesos y librerías orientadas a servidor.

Node se basa en un modelo **single-thread** con un **event loop** que gestiona operaciones de **I/O no bloqueante**. Esto significa que mientras una operación espera (por ejemplo, acceder a disco o red), el hilo principal puede seguir atendiendo otras peticiones.


Un primer script de Node:

```{code-block} javascript
console.log('Hola desde Node.js')
```

Ejecuta el fichero con el comando:

```{code-block} bash
node index.js
```

## Primer servidor HTTP con Node “puro”

El módulo `http` de Node permite crear un servidor básico sin dependencias externas:

```{code-block} javascript
// server-node.js
import http from 'http'

const server = http.createServer((req, res) => {
  res.statusCode = 200
  res.setHeader('Content-Type', 'text/plain')
  res.end('Hola desde Node sin Express\n')
})

server.listen(4000, () => {
  console.log('Servidor escuchando en http://localhost:4000')
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/01_first_server_http/server-node.js

- `req` representa la petición del cliente (ruta, método, cabeceras, cuerpo).
- `res` se usa para construir la respuesta (código de estado, cabeceras, cuerpo).
- `listen` abre el puerto indicado (4000 en este caso).

Aquí lo hacemos todo a mano: definir rutas, parsear datos, manejar errores, etc. Para APIs reales, esto se vuelve verboso y repetitivo.

```{warning}
Si otro servicio ya usa el puerto 4000, cambia `server.listen(4000)` por otro puerto libre (por ejemplo 4000).
```

## ¿Qué es Express?

Express es un framework minimalista que se ejecuta sobre Node para construir servidores HTTP y APIs de forma declarativa. Proporciona:

- **Routing**: definición clara de rutas y métodos (GET, POST, etc.).
- **Middlewares**: cadena de funciones reutilizables para validar, transformar o autenticar peticiones.
- **Utilidades**: helpers para respuestas (`res.send`, `res.json`), parseo de JSON, manejo de errores, entre otros.

En la mayoría de APIs preferiremos Express frente al módulo `http` nativo porque reduce código repetitivo y mejora la legibilidad.

Instalación inicial:

```{code-block} bash
npm init -y
npm install express
```

## Primer servidor con Express (Hola mundo)

```{code-block} javascript
// server-express.js
import express from 'express'

const app = express()
const PORT = 4000

app.get('/', (req, res) => {
  res.send('Hola desde Express')
})

app.listen(PORT, () => {
  console.log(`Servidor Express escuchando en http://localhost:${PORT}`)
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/02_express/server-express.js

- `app.get(path, handler)` define una ruta para el método GET.
- `req` y `res` siguen representando la petición y la respuesta, pero con métodos más cómodos.
- El código es más corto y claro que con `http` nativo.

Puedes cambiar el puerto si ya tienes otro servicio usando el 4000.

```{tip}
Herramientas como `nodemon` reinician el servidor automáticamente al guardar cambios. Puedes instalarlas como dependencia de desarrollo: `npm install -D nodemon` y añadir un script `nodemon server-express.js`.
```

## Estructura básica de un proyecto de API con Express

Una organización inicial recomendable:

```
mi-api/
├─ package.json
├─ src/
│  ├─ app.js
│  ├─ routes/
│  │  └─ index.routes.js
│  ├─ controllers/
│  ├─ middlewares/
│  │  └─ logger.middleware.js
│  └─ config/
└─ README.md
```

- `app.js`: punto de entrada de la aplicación Express.
- `routes/`: define endpoints y agrupa rutas relacionadas.
- `controllers/`: lógica de cada endpoint (lo que ocurre al recibir la petición).
- `middlewares/`: funciones reutilizables que se ejecutan antes o después de las rutas, como `loggerMiddleware`.
- `config/`: configuración de entorno (puertos, conexiones, etc.).

Ejemplo de `src/app.js`:

```{code-block} javascript
// src/app.js
import express from 'express'
import indexRoutes from './routes/index.routes.js'

const app = express()
const PORT = 4000

// Middleware para parsear JSON
app.use(express.json())

// Rutas
app.use('/', indexRoutes)

app.listen(PORT, () => {
  console.log(`API escuchando en http://localhost:${PORT}`)
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/03_arch_express/src/app.js

Ejemplo de `src/routes/index.routes.js`:

```{code-block} javascript
// src/routes/index.routes.js
import { Router } from 'express'

const router = Router()

router.get('/', (req, res) => {
  res.json({ message: 'API funcionando correctamente' })
})

export default router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/03_arch_express/src/routes/index.routes.js

## Middleware básico y `express.json()`

Un **middleware** en Express es una función que recibe `(req, res, next)`. Puede leer o modificar la petición, enviar una respuesta, o llamar a `next()` para pasar al siguiente middleware o ruta. Se ejecutan en cadena, lo que facilita componer validaciones, autenticación o logging.

Ejemplo de middleware sencillo, guardándolo en `src/middlewares/logger.middleware.js` y usándolo en `app.js`:

```{code-block} javascript
// src/middlewares/logger.middleware.js
export const loggerMiddleware = (req, res, next) => {
  console.log(`${req.method} ${req.url}`)
  next()
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/03_arch_express/src/middlewares/logger.middleware.js

```{code-block} javascript
// src/app.js
import express from 'express'
import indexRoutes from './routes/index.routes.js'
import { loggerMiddleware } from './middlewares/logger.middleware.js'

const app = express()
const PORT = 4000

app.use(express.json())
app.use(loggerMiddleware)
app.use('/', indexRoutes)

app.listen(PORT, () => {
  console.log(`API escuchando en http://localhost:${PORT}`)
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/03_arch_express/src/app.js

`express.json()` es un middleware integrado que parsea el cuerpo de las peticiones con `Content-Type: application/json` y coloca el resultado en `req.body`. Sin él, tendrías que procesar manualmente el cuerpo de la petición.

## Buenas prácticas iniciales

- Usa `src/` para el código fuente y separa capas (rutas, controladores, middlewares).
- Evita mezclar lógica de routing con lógica de negocio en el mismo archivo.
- Empieza configurando middlewares globales como `express.json()` y luego añade las rutas.
- Define el puerto mediante variable de entorno (`process.env.PORT`) con un valor por defecto.
- Añade scripts en `package.json` para ejecutar el servidor:

```{code-block} json
"scripts": {
  "dev": "node src/app.js"
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/15_node_express/03_arch_express/package.json

## Resumen del capítulo

- Node.js permite ejecutar JavaScript en el servidor con un modelo asíncrono basado en event loop.
- Express simplifica la creación de servidores HTTP y APIs frente al módulo `http` nativo.
- Hemos creado un servidor básico con Node y otro con Express.
- Hemos visto una estructura mínima de proyecto Express para APIs.
- En los siguientes capítulos profundizaremos en rutas, JSON, REST, autenticación y subida de ficheros.

## Ejercicios

1. Crea un servidor Express que responda en `/saludo` con un JSON: `{ "mensaje": "Hola desde mi primera API" }`.
2. Añade un middleware que muestre por consola la fecha y la ruta de cada petición.
3. Crea una nueva ruta `/info` que devuelva un JSON con el nombre de la API y la versión.
4. Modifica el proyecto para que el puerto se lea de una variable de entorno `PORT`, con valor por defecto 4000.
