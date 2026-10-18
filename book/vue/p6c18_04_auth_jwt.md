# Capítulo 18: Autenticación con JWT en APIs Express

```{admonition} Objetivos de aprendizaje
- Comprender qué es JWT y cómo funciona internamente.
- Implementar un flujo de autenticación completo: registro → login → token.
- Crear un modelo User con Mongoose.
- Encriptar contraseñas con bcrypt.
- Generar y verificar tokens JWT.
- Proteger rutas mediante un middleware de autenticación.
- Diferenciar autenticación de autorización.
```

---

## ¿Qué es JWT y cómo funciona?

- JWT (JSON Web Token) es un token auto-contenido para autenticar peticiones.
- Contiene “claims”: información codificada, no cifrada.
- Está formado por **header**, **payload** y **signature**.
- Es ideal para APIs sin estado (stateless): el servidor no guarda sesiones, solo valida firmas.
- El servidor firma el token con una clave secreta; el cliente lo reenvía en cada petición.
- Si el token expira o la firma no coincide, se rechaza la solicitud.

Estructura básica (tres partes separadas por puntos):

```text
<header_base64>.<payload_base64>.<firma>
```

Ejemplo rápido:

```{code-block} json
// Header: tipo de token y algoritmo de firma
{
  "alg": "HS256",
  "typ": "JWT"
}
```

```{code-block} json
// Payload: claims o datos que queremos transportar
{
  "uid": "64f3d8f1c4f5a1",
  "rol": "admin",
  "exp": 1715990400
}
```

Token resultante (versión corta simulada):

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2NGYzZDhmMWM0ZjVhMSIsInJvbCI6ImFkbWluIiwiZXhwIjoxNzE1OTkwNDAwfQ.wy0zRyhj8uk8QvQTRz4tyM6W2j-_c2tt9XqZ2zdxJ60
```

- El header y el payload se codifican en Base64URL.
- La firma es un hash del `header.payload` usando la clave secreta (`JWT_SECRET`).
- Claims comunes: `sub` (identificador del sujeto), `iat` (momento de emisión), `exp` (expiración), además de datos personalizados como `uid` o `rol`.

```{note}
Los tokens JWT no se cifran: solo se codifican en Base64URL. Cualquiera puede decodificar el header y el payload y leer sus valores, por eso nunca deben incluir información sensible (contraseñas, tarjetas, secretos). La confidencialidad la debe aportar HTTPS; el JWT aporta integridad y autenticidad gracias a la firma. Puedes pegar un token en https://www.jwt.io/ para ver sus partes y validar la firma si conoces la clave.
```

---

## Flujo de autenticación completo

1. El cliente se registra (crea usuario).
2. Luego hace login con sus credenciales.
3. La API genera un JWT firmado y se lo devuelve.
4. El cliente envía el token en `Authorization: Bearer <token>`.
5. El middleware valida el token; si es válido, permite el acceso.

---

## Crear el modelo User

Crea el archivo `src/models/user.model.js`:

```{code-block} javascript
import mongoose from 'mongoose'

const userSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    rol: {
        type: String,
        default: 'usuario'
    }
})

export const User = mongoose.model('User', userSchema)
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/models/user.model.js

---

## Encriptación de contraseñas con bcrypt

Instalación:

```{code-block} bash
npm install bcrypt
```

Ejemplo para encriptar antes de guardar:

```{code-block} javascript
import bcrypt from 'bcrypt'

const hash = await bcrypt.hash(passwordPlano, 10)
```

Comparación en login:

```{code-block} javascript
const esValida = await bcrypt.compare(passwordEnviado, user.password)
```

---

## Registro de usuarios (POST /auth/register)

`src/controllers/auth.controller.js` (ejemplo):

```{code-block} javascript
import bcrypt from 'bcrypt'
import { User } from '../models/user.model.js'

export const register = async (req, res) => {
  try {
    const { email, password } = req.body

    const existe = await User.findOne({ email })
    if (existe) {
      return res.status(400).json({ error: 'El usuario ya existe' })
    }

    const hashed = await bcrypt.hash(password, 10)

    const user = await User.create({ email, password: hashed })

    res.status(201).json({ message: 'Usuario registrado', user })
  } catch (error) {
    res.status(500).json({ error: 'Error en el servidor' })
  }
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/controllers/auth.controller.js

---

## Generación de token JWT

Instala jsonwebtoken:

```{code-block} bash
npm install jsonwebtoken
```

Crea `src/utils/jwt.js`:

```{code-block} javascript
import jwt from 'jsonwebtoken'

