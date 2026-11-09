# Mobysuite Reports para OpenAI

Complemento gratuito para consultar reportes de ventas de Mobysuite, destinado a gerentes y administradores en Chile. **En preparación; no publicado en el directorio público de OpenAI.**

## Instalación y conexión

En **Complementos → Agregar → Agregar marketplace**, usa:

- Origen: `https://github.com/apptec-cl/mcp-config-mobysuite-openai`
- Referencia: `main`
- Rutas dispersas: vacío.

Selecciona la fuente **Mobysuite** e instala **Mobysuite Reports**. Desde la versión **0.2.0**, hay un único complemento con un endpoint compartido:

```text
https://mcp.mobysuite.com/editable/reports
```

El flujo previsto es:

1. Conectar el MCP del complemento mediante OAuth.
2. En el formulario de Mobysuite, editar **Customer** con el identificador de la inmobiliaria, por ejemplo `copernico` o `imagina`.
3. Introducir Client ID y Client secret de integración únicamente en Mobysuite y completar la autorización.
4. Volver a Codex y comprobar que aparezcan las herramientas.

`editable` identifica la ruta compartida, no una inmobiliaria. El servidor debe comprobar que las credenciales corresponden al Customer y aplicar los permisos de gerente o administrador. La edición del campo no otorga acceso por sí misma.

La guía de onboarding se encuentra en `skills/setup/SKILL.md`. Si ya existe una autorización válida, Codex puede reutilizarla. Una autorización anterior para `/copernico/reports` no demuestra que la nueva conexión funcione; hay que verificar específicamente el MCP `mobysuite-reports` con `/editable/reports`.

No compartas credenciales ni tokens por el chat o repositorio. No se cierra la conexión independiente `mobysuite` ni se borran sus tokens al actualizar el complemento.

## Configuración Git y pública

- `plugin.json`, `mcp.json`, `skills/setup/`, `assets/`: complemento Git con endpoint compartido.
- `.codex-plugin/plugin.json`, `.mcp.json`: compatibilidad sincronizada.
- `.agents/plugins/marketplace.json`: catálogo con una entrada.
- `config/mcp.public.json`: mismo endpoint con metadatos OAuth para el portal de publicación.
- `docs/pages/`: borradores de privacidad, términos y soporte; no son textos definitivos.

El lector de Codex probado descarta una entrada MCP Git con `extensions.com.openai`. Por ello `mcp.json` local declara solo transporte y URL, y OAuth se descubre mediante los metadatos del servidor. El ZIP público usa la configuración separada, con OAuth DCR y scope `mcp:tools`. Ya no se necesita `urlTemplates`.

Las variantes anteriores por inmobiliaria fueron retiradas del catálogo y del código generado. Si instalaste la antigua variante de Imagina, migra al complemento común mediante el flujo de desinstalación e instalación de Codex; este cambio del catálogo no borra una instalación ni revoca autorizaciones existentes.

## Generar el ZIP

Requiere Python 3, sin dependencias adicionales:

```sh
python3 scripts/package.py
```

Genera e inspecciona `dist/mobysuite-reports-DRAFT.zip`, con manifiestos portables, onboarding y el icono. Excluye el catálogo Git, los overlays y las páginas HTML. El paquete sigue siendo un borrador y no está listo para revisión pública.

## Verificaciones

- `/editable/reports` devuelve HTTP 401 sin token y anuncia su metadata de recurso protegido con la misma URL exacta.
- El recurso anuncia `https://mcp.mobysuite.com` como servidor de autorización y `mcp:tools` como scope.
- Antes de la migración, el MCP del complemento en 0.1.2 completó OAuth para la URL fija de Copérnico y expuso 18 herramientas. No equivale a una prueba del endpoint nuevo.
- `reports_list_projects` falló anteriormente por el formato de salida estructurada; véase [diagnóstico](docs/mcp-diagnostics.md).
- El icono oficial procede de `https://mobysuite.com/icon.svg` y se preparó en PNG de 512 × 512.

El formulario editable y la nueva autorización requieren verificación en el host. El control de roles, la correspondencia entre Customer y credenciales y el aislamiento entre inmobiliarias deben verificarse en el servidor, cuya implementación no está en este repositorio.

Según el publicador, el MCP solo consulta datos y no guarda consultas ni resultados.

## Pendiente para el directorio público

1. Verificar OAuth del endpoint compartido y la selección de inmobiliaria; corregir el contrato de respuesta de las herramientas.
2. Completar privacidad y términos: razón social, credenciales OAuth y registros técnicos, proveedores y solicitudes de privacidad. Contacto: `soporte@mobysuite.com`.
3. Publicar soporte, privacidad y términos e incorporar URLs verificadas. La política en `https://mobysuite.com/cl/politicas` aún debe cubrir esta integración.
4. Completar identidad y dominio en el portal; verificar permisos, esquemas y anotaciones.
5. Preparar y ejecutar cinco casos positivos y tres negativos, grabar una demo real y configurar una cuenta de prueba para revisores en los campos seguros del portal.
6. Resolver las comprobaciones del portal antes de enviar a revisión.

Referencias: [paquetes e instalación](https://developers.openai.com/plugins/build/plugins), [envío y publicación](https://developers.openai.com/plugins/deploy/submission).
