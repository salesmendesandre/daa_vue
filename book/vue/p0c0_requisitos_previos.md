(sesion01)=
# Requisitos previos (antes de empezar)

## Resumen
Este capítulo establece las bases técnicas necesarias para iniciar el curso con **Vue 3**. Proporciona una síntesis de los conocimientos de JavaScript ES6, las herramientas que deben estar instaladas y las verificaciones mínimas para asegurar que el entorno de desarrollo (con **Vite**) esté listo antes de empezar a desarrollar.

## Resultados de aprendizaje
- Identificar y aplicar los conceptos ES6 fundamentales que se utilizarán durante el curso.
- Preparar un entorno multiplataforma homogéneo con Node.js LTS gestionado con nvm, npm, Git y VS Code correctamente configurados.
- Verificar instalaciones mediante comandos específicos y resolver incidencias típicas de configuración.
- Establecer prácticas iniciales de versionado, seguridad y gestión de archivos sensibles.

## Conocimientos previos de programación
Se espera que el estudiantado domine los elementos básicos de programación y tenga familiaridad con la consola de comandos. Los siguientes conceptos de ES6 serán esenciales:

### Conceptos ES6 imprescindibles
- **`let` y `const`**: comprender el alcance de bloque y la inmutabilidad referencial.

  ```javascript
  const apiUrl = "https://api.example.com";
  let retries = 0;
  if (retries === 0) {
    const message = "Primer intento";
    console.log(message);
  }
  // console.log(message); // ReferenceError: message is not defined
  ```

- **Arrow functions**: sintaxis concisa.

  ```javascript
  const items = [1, 2, 3];
  const squared = items.map((value) => value ** 2);
  console.log(squared); // [1, 4, 9]
  // Explicación:
  // La función `map` itera sobre cada elemento del array `items`.
  // Para cada `value` (valor), la arrow function `(value) => value ** 2`
  // calcula su cuadrado (`value` elevado a la potencia de 2).
  // El resultado es un nuevo array `squared` con los valores transformados.
  ```

  ```javascript
  const numbers = [1, 2, 3, 4, 5, 6];
  const evens = numbers.filter((value) => value % 2 === 0);
  console.log(evens); // [2, 4, 6]
  // Explicación:
  // La función `filter` itera sobre cada elemento del array `numbers`.
  // Para cada `value` (valor), la arrow function `(value) => value % 2 === 0`
  // comprueba si el número es par.
  // El resultado es un nuevo array `evens` con los valores que cumplen la condición.
  ```

- **Módulos ES6**: uso de `import`/`export` para dividir responsabilidades.

  ```javascript
  // utils/math.js
  export const add = (a, b) => a + b;

  // main.js
  import { add } from "./utils/math.js";
  console.log(add(2, 3)); // 5
  ```

- **Destructuring y spread**: extracción y combinación flexible de datos.

  El **destructuring** permite extraer datos de arrays u objetos en variables distintas, simplificando el acceso a sus propiedades. El **spread operator (`...`)** permite expandir elementos de un iterable (como un array) o propiedades de un objeto.

  ```javascript
  // Ejemplo de Destructuring y Spread
  const config = { theme: "light", lang: "es", shortcuts: true };

  // Destructuring: extrae `theme` y agrupa el resto en `rest`
  const { theme, ...rest } = config;
  console.log(theme); // "light"
  console.log(rest);  // { lang: "es", shortcuts: true }

  // Spread: crea un nuevo objeto `extended` combinando `config`
  // y sobrescribiendo la propiedad `lang`.
  const extended = { ...config, lang: "en" };
  console.log(extended.lang); // "en"
  console.log(extended.theme); // "light"
  ```

- **`async/await` con manejo de errores**: flujos asíncronos legibles.

  `async/await` es una sintaxis que simplifica la escritura de código asíncrono basado en Promesas, haciéndolo más legible y fácil de mantener. Una función declarada con `async` devuelve implícitamente una Promesa. La palabra clave `await` pausa la ejecución de la función hasta que la Promesa se resuelva o rechace.

  Es fundamental envolver las llamadas `await` en un bloque `try...catch` para gestionar errores de red o del servidor de forma controlada.

  ```javascript
  const fetchData = async (endpoint) => {
    try {
      // `await` pausa la ejecución hasta que `fetch` complete la petición.
      const response = await fetch(endpoint);

      // Si la respuesta no es exitosa (ej. error 404 o 500),
      // se lanza un error para ser capturado por el bloque `catch`.
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      // `await` de nuevo para parsear la respuesta como JSON.
      return await response.json();
    } catch (error) {
      // Se captura cualquier error ocurrido en el bloque `try`.
      console.error("Error de red o de servidor:", error.message);

      // Se relanza el error para que el código que llama a `fetchData`
      // también pueda gestionarlo.
      throw error;
    }
  };

  // Ejemplo de uso de fetchData
  const loadUserData = async () => {
    try {
      const data = await fetchData("https://api.example.com/user");
      console.log("Datos de usuario:", data);
    } catch (error) {
      console.error("No se pudieron cargar los datos del usuario.");
      // Aquí se podría mostrar un mensaje de error en la UI.
    }
  };

  loadUserData();
  ```