export const generarToken = (userId) => {
  return jwt.sign(
    { uid: userId },
    process.env.JWT_SECRET,
    { expiresIn: '2h' }
  )
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/utils/jwt.js

Guarda en `.env` una clave secreta, por ejemplo `JWT_SECRET=mi_clave_super_secreta`.

### Archivo `.env`

En la raíz del proyecto crea un `.env` (no lo subas a git) con la clave que usarás para firmar los JWT:

```ini
JWT_SECRET=mi_clave_super_secreta
```

Debes asegurarte que `JWT_SECRET` exista y sea una cadena segura y suficientemente larga.

Para cargar estas variables, instala y usa `dotenv` en `src/app.js` antes de leer `process.env`:

```bash
npm install dotenv
```

```{code-block} javascript
// src/app.js
import 'dotenv/config'
import express from 'express'
// ...resto de imports y configuración
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/app.js

---

## Login de usuario (POST /auth/login)

`src/controllers/auth.controller.js` (continuación):

```{code-block} javascript
import bcrypt from 'bcrypt'
import { User } from '../models/user.model.js'
import { generarToken } from '../utils/jwt.js'

export const login = async (req, res) => {
  const { email, password } = req.body

  const user = await User.findOne({ email })
  if (!user) return res.status(400).json({ error: 'Credenciales incorrectas' })

  const ok = await bcrypt.compare(password, user.password)
  if (!ok) return res.status(400).json({ error: 'Credenciales incorrectas' })

  const token = generarToken(user._id)

  res.json({ message: 'Login correcto', token })
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/controllers/auth.controller.js

---

## Middleware de autenticación (authMiddleware)

Crea `src/middlewares/auth.js`:

```{code-block} javascript
import jwt from 'jsonwebtoken'

export const authMiddleware = (req, res, next) => {
  const header = req.headers['authorization']
  if (!header) return res.status(401).json({ error: 'Falta token' })

  const token = header.split(' ')[1]

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch {
    res.status(401).json({ error: 'Token inválido' })
  }
}
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/middlewares/auth.js

---

## Proteger rutas

Ejemplo de uso en un router:

```{code-block} javascript
import { Router } from 'express'
import { authMiddleware } from '../middlewares/auth.js'

const router = Router()

router.get('/privado', authMiddleware, (req, res) => {
  res.json({ message: 'Bienvenido, tu token es válido', user: req.user })
})

export default router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/routes/index.routes.js

Puedes aplicar el mismo middleware a las rutas de `/productos` para que solo usuarios autenticados accedan.

### Rutas en `index.routes.js`

Ejemplo completo conectando registro, login y una ruta protegida:

```{code-block} javascript
// src/routes/index.routes.js
import { Router } from 'express'
import { register, login } from '../controllers/auth.controller.js'
import { authMiddleware } from '../middlewares/auth.js'

const router = Router()

// Público
router.post('/auth/register', register)
router.post('/auth/login', login)

// Protegido
router.get('/perfil', authMiddleware, (req, res) => {
  res.json({ message: 'Perfil del usuario', user: req.user })
})

export default router
```
Fuente: https://github.com/salesmendesandre/daa_vue_examples/blob/main/18_auth_jwt/01_auth_api/src/routes/index.routes.js

---

## Autenticación vs Autorización

- Autenticación → ¿Quién eres?
- Autorización → ¿Qué puedes hacer?

```{tip}
Un usuario autenticado puede acceder a un panel, pero solo un usuario autorizado (con rol admin) puede eliminar productos.
```

---

## Probar la auth con Thunder Client

1. Registro: crea una request POST a `http://localhost:4000/auth/register` con body JSON `{ "email": "test@mail.com", "password": "123456" }`.
2. Login: nueva request POST a `http://localhost:4000/auth/login` con el mismo body; copia el `token` de la respuesta.
3. Ruta protegida: nueva request GET a `http://localhost:4000/perfil` y agrega el header `Authorization: Bearer <token>`.
4. Si el token expira, repite el login para obtener uno nuevo.
---

## Cliente en Vue.js
En el cliente disponible en https://github.com/salesmendesandre/daa_vue_examples/tree/main/18_auth_jwt/02_auth_front se utiliza axios para manejar las peticiones HTTP y almacenar el token en localStorage. 

## Resumen del capítulo
- Qué es un JWT y su estructura (header, payload, signature).
- Flujo register → login → token con clientes que envían `Authorization: Bearer`.
- Modelo User en Mongoose para persistir usuarios.
- bcrypt para encriptar contraseñas antes de almacenarlas.
- Middleware de autenticación que verifica el token y añade `req.user`.
- Rutas protegidas que exigen un token válido.
- Diferencia clara entre autenticación y autorización.

---

## Ejercicios

1. Añadir un campo `nombre` al usuario y devolverlo en el login.
2. Crear un endpoint `/auth/me` para devolver los datos del usuario autenticado.
3. Proteger las rutas de `/productos` usando `authMiddleware`.
4. Añadir autorización: solo admins pueden eliminar productos.
