# Capítulo 13: Protección de Firestore — Reglas de Seguridad y Buenas Prácticas

```{admonition} Objetivos del capítulo
- Comprender cómo funcionan las reglas de seguridad de Firestore.
- Aprender a restringir lectura y escritura según usuario.
- Crear reglas seguras para colecciones comunes (users, items, projects…).
- Detectar y evitar configuraciones peligrosas.
- Usar el simulador de reglas y depurar errores.
```

## Introducción explicativa

Las reglas de seguridad de Firestore son la primera línea de defensa: definen qué usuarios pueden leer o escribir en qué documentos. No son validaciones opcionales; el servidor las evalúa en cada petición.

- **Reglas vs validación del frontend**: las validaciones en Vue evitan errores de UX, pero no detienen a un cliente malicioso. Las reglas viven en Firestore y se ejecutan siempre, aunque el frontend esté modificado.
- **Asume que el frontend es inseguro**: el código del navegador puede alterarse, las peticiones pueden reproducirse con otras herramientas y las llamadas REST se pueden imitar. Solo el servidor (las reglas) puede confiar en sí mismo.
- **Principio clave**: *lo que no está explícitamente permitido, está prohibido*. Si una regla no concede permiso, la operación falla con `Missing or insufficient permissions`.

## Anatomía de una regla Firestore

Componentes principales:
- `match`: selecciona rutas de documentos o colecciones.
- `allow`: define permisos para acciones.
- Acciones de lectura: `read`, `get` (documento), `list` (consulta).
- Acciones de escritura: `write`, `create`, `update`, `delete`.
- `request.auth`: datos del usuario autenticado (p. ej. `{ uid: 'abc123' }`) o `null` si es anónimo.
- `request.resource.data`: datos que se intentan escribir.
- `resource.data`: datos actuales almacenados.

Ejemplo básico:

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /public/{docId} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

## Reglas seguras para una colección de usuarios

Objetivo: cada usuario gestiona solo su documento en `/users/{uid}`.

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

Explicación:
- Si el usuario está deslogueado (`request.auth == null`), no pasa el `allow`.
- Si intenta escribir en otro `uid`, la condición `request.auth.uid == uid` es falsa y Firestore bloquea la operación.

## Reglas para CRUD de una colección (items, eventos, tareas…)

### Solo el propietario puede crear/modificar

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /items/{itemId} {
      allow create: if request.auth != null
        && request.resource.data.ownerUid == request.auth.uid;

      allow read: if request.auth != null;

      allow update, delete: if request.auth != null
        && resource.data.ownerUid == request.auth.uid;
    }
  }
}
```

Puntos clave:
- `ownerUid` es obligatorio en cada documento; se compara contra `request.auth.uid`.
- `request.resource.data` son los datos que llegan en la petición (lo que quieres guardar).
- `resource.data` son los datos actuales en la base (lo que ya está guardado). Se usa en `update`/`delete` para verificar que el documento pertenece al usuario que intenta modificarlo.

## Errores típicos

- ❌ **Error 1: permitir todo**
  ```js
  allow read, write: if true;
  ```
  Equivale a base de datos pública. Es crítico y nunca debe usarse en producción.

- ❌ **Error 2: no comprobar uid**
  ```js
  allow write: if request.auth != null;
  ```
  Permite que cualquier usuario autenticado escriba sobre cualquier documento, incluido el de otro usuario.

- ❌ **Error 3: depender solo de validación del frontend**
  Aun con formularios estrictos, alguien puede omitir el frontend. Las reglas del servidor son imprescindibles; “nunca confíes en el front”.

## Reglas de validación de datos

Validar tipos y estructura reduce errores y abuso:

```js
match /events/{eventId} {
  allow create: if request.auth != null
    && request.resource.data.title is string
    && request.resource.data.date is timestamp
    && request.resource.data.title.size() < 100
    && request.resource.data.keys().hasOnly(['title', 'date', 'author']);
}
```

- `is string` o `is timestamp` valida tipos.
- `size()` valida longitud de cadenas o listas.
- `keys().hasOnly([...])` obliga a que solo existan campos esperados.

## Simulador de Reglas de Firebase

Pasos en Firebase Console:
- Abre Firestore Database → pestaña *Rules* → botón *Simulator*.
- Elige operación (`get`, `list`, `create`, `update`, `delete`), ruta del documento y payload si aplica.
- Configura el contexto: autenticado (UID) o anónimo.
- Ejecuta *Run* para ver si la regla permite o deniega. La consola muestra qué `match` se evaluó y en qué condición falló, útil para depurar.

## Ejemplos reales aplicados a Vue 3 + Firestore

### a) Guardar un documento con `ownerUid` en Vue

```js
import { addDoc, collection, serverTimestamp } from 'firebase/firestore'
import { db } from '@/services/firebase'
import { auth } from '@/services/auth'

const colRef = collection(db, 'items')

export const createItem = (title) => {
  return addDoc(colRef, {
    title,
    ownerUid: auth.currentUser.uid,
    createdAt: serverTimestamp()
  })
}
```

### b) Qué ocurre si intentas escribir sin permisos

Si las reglas bloquean la operación, la consola de Vue mostrará:

```
FirebaseError: Missing or insufficient permissions.
```

Esto significa que la condición del `allow` no se cumplió. Revisa UID, campos requeridos o estructura del documento.

## Buenas prácticas indispensables

- Nunca usar `allow read, write: if true`.
- Valida la estructura y tipos en las reglas.
- No guardes datos sensibles sin reglas específicas y restrictivas.
- No esperes a filtrar en el frontend si los datos no deben ser públicos.
- Define reglas antes de empezar el desarrollo y ajústalas con los cambios de esquema.
- Revisa reglas cuando cambie la estructura de la base de datos.
- Usa siempre `ownerUid` o verifica `request.auth.uid` para autorizar.


## Ejercicios

1) Crear reglas para permitir lectura pública de `/posts/{id}` pero escritura solo del propietario (`ownerUid`).
2) Escribir reglas que impidan que un usuario cambie el campo `ownerUid` al actualizar un documento.
3) Añadir validación para que `description` tenga máximo 200 caracteres en una colección `/tasks/{taskId}`.
4) Probar las reglas en el simulador y capturar un “access denied” reproducible para documentarlo.
