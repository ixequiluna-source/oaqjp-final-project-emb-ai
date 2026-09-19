![Emotion Detector](docs/assets/cover.svg)

# Emotion Detector

**Una integración pequeña y legible: del texto a la respuesta de un modelo.**

Aplicación educativa con Python y Flask que consulta Watson NLP Skills Network para obtener cinco puntuaciones —ira, disgusto, miedo, alegría y tristeza— y la etiqueta con mayor puntuación. El modelo configurado trabaja con texto en inglés.

[English](README.md) · [Verificación y límites](docs/VERIFICATION.md) · [Autor](https://ixequiluna.ai)

Proyecto final del curso **IBM/Coursera Python Project for AI & Application Development**, mantenido por **Dr. Ixequi Luna**. La implementación integra un modelo externo; no entrena uno propio.

## Prueba la implementación

Sigue la [instalación para Windows, macOS y Linux](README.md#run-locally). Después:

```sh
python -m unittest discover -v
python server.py
```

Abre **http://localhost:5000** y utiliza una frase sintética en inglés. La inferencia real requiere disponibilidad del endpoint externo. Las pruebas usan respuestas simuladas para verificar la selección de etiquetas; no miden exactitud del modelo.

## Qué vale la pena revisar

- La separación entre paquete Python, servidor Flask y cliente web.
- El resultado consistente para una entrada vacía.
- El timeout explícito y la respuesta 503 ante un fallo de red del proveedor.
- Los cinco casos deterministas, uno por etiqueta dominante.

La interfaz ya incorpora carga, recuperación de errores, cancelación al editar y cinco indicadores. El servidor valida respuestas incompletas y puntuaciones fuera de rango. El texto viaja en el cuerpo de POST, con límite de 2,000 caracteres; la ruta GET heredada permanece solo por compatibilidad con el curso. No se utiliza para diagnóstico ni con datos personales: el contenido se envía a un proveedor externo.
