import requests, pytz, json
from datetime import datetime, timedelta
from langchain.tools import Tool, StructuredTool
from .schemas import GetPacientInput, ServicesProfessionalInput, HoursInput, DataServiceInput, AppointmentDataInput
from .llm_config import llm
from langchain_core.prompts import PromptTemplate


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

    # Prompt para identificar el servicio primera vez o de seguimiento
    prompt = PromptTemplate.from_template(
        "Tenemos esto: '{api_response}'. Basado en esa información, "
        "si la especialidad del profesional es 'Medicina general' "
        "debes mostrar un servicio específico, el cual es 'consulta general'"
        "Devuelve únicamente ese servicio con su información sin explicaciones"
        "Si la especialidad del profesional es distinta a 'Medicina general' "
        "debes buscar dos servicios específicos,los cuales son 'primera vez' y 'seguimieto'"
        "Devuelve únicamente esos dos servicios con su información."
    )

    services = llm.invoke(prompt.format(api_response=response.text)).content.strip()
    print(f"SERVICIOS FILTRADOS: {services}")

    if response.status_code == 200:
        return services
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

def get_service_client(data):    
    """Busca el ID del servicio con IA y obtiene su ID para luego consultar la disponibilidad"""
    
    api_url = "http://127.0.0.1:8000/api/get-all-services/"
    response = requests.get(api_url)    
    print("REQUEST RESPONSE: ", response.json())

    services = response.json()  # Obtiene la lista de servicios
    service_list = ", ".join([s["nombre"] for s in services])  # Crear lista de nombres

    # Prompt para identificar el servicio correcto
    prompt = PromptTemplate.from_template(
        "Tenemos esto: '{data}'. Basado en esa información, "
        "determina cuál de los siguientes servicios mencionó: {service_list}. "
        "Devuelve únicamente el nombre exacto del servicio sin explicaciones."
    )

    # obtener nombre exacto del servicio con el modelo
    service_detected = llm.invoke(prompt.format(data=data, service_list=service_list)).content.strip()

    service_id = next((s["id"] for s in services if s["nombre"] == service_detected), None)

    if service_id is None:
        return {"error": "No se encontró el servicio. Por favor, verifica el nombre."}
    print("RESPUESTA DEL MODELO: ", service_detected, service_id)    

    return service_id, service_detected

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
        "fecha_cita": "",
        "hora_cita": "",
        "id_servicio": 0,
        "nombre_servicio": "",
        "id_profesional": 0,
        "profesional_first_name": "",
        "profesional_last_name": ""
    }
    return data

def build_appointment_payload(agent_json):    

    print(f"JSON DEL AGENTE: {agent_json}")
    
    id_service = agent_json.get("id_servicio")
    api_url = "http://127.0.0.1:8000/api/service/"
    payload = {
        "tipo": id_service
    }
    response = requests.post(api_url, json=payload)
    print(f"response: {response}")
    service = response.json()
    print(f"service : {service}")
    duracion = service[0]["duracion"]
    print(f"duracion: {duracion}")

    hora_cita = datetime.strptime(agent_json['hora_cita'], "%H:%M")
    print(f"HORA DE CITA: {hora_cita}")
    hora_inicio = hora_cita +  timedelta(hours=5)
    print(f"HORA DE INICIO: {hora_inicio.strftime('%H:%M')}")
    hora_fin = hora_inicio + timedelta(seconds=duracion)
    print(f"HORA DE FIN: {hora_fin.strftime('%H:%M')}")

    payload = {
        "cliente": {
            "Activo": 1,
            "ActividadEconomicaId": 496,
            "MunicipioId": 636,
            "DigitoVerificacion": 0,
            "Declarante": False,
            "Apellido1": agent_json.get("apellido", ""),
            "Apellido2": ".",
            "CorreoElectronico": agent_json.get("email", ""),
            "Direccion": "Sin dirección",
            "Id": 0,
            "ListaPrecioId": 0,
            "NoEliminado": True,
            "Nombre1": agent_json.get("nombre", ""),
            "Nombre2": ".",
            "Principal": False,
            "RazonSocial": ".",
            "RegimenTributarioId": 1,
            "ResponsabilidadFiscal": "O-99",
            "Retefuente": False,
            "TelefonoFax": 0,
            "TelefonoFijo": "0",
            "TelefonoMovil": agent_json.get("telefono", ""),
            "UltimaActualizacion": "2020-01-01",
            "numeroDocumento": agent_json.get("documento", ""),
            "personeriaTributariaId": 1,
            "tipoDocumentoId": 3
        },
        "inicio": f"{agent_json['fecha_cita']}T{hora_inicio.strftime('%H:%M')}:00.000Z",
        "fin": f"{agent_json['fecha_cita']}T{hora_fin.strftime('%H:%M')}:00.000Z",
        "metodo_pago": {
            "id": 4,
            "name": "Tarjeta débito"
        },
        "servicio": {
            "id": agent_json.get("id_servicio", ""),
            "servicio_nombre": agent_json.get("nombre_servicio"),
            "servicio_total_duracion": duracion
        },
        "tecnico": {
            "base_user_id": 0,
            "id": agent_json.get("id_profesional", ""),
            "tecnico_first_name": agent_json.get("profesional_first_name"),
            "tecnico_id": agent_json.get("id_profesional", ""),
            "tecnico_last_name": agent_json.get("profesional_last_name"),
            "tecnico_nombre": f"{agent_json.get("profesional_first_name")} {agent_json.get("profesional_last_name")}"
        }
    }
    return payload


def data_register(
        nombre: str,
        apellido: str,
        documento: str,
        telefono: str,
        email: str,
        fecha_cita: str,
        hora_cita: str,
        id_servicio: int,
        nombre_servicio: str,
        id_profesional: int,
        profesional_first_name: str,
        profesional_last_name: str
                ):
    
    json_data = {
        "nombre": nombre,
        "apellido": apellido,
        "documento": documento,
        "telefono": telefono,
        "email": email,
        "fecha_cita": fecha_cita,
        "hora_cita": hora_cita,
        "id_servicio": id_servicio,
        "nombre_servicio": nombre_servicio,
        "id_profesional": id_profesional,
        "profesional_first_name": profesional_first_name,
        "profesional_last_name": profesional_last_name
    }
    print(f"JSON DATA RECIBIDO: {json_data}")    

    api_url = f"http://127.0.0.1:8000/api/post-cita/"
    payload = build_appointment_payload(json_data)
    response = requests.post(api_url, json=payload)

    print(f"Request payload: {payload}")
    print(f"response: {response}, status: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error al registrar la cita"}    
    
    
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
    ),
    StructuredTool.from_function(
        name="get_service_client",
        func=get_service_client,
        description="Determina el servicio al cual se refiere el usuario basándose en su mensaje.",
        args_schema=DataServiceInput 
    ),
    StructuredTool.from_function(
        name="send_json",
        func=data_register,
        description="Recibe un json con la información de la cita para realizar el registro",
        args_schema=AppointmentDataInput
    )
]