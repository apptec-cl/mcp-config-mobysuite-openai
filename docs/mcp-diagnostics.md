# Diagnóstico MCP del 9 de noviembre de 2026

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
