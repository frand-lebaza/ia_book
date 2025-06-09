import requests, pytz
from datetime import datetime
from langchain.tools import Tool, StructuredTool
from .schemas import GetPacientInput, ServicesProfessionalInput, HoursInput

def get_user(document):
    """Obtener información del paciente desde una API externa."""
    api_url = f"http://127.0.0.1:8000/api/pacientes/{document}"
    response = requests.get(api_url)
    date = get_current_date()
    if response.status_code == 200:
        print(f"DATE ACTUAL: {date}")
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

def get_current_date(*args, **kwargs):
    try:
        zona_horaria = pytz.timezone('Etc/GMT+5')
        fecha_actual = datetime.now(zona_horaria)

        return {
            "current_date": fecha_actual.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"            
        }
    except Exception as e:
        print(f"Error al obtener la fecha actual: {e}")
        return None

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

def json_appointment(*args, **kwargs):
    data = {
        "nombre": "",
        "apellido": "",
        "documento": "",
        "telefono": "",
        "email": "",
        "fecha_inicio": "",
        "fecha_fin": "",
        "metodo_pago": {
            "id": 0,
            "name": ""
        },
        "servicio": {
            "id": 0,
            "servicio_nombre": "",
            "servicio_total_duracion": 0
        },
        "tecnico": {
            "base_user_id": 0,
            "id": 0,
            "tecnico_first_name": "",
            "tecnico_id": 0,
            "tecnico_last_name": "",
            "tecnico_nombre": ""
        }
    }
    return data

def info_appointment(data):
    return {
            "cliente":{
                "Activo": 1,
                "ActividadEconomicaId": 496,
                "MunicipioId": 636,
                "DigitoVerificacion": 0,
                "Declarante": False,
                "Apellido1": "", # llenar campo
                "Apellido2": ".",
                "CorreoElectronico": "", # llenar campo
                "Direccion": "Sin dirección",
                "Id": 0,
                "ListaPrecioId": 0,
                "NoEliminado": True,
                "Nombre1": "", # llenar campo
                "Nombre2": ".",
                "Principal": False,
                "RazonSocial": ".",
                "RegimenTributarioId": 1,
                "ResponsabilidadFiscal": "O-99",
                "Retefuente": False,
                "TelefonoFax": 0,
                "TelefonoFijo": "0",
                "TelefonoMovil": "", # llenar campo
                "UltimaActualizacion": "2020-01-01",
                "numeroDocumento": "", # llenar campo
                "personeriaTributariaId": 1,
                "tipoDocumentoId": 3
            },
            "inicio": "", # llenar campo 
            "fin": "", # llenar campo 
            "metodo_pago": {
                "id": 0, # llenar campo
                "name": "" # llenar campo
            },
            "servicio": {
                "id": 0, # llenar campo
                "servicio_nombre": "", # llenar campo
                "servicio_total_duracion": 0 # llenar campo
            },
            "tecnico": {
                "base_user_id": 0, # llenar campo
                "id": 0,# llenar campo
                "tecnico_first_name": "",
                "tecnico_id": 0, # llenar campo
                "tecnico_last_name": "", # llenar campo
                "tecnico_nombre": "" # llenar campo
            }
    }

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
    ),
    StructuredTool.from_function(
        name="get_hours",
        func=get_hours,
        description="Obtiene las horas disponibles de un profesional para una fecha y servicio específico.",
        args_schema=HoursInput
    ),
    Tool.from_function(
        name="get_current_date",
        func=get_current_date,
        description="Obtiene la fecha y hora actual en formato UTC."
    ),
    Tool.from_function(
        name="get_json_session",
        func=json_appointment,
        description="Devuelve un json con los datos del paciente y la cita que se va a agendar. Este json se va a ir llenando a medida que avanza la conversación. "
    )
]