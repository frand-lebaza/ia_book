import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, SimpleMemory, CombinedMemory
from langchain.prompts import SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor
# from .tools_huila import tools
from .tools_agent import tools
from .prompt import system_message

# instancia del modelo openAI con configuración personalizada
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=300, # Limitar tokens de salida para evitar respuestas demasiado largas
    streaming=True, # Habilitar streaming para respuestas más rápidas
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Crear memoria de conversación
memory = ConversationBufferMemory(
    memory_key="chat_history", # Clave para almacenar el historial de conversación 
    return_messages=True # Retornar mensajes completos en lugar de solo texto
    )

# Crear el prompt del agente    
prompt = ChatPromptTemplate.from_messages(
    [
        system_message, # Mensaje del sistema con instrucciones
        MessagesPlaceholder(variable_name="chat_history"), # Historial de conversación 
        MessagesPlaceholder(variable_name="agent_scratchpad"), # Pasos intermedios del agente
        HumanMessagePromptTemplate.from_template("{input}") # Mensaje del usuario con la entrada actual
    ]
)
# Crear el agente con Function Calling y herramientas
agent_ia = create_openai_functions_agent(
    llm=llm, # Modelo de lenguaje utilizado
    tools=tools, # Herramientas disponibles para el agente
    prompt=prompt # Plantilla de prompt donfigurado para el agente
)

# Inicializar el agente con las herramientas, memoria y gestor de conversación
agent_executor = AgentExecutor(
    agent=agent_ia, # Agente configurado con las herramientas y prompt
    tools=tools, # Herramientas disponibles para el agente
    memory=memory, # Memoria de conversación para mantener el contexto
    verbose=True, # Habilitar salida detallada para depuración
    max_iterations=3, # Número máximo de iteraciones para el agente
    output_key="output" # Clave de salida para el resultado final del agente
)

# Función para responder a mensajes utilizando el agente configurado
def responder_ia_langchain(mensaje):
    # Enviar el mensaje al agente y obtener la respuesta
    respuesta = agent_executor.invoke({"input": mensaje})
    # Retornar la salida del agente
    return respuesta["output"]

