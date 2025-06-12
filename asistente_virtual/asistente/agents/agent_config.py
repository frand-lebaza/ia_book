import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, SimpleMemory, CombinedMemory
from langchain_redis import RedisChatMessageHistory
from langchain.prompts import SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.agents import create_openai_functions_agent, AgentExecutor
from .llm_config import llm
from .tools_agent import tools
from .tools_previred import tools_previred
from .prompt import system_message
from .prompt_previred import system_message_previred
from redis import Redis

redis_client = Redis.from_url(os.getenv("REDIS_URL"))

def get_memory(session_id):
    redis = os.getenv("REDIS_URL")
    print(f"Conectando a Redis en {redis} con session_id: {session_id}")

    message_history = RedisChatMessageHistory(
        session_id=session_id, # ID de sesión para identificar la conversación
        url=redis_client # URL de conexión a Redis
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history", # Clave para almacenar el historial de conversación 
        chat_memory=message_history, # Historial de mensajes almacenado en Redis
        return_messages=True # Retornar mensajes completos en lugar de solo texto
    )
    return memory

memory = ConversationBufferMemory(
        memory_key="chat_history", # Clave para almacenar el historial de conversación         
        return_messages=True # Retornar mensajes completos en lugar de solo texto
    )

user_memories = {}

def get_or_create_memory(thread_id):
    if thread_id not in user_memories:
        user_memories[thread_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return user_memories[thread_id]

# Crear el prompt del agente    
prompt = ChatPromptTemplate.from_messages(
    [
        system_message_previred, # Mensaje del sistema con instrucciones
        MessagesPlaceholder(variable_name="chat_history"), # Historial de conversación 
        MessagesPlaceholder(variable_name="agent_scratchpad"), # Pasos intermedios del agente
        HumanMessagePromptTemplate.from_template("{input}") # Mensaje del usuario con la entrada actual
    ]
)
# Crear el agente con Function Calling y herramientas
agent_ia = create_openai_functions_agent(
    llm=llm, # Modelo de lenguaje utilizado
    tools=tools_previred, # Herramientas disponibles para el agente
    prompt=prompt # Plantilla de prompt donfigurado para el agente
)

# Función para responder a mensajes utilizando el agente configurado
def responder_ia_langchain(mensaje, thread_id):
    # print(f"Recibiendo mensaje: - {mensaje} - para la sesión: {sessionid}")
    # memory = get_memory(session_id) # Obtener la memoria de conversación para la sesión actual
    memory = get_or_create_memory(thread_id)
    # Inicializar el agente con las herramientas, memoria y gestor de conversación
    agent_executor = AgentExecutor(
        agent=agent_ia, # Agente configurado con las herramientas y prompt
        tools=tools_previred, # Herramientas disponibles para el agente
        memory=memory, # Memoria de conversación para mantener el contexto
        verbose=True, # Habilitar salida detallada para depuración
        max_iterations=3, # Número máximo de iteraciones para el agente
        output_key="output" # Clave de salida para el resultado final del agente
    )
    # Enviar el mensaje al agente y obtener la respuesta
    respuesta = agent_executor.invoke({"input": mensaje})
    # Retornar la salida del agente
    return respuesta["output"]

