# Refactorización a LCEL Asíncrono

Ejercicio del Módulo 2: migrar de una llamada imperativa al SDK crudo a una **cadena declarativa LCEL ejecutada de forma asíncrona**.

Todo el flujo vive en `lcel_asincrono.py`.

## Qué hace el script

Compone una cadena de tres eslabones con el operador pipe `|`:

```python
pregunta_chain = template | model | parser
```

1. **`ChatPromptTemplate`** — definido con `from_messages` y roles explícitos (`system` / `human`). Ambos mensajes son variables (`{system}` y `{pregunta}`), así que la personalidad y la pregunta se inyectan en tiempo de ejecución.
2. **Modelo (`ChatOpenAI` o `ChatOllama`)** — recibe el `ChatPromptValue` y devuelve un `AIMessage`.
3. **`StrOutputParser`** — extrae el `.content` y devuelve un string limpio, no el objeto `BaseMessage`.

La ejecución es asíncrona: `main()` arma el diccionario de entrada y llama

```python
resultado = await pregunta_chain.ainvoke({"system": system, "pregunta": pregunta})
```

Las claves del diccionario coinciden exactamente con las variables del template — ahí está el contrato de la cadena.

## Selección de proveedor

Antes de construir la cadena, el script lee `LLM_PROVIDER` del `.env`:

| Valor | Modelo |
|---|---|
| `openai` | `ChatOpenAI(model="gpt-4o-mini", temperature=0.7)` |
| cualquier otro / vacío | `ChatOllama(model="llama3.2", temperature=0.7)` (default) |

El `import` se hace dentro de cada rama para no exigir la dependencia del proveedor que no se usa. Como la interfaz `Runnable` es la misma en ambos casos, **la cadena no cambia** al cambiar de modelo: esa es justamente la ventaja de LCEL.

## Cómo correrlo

```bash
pip install -r requirements.txt
cp .env.example .env   # completar OPENAI_API_KEY si se usa openai
python lcel_asincrono.py
```

Con Ollama hay que tener el servidor local corriendo y el modelo `llama3.2` descargado (`ollama pull llama3.2`).