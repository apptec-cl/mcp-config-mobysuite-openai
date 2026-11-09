# Mobysuite Reports para OpenAI

Complemento gratuito para consultar reportes de ventas de Mobysuite, destinado a gerentes y administradores en Chile. **En preparación; no publicado en el directorio público de OpenAI.**

## Instalar en Codex desde GitHub

En **Complementos → Agregar → Agregar marketplace**:

- Origen: `https://github.com/apptec-cl/mcp-config-mobysuite-openai`
- Referencia: `main`
- Rutas dispersas: vacío.

En la fuente **Mobysuite**, elige la organización antes de instalar:

| Complemento | Cliente | URL MCP |
| --- | --- | --- |
| Mobysuite Reports · Copérnico | Copérnico | `https://mcp.mobysuite.com/copernico/reports` |
| Mobysuite Reports · Imagina | Imagina | `https://mcp.mobysuite.com/imagina/reports` |

La raíz del repositorio contiene la variante de Copérnico; `clients/imagina/` contiene la variante de Imagina. Se usan URLs concretas y nombres de servidor diferentes. Elegir una ruta no concede acceso: el servidor debe comprobar la organización y el rol del usuario.

## Conexión y onboarding

1. Actualiza el marketplace e instala la variante de tu organización.
2. Completa la acción de conexión OAuth ofrecida por Codex para el MCP del complemento. La política del catálogo es `ON_INSTALL`. Si el host reutiliza una sesión válida, puede no mostrar otro formulario.
3. En el formulario de **Mobysuite**, introduce las credenciales de integración (Client ID y Client secret) y completa la autorización. No las pegues en el chat ni en el repositorio.
4. La guía de setup del complemento comprueba la organización, el estado de conexión y las herramientas. No crea otro MCP independiente para simular una instalación correcta.
5. Prueba una lectura mínima. Autenticación completada no equivale a que todas las herramientas respondan correctamente.

La instalación desde Git usa descubrimiento OAuth estándar: el servidor anuncia el recurso protegido, el servidor de autorización, registro dinámico, PKCE S256 y scope `mcp:tools`.

### Corrección de la versión 0.1.2

El lector local de Codex instalado descartó el MCP cuando la entrada de `mcp.json` contenía `extensions.com.openai`. Se reprodujo con configuraciones mínimas: el servidor básico `streamable-http` se descubre, pero agregar `auth` o `urlTemplates` bajo esa extensión deja `mcpServers` vacío. Añadir un overlay no resolvía la entrada portable inválida para ese lector.

La configuración Git ahora usa el MCP básico con URL concreta. El lector de Codex reconoce ambos servidores y sus skills de setup, y resuelve las rutas del icono. La instalación, la acción automática de conexión y el resultado visual deben verificarse además en el host; los registros de prueba se detallan en `docs/mcp-diagnostics.md`.

## Archivos y generación

- `plugin.json`, `mcp.json`, `skills/setup/`, `assets/`: variante Git de Copérnico.
- `.codex-plugin/plugin.json` y `.mcp.json`: compatibilidad sincronizada para clientes anteriores.
- `clients/imagina/`: variante Git generada para Imagina.
- `.agents/plugins/marketplace.json`: catálogo con ambas variantes.
- `config/mcp.public.json`: propuesta de configuración pública con OAuth y plantilla `{cliente}`, pendiente de validación en el portal.
- `docs/pages/`: borradores HTML de privacidad, términos y soporte. No son textos definitivos.

Requiere Python 3, sin dependencias adicionales:

```sh
python3 scripts/build_client_plugins.py
python3 scripts/package.py
```

El primer comando sincroniza Imagina con los componentes comunes. El segundo valida los archivos y genera `dist/mobysuite-reports-DRAFT.zip` para preparar la publicación pública: usa nombre genérico, `config/mcp.public.json` y el icono. Excluye el catálogo, las variantes Git, el setup específico de una organización y las páginas HTML. No es un ZIP listo para enviar a revisión.

La plantilla de publicación propuesta es `https://mcp.mobysuite.com/{cliente}/reports`. Su importación y flujo de selección aún deben validarse en el portal. La presencia de esta plantilla en el borrador público no implica que el Codex local ofrezca un formulario para resolverla. Para otros clientes, el mantenedor debe preparar una variante con la URL confirmada.

## Estado de pruebas

- Los endpoints de Copérnico e Imagina responden HTTP 401 sin token y anuncian recursos OAuth correspondientes a su ruta.
- La conexión independiente `mobysuite` de Copérnico completó OAuth y expuso 18 herramientas. Esa prueba es independiente del complemento Git.
- `reports_list_projects` falló por formato de salida estructurada en el servidor: véase [diagnóstico](docs/mcp-diagnostics.md).
- El icono oficial procede de `https://mobysuite.com/icon.svg` y está preparado en PNG de 512 × 512.

Según el publicador, el MCP solo consulta datos y no guarda consultas ni resultados; el acceso está destinado a gerentes o administradores. El servidor y su control de roles no están en este repositorio. El aislamiento entre organizaciones y el rechazo de tokens cruzados siguen pendientes de prueba.

## Pendiente para el directorio público

1. Revisar y completar las páginas de privacidad y términos: razón social, tratamiento de credenciales OAuth y registros técnicos, proveedores y solicitudes de privacidad. Contacto: `soporte@mobysuite.com`.
2. Publicar soporte, privacidad y términos e incorporar URLs verificadas. La política actual de `https://mobysuite.com/cl/politicas` aún no describe esta integración MCP.
3. Validar el paquete público y la plantilla en el portal; completar identidad y dominio.
4. Corregir las respuestas del servidor y verificar permisos, esquemas y anotaciones de herramientas.
5. Preparar y ejecutar cinco casos positivos y tres negativos, grabar una demo real y configurar acceso seguro para revisores.
6. Resolver las comprobaciones del portal antes del envío a revisión.

Referencia: [Documentación oficial de paquetes e instalación](https://developers.openai.com/plugins/build/plugins), [envío y publicación](https://developers.openai.com/plugins/deploy/submission).
