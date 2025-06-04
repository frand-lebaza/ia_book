import requests
from langchain.tools import Tool, StructuredTool
from .schemas import GetPacientInput, ListHotelsInput, BookHotelInput, TypeActivitiesInput

def get_paciente(document):
    """Obtener información del paciente desde una API externa."""
    api_url = f"http://127.0.0.1:8000/api/pacientes/{document}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Paciente no encontrado"}    

def list_hoteles(fecha_inicio: str, fecha_fin: str, ciudad: str):
    """Obtener información del paciente desde una API externa."""
    api_url = f"http://127.0.0.1:8000/api/hoteles/"
    payload = {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "ciudad": ciudad
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "error al obtener hoteles"}    

def book_hotel(document: str, email: str, name_hotel: str, name_client: str, date_init: str, date_end: str):
    """Reservar un hotel para un paciente."""
    api_url = "http://127.0.0.1:8000/api/book-hotel/"
    payload = {
        "document": document,
        "email": email,
        "name_hotel": name_hotel,
        "name_client": name_client,
        "date_init": date_init,
        "date_end": date_end
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return "Esta función aún no está implementada. Por favor, inténtelo más tarde."

def type_activities(*args, **kwargs):    
    api_url = "http://127.0.0.1:8000/api/get-activities/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return "Esta función aún no está implementada. Por favor, inténtelo más tarde."    

def get_variations(type: int):
    api_url = f"http://127.0.0.1:8000/api/get-variations/{type}/"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return "Esta función aún no está implementada. Por favor, inténtelo más tarde."

tools = [
    StructuredTool.from_function(
        func=get_paciente,
        name="get_paciente",
        description="Obtiene los datos del paciente a partir de su número de documento.",
        args_schema=GetPacientInput
    ),
    StructuredTool.from_function(
        func=list_hoteles,
        name="list_hoteles",
        description="Obtiene una lista de hoteles disponibles para una ciudad en un rango de fechas.",
        args_schema=ListHotelsInput
    ),
    StructuredTool.from_function(
        func=book_hotel,
        name="book_hotel",
        description="Reserva un hotel para un paciente.",
        args_schema=BookHotelInput
    ),
    Tool.from_function(
        func=type_activities,
        name="get_activities",
        description="Obtiene una lista de tipos de actividades recomendadas por el doctor."
    ),
    StructuredTool.from_function(
        func=get_variations,
        name="get_variations",
        description="Obtiene una lista de actividades recomendadas por el doctor para un tipo específico.",
        args_schema=TypeActivitiesInput
    )
]
