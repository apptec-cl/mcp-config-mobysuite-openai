# Diagnóstico MCP del 9 de noviembre de 2026

## Onboarding del complemento, versión 0.1.2

Se consultó `plugin/read` del app-server instalado de Codex antes y después del cambio. La versión 0.1.1 presentaba `mcpServers: []` y ninguna skill de onboarding. Una prueba con paquetes mínimos aisló la causa: este lector acepta la entrada portable básica `streamable-http`, pero descarta la entrada al agregar `extensions.com.openai` con `auth` o `urlTemplates`.

La versión 0.1.2 usa URLs concretas y descubrimiento OAuth estándar para instalaciones Git. Se separó la configuración propuesta para el portal en `config/mcp.public.json`. El marketplace ofrece variantes explícitas de Copérnico e Imagina, sin prometer un selector dinámico que esta instalación no ofrece.

Comprobaciones realizadas:

- `plugin/read` de las fuentes reconoce el MCP y la skill de setup de cada variante, y resuelve las rutas del icono.
- El CLI instaló Copérnico 0.1.2. El lector confirmó `installed: true`, `enabled: true`, `mcpServers: ["mobysuite-reports"]` y una `onboardingSkill` activa.
- `mcpServerStatus/list` distinguió `mobysuite` (conexión independiente autorizada, 18 herramientas) de `mobysuite-reports` (MCP del complemento, `notLoggedIn`, cero herramientas antes del login).
- Se inició `mcpServer/oauth/login` con el nombre real `mobysuite-reports`. El host generó una URL de autorización y se abrió el formulario de Mobysuite para Copérnico, solicitando Client ID y Client secret. No se copiaron credenciales al repositorio.

La autorización de este nuevo intento requiere que el usuario complete el formulario. No se ha verificado todavía que el botón de instalación en la interfaz abra automáticamente el flujo, ni el aspecto visual del icono. La skill de setup puede guiar el flujo soportado, pero no reemplaza el cliente OAuth ni crea una conexión independiente.

## Autenticación y descubrimiento

La conexión independiente de Codex `mobysuite`, configurada para Copérnico, completó OAuth con éxito mediante `codex mcp login mobysuite`. El navegador mostró la confirmación de autenticación y el host expuso 18 herramientas de reportes.

Esta comprobación corresponde al MCP independiente, no prueba que el complemento de Git esté registrando su propio servidor. La versión 0.1.1 del complemento se instaló correctamente mediante CLI, con overlay de compatibilidad y rutas de icono corregidas; falta comprobar el icono y el arranque del MCP del complemento en una nueva sesión de la aplicación.

## Fallo reproducido en el servidor

Se invocó una vez `reports_list_projects` con `{}` a través de la conexión autenticada. La herramienta devolvió un error:

```text
structured_content must be a dict or None. Got list
Tools should wrap non-dict values based on their output_schema.
```

La consulta no pasó. No se incluyen datos comerciales, identificadores privados ni credenciales en este informe.

La capa MCP está intentando asignar una lista directamente a su contenido estructurado. La corrección debe realizarse en el código del servidor y mantener coherencia entre la respuesta y su esquema de salida. Una forma posible es devolver un objeto envolvente:

```json
{
  "projects": []
}
```

`projects` debe contener los proyectos obtenidos, reducidos a los campos necesarios, y `outputSchema` debe declarar ese objeto y su array. Es un ejemplo de contrato propuesto, no una corrección desplegada. El repositorio actual contiene configuración y no incluye la implementación del servidor MCP.

Después de corregir el servidor: reconectar o refrescar herramientas, ejecutar de nuevo el listado y verificar que no haya `isError`, que la respuesta cumpla su esquema y que los proyectos pertenezcan a la organización autorizada. El aislamiento entre organizaciones y el control de roles siguen pendientes de prueba.
