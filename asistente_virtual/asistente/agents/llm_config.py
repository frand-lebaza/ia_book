import os
from langchain_openai import ChatOpenAI

# instancia del modelo openAI con configuración personalizada
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=300, # Limitar tokens de salida para evitar respuestas demasiado largas
    streaming=True, # Habilitar streaming para respuestas más rápidas
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
