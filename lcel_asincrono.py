import asyncio
import os
# from langchain_openai import ChatOpenAI
# from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env


# -- Selección del proveedor de LLM según la variable de entorno
if os.getenv("LLM_PROVIDER", "ollama") == "openai":
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
else:
    from langchain_ollama import ChatOllama
    model = ChatOllama(model="llama3.2", temperature=0.7)

parser = StrOutputParser()

# -- Template
template = ChatPromptTemplate.from_messages([
    ("system", "{system}"),
    ("human", "{pregunta}")
])

# -- Cadena: --
pregunta_chain = template | model | parser

async def main():
    system = ( 
        "Sos una persona de una cordura inquebrantable. Respondés en un tono "
        "plano, literal y ligeramente aburrido, como un manual de instrucciones. "
        "Nada de metáforas, entusiasmo ni humor. Máximo 3 oraciones. ")
    pregunta = "Cual es la pregunta mas loca que se te pueda ocurrir?"

    prompt_completo = {"system": system, "pregunta": pregunta}

    resultado = await pregunta_chain.ainvoke(prompt_completo)
    print(f"Resultado: {resultado}")

if __name__ == "__main__":
    asyncio.run(main())
