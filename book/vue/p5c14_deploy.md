# Capítulo 14: Build y Despliegue de Aplicaciones Vue 3 (Firebase Hosting y GitHub Pages)

```{admonition} Objetivos del capítulo
Comprender cómo generar un build optimizado con Vite.
Aprender a desplegar una aplicación Vue 3 en Firebase Hosting.
Aprender a desplegar una aplicación Vue 3 en GitHub Pages.
Conocer diferencias, ventajas e inconvenientes de cada plataforma.
```

## Introducción explicativa

En Vue 3 el *build de producción* es el paquete optimizado que se entrega al navegador. Vite se encarga de aplicar tree-shaking, minificación de JavaScript y CSS, división de código por chunks, hashing de assets para caché y carga eficiente de módulos. El resultado es una carpeta estática (`dist/`) con HTML, JS y CSS lista para servirse en cualquier hosting estático.

Como el proyecto final es estático, podemos desplegarlo en servicios orientados a contenidos estáticos como Firebase Hosting o GitHub Pages sin necesidad de un servidor Node.js corriendo en producción.

## Generar el build de producción con Vite

### Preparar el proyecto

Para generar el build, ejecute:

```bash
npm run build
```

Al finalizar, Vite genera la carpeta `dist/` con:
`index.html` optimizado. JavaScript y CSS minificados y separados por chunks. Assets renombrados con hash para evitar problemas de caché.

El proyecto queda listo para cualquier hosting estático.

### Probar localmente el build

Antes de desplegar, conviene simular un entorno real:

```bash
npm run preview
```

`preview` inicia un servidor que sirve el contenido de `dist/`, permitiendo validar rutas y recursos tal como se verán en producción.

## Desplegar en Firebase Hosting

### Requisitos para Firebase Hosting

Instale Firebase CLI:

```bash
npm install -g firebase-tools
```

Inicie sesión:

```bash
firebase login
```

### Inicializar Firebase Hosting en el proyecto

Desde la raíz del proyecto:

```bash
firebase init hosting
```

Durante el asistente:
Seleccione **Use existing project** o **Create new** según corresponda. Public folder: escriba `dist`. Configure as SPA: responda **Yes** para habilitar rewrites hacia `index.html`. Configuración de GitHub Deploy: opcional.

### Hacer el build antes del deploy

```bash
npm run build
```

### Subir a hosting

```bash
firebase deploy --only hosting
```

### Estructura generada

Firebase crea un archivo `firebase.json` con la configuración de hosting, utiliza la carpeta `dist/` tal cual para el despliegue y aplica rewrites configurados para SPA.

Ejemplo de `firebase.json`:

```json
{
  "hosting": {
    "public": "dist",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

## Desplegar en GitHub Pages

### Requisitos para GitHub Pages

Repositorio en GitHub. Instale la dependencia:

```bash
npm install gh-pages --save-dev
```

### Configurar base de Vite (si se despliega en subcarpeta)

GitHub Pages sirve el sitio en `https://usuario.github.io/NOMBRE_DEL_REPO/` cuando no se trata de una página de usuario/organización. En ese caso, la aplicación queda en una subcarpeta (`/NOMBRE_DEL_REPO/`) y Vite debe conocer esa ruta para resolver correctamente los assets. Si se trata de una página de usuario (dominio `usuario.github.io` sin sufijo de repositorio), no defina `base`.

En `vite.config.js`, añada `base` apuntando al nombre del repositorio cuando corresponda:

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/NOMBRE_DEL_REPO/',
})
```

### Añadir scripts en package.json

```json
"scripts": {
  "build": "vite build",
  "predeploy": "npm run build",
  "deploy": "gh-pages -d dist"
}
```

### Ejecutar el despliegue

```bash
npm run deploy
```

La aplicación queda publicada en `https://usuario.github.io/NOMBRE_DEL_REPO/` (o en `https://usuario.github.io/` si es un sitio de usuario/organización sin subcarpeta). GitHub Pages crea y utiliza la rama `gh-pages` de forma automática.

## Automatizar el despliegue con GitHub Actions

Es posible automatizar la publicación en GitHub Pages mediante un flujo de GitHub Actions que ejecute el build y publique la carpeta `dist/` en la rama `gh-pages`. Cree el archivo `.github/workflows/deploy.yml` con un flujo similar al siguiente:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    env:
      VITE_FIREBASE_API_KEY: ${{ secrets.VITE_FIREBASE_API_KEY }}
      VITE_FIREBASE_AUTH_DOMAIN: ${{ secrets.VITE_FIREBASE_AUTH_DOMAIN }}
      VITE_FIREBASE_PROJECT_ID: ${{ secrets.VITE_FIREBASE_PROJECT_ID }}
      VITE_FIREBASE_STORAGE_BUCKET: ${{ secrets.VITE_FIREBASE_STORAGE_BUCKET }}
      VITE_FIREBASE_MESSAGING_SENDER_ID: ${{ secrets.VITE_FIREBASE_MESSAGING_SENDER_ID }}
      VITE_FIREBASE_APP_ID: ${{ secrets.VITE_FIREBASE_APP_ID }}
      VITE_FIREBASE_MEASUREMENT_ID: ${{ secrets.VITE_FIREBASE_MEASUREMENT_ID }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - name: Remove possible gh-pages cache submodule (avoid .gitmodules error)
        run: rm -rf node_modules/.cache/gh-pages || true
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
          publish_branch: gh-pages
```

El flujo se activa al hacer push a la rama `main`, instala dependencias, ejecuta `npm run build` y publica el contenido de `dist/` en la rama `gh-pages`. Para un proyecto que necesite `base`, asegúrese de que `vite.config.js` lo defina según el nombre del repositorio.

### Variables de entorno con secrets

Riesgo de exposición: en Vue 3 toda variable que empiece por `VITE_` queda embebida en el bundle y accesible en el navegador; no debe usarse para información realmente privada, aunque sí para claves públicas o endpoints.

**Dónde se definen:** 
En GitHub, vaya a **Settings → Secrets and variables → Actions → New repository secret** y cree entradas como `VITE_API_URL` o las claves de Firebase.

Cómo se consumen en el workflow: la sección `env:` del flujo referencia los secrets listados a continuación y los inyecta en la fase de build.
  - `secrets.VITE_FIREBASE_API_KEY`
  - `secrets.VITE_FIREBASE_AUTH_DOMAIN`
  - `secrets.VITE_FIREBASE_PROJECT_ID`
  - `secrets.VITE_FIREBASE_STORAGE_BUCKET`
  - `secrets.VITE_FIREBASE_MESSAGING_SENDER_ID`
  - `secrets.VITE_FIREBASE_APP_ID`
  - `secrets.VITE_FIREBASE_MEASUREMENT_ID`



Motivo: se evita almacenar credenciales en el repositorio o en el archivo del workflow y se limitan al entorno de ejecución de GitHub Actions.

## Buenas prácticas

Ejecute `npm run preview` antes de cada despliegue. Mantenga `dist/` ignorado en Git (`.gitignore`). Si utiliza Vue Router en modo history, confirme los rewrites (Firebase) o configure rutas en GitHub Pages. Defina variables de entorno separando desarrollo y producción. No incluya claves privadas en el build ni en el repositorio.
