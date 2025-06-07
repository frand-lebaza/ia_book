import requests
from langchain.tools import Tool, StructuredTool
from .schemas import GetPacientInput, ServicesProfessionalInput, HoursInput

def get_user(document):
    """Obtener información del paciente desde una API externa."""
    api_url = f"http://127.0.0.1:8000/api/pacientes/{document}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Paciente no encontrado"} 

def get_coberturas(*args, **kwargs):
    """Obtener una lista de ciudades desde una API externa."""
    api_url = "http://127.0.0.1:8000/api/coberturas/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al obtener ciudades"}
    
def get_professional(*args, **kwargs):
    """Obtener lista de profesionales por categoría desde una API externa."""
    api_url = "http://127.0.0.1:8000/api/professionals/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al obtener ciudades"}

def get_services(id_professional: int):
    """Obtener servicios de un profesional específico desde una API externa."""
    api_url = f"http://127.0.0.1:8000/api/services/{id_professional}/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al obtener servicios del profesional"}

def get_hours(id_professional: int, date: str, id_service: int):
    api_url = f"http://127.0.0.1:8000/api/get-hours/"
    payload = {
        "tecnicos_id": id_professional,
        "startdate": date,
        "tipo": id_service
    }
    response = requests.post(api_url, json=payload)
    print(f"Request payload: {payload}")
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al obtener horas disponibles"}

# Definir la herramienta para obtener ciudades
tools_previred = [
    StructuredTool.from_function(
        name="get_user",
        func=get_user,
        description="Obtiene información del paciente por su número de documento.",
        args_schema=GetPacientInput
    ),
    Tool.from_function(
        name="get_coberturas",
        func=get_coberturas,
        description="Obtiene una lista de ciudades que tienen cobertura para atender pacientes."
    ),
    Tool.from_function(
        name="get_professional",
        func=get_professional,
        description="Obtiene una lista de profesionales disponibles por categoría."
    ),
    StructuredTool.from_function(
        name="get_services",
        func=get_services,
        description="Obtiene los servicios de un profesional específico.",
        args_schema=ServicesProfessionalInput
    )
]