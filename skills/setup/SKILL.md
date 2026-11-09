---
name: setup
description: Configurar y verificar Mobysuite Reports, elegir la inmobiliaria en el formulario OAuth y conectar la cuenta después de instalar el complemento.
---

# Conectar Mobysuite Reports

Este complemento usa un único endpoint compartido:
`https://mcp.mobysuite.com/editable/reports`.
La inmobiliaria se indica en el campo **Customer** del formulario OAuth de
Mobysuite; `editable` es la ruta del endpoint y no el identificador de la empresa.

1. Explica el flujo: conectar, indicar Customer, introducir las credenciales de
   integración en Mobysuite y autorizar. Usa el identificador de inmobiliaria que
   el usuario conoce, por ejemplo `copernico` o `imagina`. No inventes una empresa
   ni asumas que el usuario pertenece a una por tener su URL.
2. Comprueba el MCP y el estado de autenticación del propio complemento
   `mobysuite-reports`. Una conexión independiente llamada `mobysuite` o una
   conexión antigua a `/copernico/reports` no demuestra que esta conexión funcione.
   Si no se registra el servidor, informa del problema y pide actualizar el
   marketplace/complemento antes de probar reportes.
3. Guía al usuario a la acción de conexión o inicio de sesión del host. Usa el
   flujo OAuth generado por ese cliente para `/editable/reports`; nunca abras
   `/authorize` sin los parámetros de OAuth. No crees otro MCP independiente ni
   uses `codex mcp add` como sustituto de la conexión del complemento.
4. En el formulario de Mobysuite, el usuario debe editar **Customer** e introducir
   su Client ID y Client secret de integración. Esas credenciales van únicamente
   en el formulario de Mobysuite. Nunca las pidas en el chat, el repositorio ni
   archivos del complemento. El usuario completa el consentimiento.
5. Si Customer está bloqueado, no aparece o el host sigue usando la ruta de una
   empresa fija, reporta la discrepancia; no declares resuelto el onboarding.
6. Comprueba autenticación completada y herramientas descubiertas en el MCP del
   complemento. El servidor debe validar que las credenciales corresponden al
   Customer y restringir datos y roles. La edición del campo no concede permisos.
   No afirmes que se verificó ese control si solo se probó OAuth.
7. Si ya hay sesión, el host puede reutilizarla. No cierres sesiones ni borres
   tokens para forzar un formulario. Para cambiar de inmobiliaria, usa el flujo
   de reconexión del host y confirma el cambio de cuenta antes de actuar.
8. Ofrece una prueba mínima de lectura, como listar proyectos. Revisa errores
   antes de afirmar que funciona. Distingue fallos de autenticación de errores
   del contrato de salida del servidor. No inventes companyId ni IDs de proyecto.

No consultes datos de otra inmobiliaria ni cambies registros para probar acceso.
La instalación Git no publica el complemento en el directorio público de OpenAI.