## Entorno y herramientas
- **nvm** (Node Version Manager) configurado en el sistema.
- **Node.js LTS** (actualmente 20.x) instalado y activado mediante nvm, con npm incluido por defecto.
- **Gestor de paquetes**: npm instalado por defecto.
- **Git 2.3x o superior** para control de versiones y colaboración.
- **Visual Studio Code** con extensiones específicas para **Vue** y JavaScript.
- **Vite** como herramienta de construcción y servidor de desarrollo para proyectos Vue 3.
- **Cuenta gratuita de Firebase** para acceder a la consola de firebase.
- **Herramientas opcionales**: WSL (Windows Subsystem for Linux), **Vue.js Devtools** (extensión de navegador), Node.js Tools (inspector y profiler).

### Cuenta de Firebase
1. Acceda a <https://firebase.google.com> y pulse **Ir a consola**.
2. Inicie sesión con una cuenta de Google. Si no dispone de una, créela antes de la sesión.
3. Revise los términos de servicio y acepte.
4. Verifique que puede acceder al panel principal de Firebase Console en <https://console.firebase.google.com>. (No cree el proyecto aún).

## Instalación por sistema operativo (Windows/macOS/Linux)

Pasos:
1. Instalar nvm
2. Instalar Node.js LTS con nvm
3. Instalar Git
4. Configurar VS Code
5. Instalar extensiones recomendadas
6. Comprobaciones de versiones

### Windows (PowerShell)
1. Instale `nvm-windows` desde <https://github.com/coreybutler/nvm-windows>. Tras finalizar, abra una nueva terminal.
2. Ejecute `nvm install --lts` y `nvm use --lts` para descargar y activar la versión LTS más reciente de Node.js.
3. Instale Git desde <https://git-scm.com/download/win>. Habilite la opción "Git from the command line".
4. Instale Visual Studio Code desde <https://code.visualstudio.com/>.

### macOS (Terminal)
1. Instale nvm (con Homebrew):

   ```bash
   brew install nvm
   mkdir -p ~/.nvm
   echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
   echo '[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && . "/opt/homebrew/opt/nvm/nvm.sh"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. Instale y active Node.js LTS con nvm:

   ```bash
   nvm install --lts
   nvm use --lts
   ```

3. Instale Git si no está presente: `brew install git`.
4. Instale Visual Studio Code desde <https://code.visualstudio.com/>.

### macOS (Clase)
En el aula de informática 5 de la universidad, ejecute el siguiente script para automatizar la instalación de Node.js y NPM (Debemos hacerlo todos los dias ya que las máquinas se reinician el estado y se pierden las instalaciones):

  :::{tab-set}

  :::{tab-item} Instalación de Node.js y NPM en macOS en el aula de informática 5
  ```{code-block} bash
    curl -fsSL https://raw.githubusercontent.com/salesmendesandre/daa_vue_examples/refs/heads/main/00_prerequisites/install_node_macos_inf5.sh -o install_node_macos_inf5.sh && chmod +x install_node_macos_inf5.sh && ./install_node_macos_inf5.sh
  ```
  :::

Tras ejecutar el script anterior, confirme que `nvm install --lts` y `nvm use --lts` se han aplicado correctamente (el script ya los ejecuta, pero es recomendable repetirlos para garantizar que la versión activa sea la LTS más reciente).

### Linux (Bash)
1. Instale nvm:

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   source ~/.bashrc
   ```

2. Instale y active Node.js LTS con nvm:

   ```bash
   nvm install --lts
   nvm use --lts
   ```

3. Instale Git desde el gestor de paquetes:

   ```bash
   sudo apt-get install -y git
   ```

4. Instale Visual Studio Code desde <https://code.visualstudio.com/>.

## Verificación de la instalación
Ejecute los siguientes comandos y compare con la columna de salida esperada:

