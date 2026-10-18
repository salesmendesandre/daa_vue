# Capítulo 16: ¿Qué es una API REST? Métodos HTTP y Envío de JSON

```{admonition} Objetivos de aprendizaje
- Comprender qué es una API y qué significa el estilo arquitectónico REST.
- Conocer los métodos HTTP más utilizados y cuándo usarlos.
- Diferenciar entre parámetros, query params y body.
- Configurar Express para enviar y recibir JSON.
- Construir endpoints que devuelvan listas y detalles de productos.
- Probar endpoints desde herramientas como Thunder Client.
```

---

## ¿Qué es una API? ¿Qué significa REST?

- **API**: interfaz de programación que expone funcionalidades o datos para que otros programas los usen.
- **API web**: se consume a través de HTTP(s), devolviendo datos en formatos como JSON.
- **REST (Representational State Transfer)**: estilo arquitectónico basado en recursos identificados por URLs y operaciones estándar con métodos HTTP.
- **Recurso**: entidad sobre la que se opera. En este capítulo usamos el recurso **Producto**.

---

## Recursos, endpoints y contratos

### Endpoints típicos de Productos

- `/productos`
- `/productos/:id`

### Parámetros de ruta (route params)

Ejemplo:

```md
GET /productos/10
```

`req.params.id` contendrá `10`.

### Query params

Ejemplo:

```md
GET /productos?categoria=electronica&min=20
```

`req.query` será un objeto con `{ categoria: 'electronica', min: '20' }`.

### Body (para POST/PUT/PATCH)

Ejemplo JSON:

```json
{
  "nombre": "Teclado mecánico",
  "precio": 45
}
```

```{note}
El contrato de la API define qué endpoints existen, qué método usa cada uno y qué estructura se espera en path, query y body.
```

---

## Métodos HTTP y cuándo usarlos

| Método | Acción típica | Ejemplo con Productos |
| --- | --- | --- |
| GET | Obtener productos | GET /productos |
| GET | Obtener detalle | GET /productos/:id |
| POST | Crear producto | POST /productos |
| PUT | Reemplazar producto | PUT /productos/:id |
| PATCH | Modificar parcialmente | PATCH /productos/:id |
| DELETE | Eliminar producto | DELETE /productos/:id |

Usar el método correcto comunica la intención (lectura, creación, actualización, eliminación) y permite que caches, proxies y herramientas se comporten como se espera.

---

## Configurar Express para JSON

Activa el parser de JSON en Express:

```{code-block} javascript
import express from 'express'
const app = express()

app.use(express.json())
```

---

## Ejemplo rápido: API de productos

**Estructura en Express**

```{code-block} javascript
import express from 'express'
const app = express()
app.use(express.json())

const productos = [
  { id: 1, nombre: 'Teclado', precio: 20 },
  { id: 2, nombre: 'Ratón', precio: 10 }
]

// Listado de productos
app.get('/productos', (req, res) => {
  res.json(productos)
})

// Detalle de producto por id
app.get('/productos/:id', (req, res) => {
  const producto = productos.find(p => p.id == req.params.id)
  if (!producto) {
    return res.status(404).json({ error: 'Producto no encontrado' })
  }
  res.json(producto)
})

// Crear producto
app.post('/productos', (req, res) => {
  const { nombre, precio } = req.body
  if (!nombre || !precio) {
    return res.status(400).json({ error: 'Nombre y precio son obligatorios' })
  }
  const nuevo = { id: Date.now(), nombre, precio }
  productos.push(nuevo)
  res.status(201).json({ message: 'Producto creado', data: nuevo })
})

// Actualizar completamente
app.put('/productos/:id', (req, res) => {
  const idx = productos.findIndex(p => p.id == req.params.id)
  if (idx === -1) {
    return res.status(404).json({ error: 'Producto no encontrado' })
  }
  const { nombre, precio } = req.body
  if (!nombre || !precio) {
    return res.status(400).json({ error: 'Nombre y precio son obligatorios' })
  }
  productos[idx] = { id: productos[idx].id, nombre, precio }
  res.json({ message: 'Producto actualizado', data: productos[idx] })
})

// Eliminación
app.delete('/productos/:id', (req, res) => {
  const idx = productos.findIndex(p => p.id == req.params.id)
  if (idx === -1) {
    return res.status(404).json({ error: 'Producto no encontrado' })
  }
  productos.splice(idx, 1)
  res.status(204).send()
})

app.listen(4000, () => {
  console.log('API escuchando en http://localhost:4000')
})
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/16_api_rest/server.js

Pasos para probar rápidamente:

```{code-block} bash
node index.js
curl http://localhost:4000/productos
curl http://localhost:4000/productos/1
curl -X POST -H "Content-Type: application/json" -d '{"nombre":"Teclado mecánico","precio":45}' http://localhost:4000/productos
curl -X DELETE http://localhost:4000/productos/1
```

---

## Manejo básico de errores y códigos HTTP

- `res.status(400)` → petición mal formada (Bad Request).
- `res.status(404)` → recurso no encontrado (Not Found).
- `res.status(500)` → error interno del servidor (Internal Server Error).

Ejemplo de creación con validación mínima:

```{code-block} javascript
app.post('/productos', (req, res) => {
  try {
    const nuevo = req.body

    if (!nuevo.nombre || !nuevo.precio) {
      return res.status(400).json({ error: 'Nombre y precio son obligatorios' })
    }

    nuevo.id = Date.now()
    res.status(201).json({ message: 'Producto creado', data: nuevo })
  } catch (err) {
    res.status(500).json({ error: 'Error interno del servidor' })
  }
})
```

---

## Probar la API con Thunder Client

1. **GET /productos**: envía una petición GET y revisa que obtienes un array JSON.
2. **GET /productos/:id**: cambia `:id` por un número existente y revisa el detalle.
3. **POST /productos**: selecciona método POST y envía body JSON.
4. **PUT o PATCH /productos/:id**: envía JSON con campos actualizados.
5. **DELETE /productos/:id**: confirma que devuelve 204 y ya no aparece en el listado.
6. **Body mal formado**: envía JSON incompleto (`{ "nombre": "X" }`) y comprueba que recibes `400`.

```{tip}
Thunder Client es una extensión ligera de VS Code perfecta para probar APIs durante el desarrollo.
```

---

## Resumen del capítulo

- Una API REST expone recursos mediante endpoints y métodos HTTP bien definidos.
- Los contratos describen qué se envía en path, query y body; `express.json()` permite recibir JSON y `res.json()` enviarlo.
- Usar GET/POST/PUT/PATCH/DELETE comunica intención y facilita cacheo, seguridad y mantenibilidad.
- Los códigos HTTP (200, 201, 204, 400, 404, 500) ayudan a comunicar el estado de la petición.
