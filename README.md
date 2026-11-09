# Mobysuite Reports para OpenAI

Borrador del complemento de Mobysuite para consultar reportes de ventas desde un cliente MCP compatible. Destinado a gerentes o administradores en Chile. El complemento es gratuito.

**Estado: en preparación; no publicado ni listo para enviar a revisión.**

## Contenido

- `plugin.json`: ficha, disponibilidad en Chile y metadatos de publicación.
- `mcp.json`: conexión remota con OAuth y registro dinámico de clientes (DCR).
- `assets/icon.png`: icono oficial de Mobysuite, preparado en PNG de 512 × 512.
- `docs/pages/`: borradores HTML de privacidad, términos y soporte. Contienen decisiones pendientes y no deben publicarse como textos definitivos sin revisión.
- `scripts/package.py`: validaciones básicas y generación del ZIP de borrador.

## Conexión

La URL del MCP varía según el cliente. La configuración propone una plantilla OpenAI `urlTemplates`:

```text
https://mcp.mobysuite.com/{cliente}/reports
```

Ejemplos de URLs concretas facilitadas por el publicador:

- Copérnico: `https://mcp.mobysuite.com/copernico/reports`.
- Imagina: `https://mcp.mobysuite.com/imagina/reports`.

`url` contiene la misma plantilla, para no fijar un cliente predeterminado. El soporte y la configuración de esta plantilla deben validarse al importar el paquete en el portal y en el host de destino; no se ha comprobado el flujo de selección del cliente. En clientes MCP genéricos sin soporte de esta extensión, configurar la URL concreta de la organización; no enviar literalmente las llaves al servidor.

Cada conexión debe completar OAuth para su recurso concreto. El valor de `cliente` identifica la ruta, pero no concede acceso. El servidor debe verificar la organización y el rol autorizado y rechazar un token de otra organización. Esto requiere implementación y pruebas en el servidor, que no se incluye en este repositorio.

El servidor anuncia OAuth con flujo de código de autorización, PKCE S256, registro dinámico y scope `mcp:tools`. El transporte `streamable-http` está configurado como propuesta; falta verificar el handshake y la conexión autenticada.

No incluyas contraseñas, tokens ni credenciales de revisores en este repositorio. El cliente debe completar OAuth mediante el flujo del host. La cuenta de prueba para revisores se configura en los campos seguros del portal.

## Generar el paquete

Requiere Python 3; no necesita dependencias adicionales.

```sh
python3 scripts/package.py
```

Genera `dist/mobysuite-reports-DRAFT.zip`, con un único directorio `mobysuite-reports/` que contiene los manifiestos y el icono. El ZIP excluye las páginas de documentación y archivos locales. Estas validaciones son básicas: no sustituyen la validación ni el escaneo del portal de OpenAI.

## Verificado el 9 de noviembre de 2026

- Los endpoints de Copérnico e Imagina devuelven HTTP 401 sin token y anuncian metadatos del recurso protegido correspondientes a su ruta. Ambos anuncian el mismo servidor de autorización y el scope `mcp:tools`.
- Los metadatos OAuth publicados anuncian `/authorize`, `/token` y `/register`, con PKCE S256.
- Los manifiestos se pueden leer como JSON y el ZIP generado contiene los componentes esperados.
- El icono se obtuvo de `https://mobysuite.com/icon.svg` y se preparó sobre un lienzo cuadrado.

Según lo confirmado por el publicador, el MCP solo consulta datos y no guarda consultas ni resultados. El acceso está destinado a gerentes o administradores. Estas declaraciones aún deben verificarse contra la implementación: este repositorio contiene la configuración del complemento, no el servidor ni el control de acceso.

## Pendiente antes de la publicación

1. Revisar los borradores de privacidad y términos: completar razón social, tratamiento de credenciales OAuth y registros técnicos, proveedores y procedimiento de solicitudes de privacidad. Contacto confirmado: `soporte@mobysuite.com`.
2. Publicar las páginas de soporte, privacidad y términos e incorporar sus URLs reales en `plugin.json`. La política existente en `https://mobysuite.com/cl/politicas` describe el sitio web y conexiones con Google; aún falta cubrir esta integración MCP.
3. Verificar identidad del publicador y dominio en el portal de OpenAI.
4. Validar la plantilla de URL en el portal y el host. Conectar por OAuth con URLs concretas de ambos clientes, verificar el transporte y descubrir las herramientas reales. Comprobar el rol autorizado y el aislamiento entre organizaciones, incluyendo el rechazo de tokens cruzados.
5. Revisar los esquemas y anotaciones de herramientas; preparar y ejecutar cinco casos positivos y tres negativos con datos de prueba.
6. Grabar una demo real, verificar que los revisores puedan verla e incorporar la URL y los casos al manifiesto.
7. Generar e inspeccionar el paquete final, cargarlo en el portal y resolver los requisitos y hallazgos antes de enviarlo a revisión.

No se ha probado el inicio de sesión, el control de roles ni la ejecución de herramientas. Tampoco se ha creado una publicación pública o enviado el complemento a revisión.

Referencia: [Envío y publicación de complementos en OpenAI](https://developers.openai.com/plugins/deploy/submission).