| Comando | Salida esperada (formato) |
| --- | --- |
| `node -v` | `v20.x.x` (o superior LTS) |
| `npm -v` | `10.x.x` |
| `git --version` | `git version 2.3x.x` |

## Extensiones recomendadas

Instala estas extensiones desde el **Marketplace de VS Code** (`Ctrl + Shift + X`):

- **Vue - Official (Volar)** (Vue) → soporte para SFC (`.vue`), IntelliSense y diagnóstico.
- **ESLint** (Microsoft) → análisis estático de JavaScript/TypeScript.
- **Prettier – Code formatter** (Prettier) → formato automático y consistente.
- **TypeScript Vue Plugin (Volar)** (Vue) → tipado y herramientas avanzadas para Vue 3 (opcional si trabajas con TS).

### Configuración rápida de formato automático
1. Instala las extensiones **Prettier** y **ESLint**.
2. Abre la **paleta de comandos** (`Ctrl + Shift + P`) → “**Format Document With… → Configure Default Formatter → Prettier**”.
3. Activa “**Format On Save**” en la configuración.

## Configuración inicial de Git
1. Defina identidad global:

   ```bash
   git config --global user.name "Nombre Apellido"
   git config --global user.email "nombre.apellido@example.com"
   ```

2. Verifique configuración:

   ```bash
   git config --global --list
   ```

3. (Opcional) Configure una clave SSH:

   ```bash
   ssh-keygen -t ed25519 -C "nombre.apellido@example.com"
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   cat ~/.ssh/id_ed25519.pub
   ```

   Agregue la clave pública al proveedor de Git (GitHub, GitLab, etc.).

4. Pruebe clonación y comandos básicos:

   ```bash
   git clone git@github.com:usuario/repositorio-ejemplo.git
   cd repositorio-ejemplo
   git status
   ```

## Buenas prácticas de versionado
- Realice commits pequeños y atómicos con mensajes claros (imperativo, máximo 72 caracteres).
- Incluya un archivo `README.md` por proyecto.
- Etiquete versiones o hitos importantes (`git tag v0.1.0`).

## Seguridad y `.env`
1. Cree un archivo `.env` en la raíz del proyecto con las variables necesarias (ejemplo para Firebase):

   ```bash
   touch .env
   echo "VITE_FIREBASE_API_KEY=tu_clave_publica" >> .env
   echo "VITE_FIREBASE_AUTH_DOMAIN=tu_proyecto.firebaseapp.com" >> .env
   ```

2. Añada `.env` a `.gitignore`:

   ```bash
   echo ".env" >> .gitignore
   ```

3. No almacene secretos privados (como claves de servicio) en el repositorio. Para variables compartibles use `.env.example` con campos vacíos.
4. Revise periódicamente el historial de Git en busca de filtraciones accidentales (`git log -G"API_KEY"`).

## Solución de problemas (FAQ)
- **Node no se reconoce en la terminal (Windows)**: abra una nueva terminal tras instalar `nvm-windows`, ejecute `nvm list` para comprobar versiones disponibles y active la LTS con `nvm use --lts`.
- **Permisos denegados en macOS/Linux**: evite `sudo npm install -g`. Utilice nvm o Corepack para gestionar instalaciones sin root.
- **`git config` no persiste**: compruebe que dispone de permisos de escritura en `~/.gitconfig`.
- **Errores de clave SSH**: regenere la clave y verifique que el servicio remoto tenga la clave pública registrada.

## Checklist de verificación
- [ ] Node.js LTS instalado mediante nvm y npm reconocidos en la terminal.
- [ ] Git instalado y configurado con nombre, correo y (opcional) clave SSH.
- [ ] VS Code instalado, accesible con el comando `code`, y extensiones esenciales para Vue habilitadas (Volar, ESLint, Prettier).
- [ ] Cuenta de Firebase creada y acceso confirmado a Firebase Console.
- [ ] Ejecuté todos los comandos de verificación y obtuve versiones compatibles.


## Referencias
- nvm-sh. "Node Version Manager". <https://github.com/nvm-sh/nvm#readme>
- Corey Butler. "nvm-windows". <https://github.com/coreybutler/nvm-windows>
- npm, Inc. "npm Documentation". <https://docs.npmjs.com>
- Software Freedom Conservancy. "Git Documentation". <https://git-scm.com/docs>
- Microsoft. "Visual Studio Code Docs". <https://code.visualstudio.com/docs>
- Vue.js. "Guía de Vue 3". <https://vuejs.org/guide/introduction.html>
- Vite. "Getting Started". <https://vitejs.dev/guide/>
