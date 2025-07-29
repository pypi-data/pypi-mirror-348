# raglib

`raglib` es una librería para ejecutar agentes de IA con herramientas y conexión a base de datos. Este README explica cómo configurar y usar la librería.

## Variables de entorno necesarias

Crea un archivo `.env` en la raíz de tu proyecto con las siguientes variables:

```env
DATABASE_URL=sqlite:///ruta/a/tu/base_de_datos.db
AI_MODEL=gpt-4
OPENAI_API_KEY=tu_api_key
```

- `DATABASE_URL`: URL de conexión a la base de datos (por ejemplo, SQLite, PostgreSQL, etc.).
- `AI_MODEL`: Nombre o identificador del modelo de IA que deseas usar (por ejemplo, `gpt-4`).

## Instalación

Instala las dependencias necesarias (ajusta según tu gestor de paquetes):

```bash
pip install -r requirements.txt
```

## Uso básico

Ejemplo de cómo usar la clase `Rag` en tu código:

```python
from raglib.rag import Rag
import asyncio

async def main():
    rag = Rag()
    respuesta = await rag.run_query("¿Cuál es la capital de Francia?")
    print(respuesta)

asyncio.run(main())
```

## Notas

- Asegúrate de tener configuradas las variables de entorno antes de ejecutar tu aplicación.
- El agente creado en `rag.py` solo responde en español.
- Puedes personalizar el modelo de IA y la base de datos modificando las variables en tu `.env`.

## Contribución

Si deseas contribuir, abre un issue o un pull request.
