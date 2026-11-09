---
name: setup
description: Configurar y verificar la conexión OAuth de Mobysuite Reports después de instalar el complemento o cuando el usuario solicita conectar su cuenta.
---

# Conectar Mobysuite Reports

Esta instalación desde Git corresponde a **Imagina**, con URL
`https://mcp.mobysuite.com/imagina/reports`.

1. Explica al usuario qué organización está conectando. Si solicita otra,
   no continúes con Imagina ni cambies la ruta de un token existente. Para
   Copérnico, indica que debe instalar la variante «Mobysuite Reports · Copérnico»
   del mismo marketplace. Para otro cliente, pide su identificador para que el
   mantenedor prepare la variante; no prometas un selector que el host no ofrece.
2. Comprueba las herramientas y el estado de autenticación del MCP que pertenece
   a este complemento. No cuentes como prueba una conexión independiente llamada
   `mobysuite`. Si no aparece ningún MCP del complemento, informa del fallo de
   registro y pide actualizar el marketplace y el complemento; no inventes reportes.
3. Si el host muestra «Conectar» o «Iniciar sesión» para el MCP del complemento,
   guía al usuario a esa acción y al flujo OAuth soportado por el host. No abras
   `/authorize` sin los parámetros generados por el cliente OAuth. No crees una
   conexión independiente ni ejecutes `codex mcp add` como sustituto del onboarding.
4. El proveedor abre un formulario de Mobysuite. El usuario introduce allí sus
   credenciales de integración (Client ID y Client secret) y completa el
   consentimiento. Nunca solicites que pegue credenciales o tokens en el chat,
   archivos del complemento o repositorio. No rellenes ni aceptes el consentimiento
   en su nombre sin la autorización que requiera el host.
5. Verifica el resultado: autenticación completada y herramientas descubiertas
   en la conexión del complemento. Si ya existe una sesión válida, el host puede
   reutilizarla; no cierres sesiones ni borres tokens para forzar un formulario.
6. Ofrece una prueba de lectura mínima, como listar proyectos. Comprueba si la
   herramienta devuelve error antes de afirmar que funciona. Un error del formato
   de respuesta del servidor es distinto de un fallo OAuth; informa cuál ocurrió.

No consultes datos de otra organización ni inventes `companyId`, IDs de proyectos
o permisos. No cambies registros ni solicites permisos adicionales como prueba.

La instalación desde Git no publica el complemento en el directorio público.
Si la autorización no se inicia automáticamente, indica el estado observado y la
acción de conexión disponible; no afirmes que instalar equivale a estar conectado.
