from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .agents.agent_config import responder_ia_langchain
import json, os, requests
from langchain_core.messages import HumanMessage
from django.http.response import JsonResponse
from django.conf import settings

class AgentViewset(viewsets.GenericViewSet):
    def post(self, request):
        mensaje = request.data.get('mensaje')

        if not mensaje:
            return Response({'error': 'Falta el mensaje.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            respuesta = responder_openai(mensaje)
            return Response({'respuesta': respuesta}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'])
    def responder(self, request):
        mensaje = request.data.get('mensaje')
        # session_id = request.data.get('session_id')

        if not mensaje:
            return JsonResponse({'error': 'Falta el mensaje.'}, status=400)

        try:
            respuesta = responder_ia_langchain(mensaje)
            return JsonResponse({'respuesta': respuesta}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'])    
    def ultramsg_webhook(self, request):
        try:
            url_ngrok = os.getenv("URL_BASE_NGROK")            
            if not url_ngrok:
                return JsonResponse({'error': 'URL de Ngrok no configurada.'}, status=500)
            
            data = json.loads(request.body)
            print("Datos completos recibidos:", data)
            message_data = data.get('data', {})
            sender = message_data.get('from', '').replace('@c.us', '')
            # print("Remitente:", sender)
            user_message = message_data.get('body', '')
            # print("Usuario remitente:", user_message)
            
            # if not user_message:
            #     return JsonResponse({'error': 'Falta el mensaje.'}, status=400)

            # agent_api_url = url_ngrok + 'api/responder-ia/'
            # payload = {
            #     'mensaje': user_message,
            #     'session_id': sender,  # Usar el número de teléfono como ID de sesión
            #     }
            # print("Payload enviado al agente:", payload)
            # headers = {'Content-Type': 'application/json'}
            # response = requests.post(agent_api_url, json=payload, headers=headers)
            # print("Respuesta del agente:", response.json())
            # print("Código de estado de la respuesta del agente:", response.status_code)

            # if response.status_code != 200:
            #     return JsonResponse({'error': 'Error al procesar el mensaje del agente.'}, status=response.status_code)

            # response_data = response.json()
            # botreply = response_data.get('respuesta', '')
            # print("Respuesta del bot:", botreply)

            # ultramsg_url = os.getenv("URL_ULTRAMSG")
            # ultramsg_token = os.getenv("ULTRAMSG_TOKEN")
            # if not ultramsg_url or not ultramsg_token:
            #     return JsonResponse({'error': 'URL o token de UltraMsg no configurados.'}, status=500)
            # ultramsg_payload = {
            #     'token': ultramsg_token,
            #     'to': sender,
            #     'body': botreply
            # }
            # ultramsg_response = requests.post(ultramsg_url, data=ultramsg_payload)
            # print("Respuesta de UltraMsg:", ultramsg_response.json())
            # if ultramsg_response.status_code != 200:
            #     return JsonResponse({'error': 'Error al enviar el mensaje a UltraMsg.'}, status=ultramsg_response.status_code)                    

            # return JsonResponse({"to": sender, "body": user_message})
            return JsonResponse({"to": sender, "body": user_message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class AgentDataset(viewsets.GenericViewSet):
    """
    Clase para manejar datos del agente.    
    """
    def list_clients(self, request, document):
        print(f"Document ID: {document}")
        file_path = os.path.join(settings.BASE_DIR, 'asistente', 'agents', 'data_json/pacientes.json')
        with open(file_path, 'r') as file:
            data = json.load(file)

        paciente = next((item for item in data if item['num_document'] == document), None)
        if not paciente:
            return Response({"error": "Paciente no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(paciente, status=status.HTTP_200_OK)
    
    def list_hoteles(self, request): 
        data = request.data
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        ciudad = data.get('ciudad')
        print(f"Ciudad: {ciudad}")
        print(f"Fecha Inicio: {fecha_inicio}, Fecha Fin: {fecha_fin}")
    
        file_path = os.path.join(settings.BASE_DIR, 'asistente', 'agents', 'data_json/hoteles.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
                
        return Response(data, status=status.HTTP_200_OK)
    
    def book_hotel(self, request):
        data = request.data
        document = data.get('document')
        email = data.get('email')
        name_hotel = data.get('name_hotel')
        name_client = data.get('name_client')
        date_init = data.get('date_init')
        date_end = data.get('date_end')

        print(f"Document: {document}")
        print(f"Email: {email}")
        print(f"Hotel Name: {name_hotel}")
        print(f"Client Name: {name_client}")
        print(f"Date Init: {date_init}")
        print(f"Date End: {date_end}")

        if not all([document, email, name_hotel, name_client, date_init, date_end]):
            return Response({"error": "Faltan datos para realizar la reserva."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            "num_reserva": 1002,
            "tipo_habitacion": "",
            "nombre_hotel": name_hotel,
            "nombre_cliente": name_client,
            "num_document": document,
            "email": email,
            "fecha_inicio": date_init,
            "fecha_fin": date_end
        }

        # implementar la lógica para guardar la reserva en una base de datos
        
        return Response({"data": data}, status=status.HTTP_200_OK)
    
    def list_type_activities(*args, **kwargs):
        """
        Método para listar los tipos de actividades.
        """
        file_path = os.path.join(settings.BASE_DIR, 'asistente', 'agents', 'data_json/type_activities.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return Response(data, status=status.HTTP_200_OK)
    
    def list_activities(self, request, type):
        """
        Método para listar las actividades.
        """
        print(f"Tipo de actividad: {type}")
        if not type:
            return Response({"error": "Falta el tipo de actividad."}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = os.path.join(settings.BASE_DIR, 'asistente', 'agents', 'data_json/activities.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        activities = [data for data in data if data['id_type'] == type]
        if not activities:
            return Response({"error": "No se encontraron actividades para el tipo especificado."}, status=status.HTTP_404_NOT_FOUND)
        print(f"Actividades encontradas: {activities}")
        
        return Response(activities, status=status.HTTP_200_OK)
    
    def get_activities_dates(self, request, type):
        """
        Método para obtener actividades disponibles en fechas específicas.
        """

        data = request.data
        dates = data.get('dates', [])

        print(f"Tipo de actividad: {type}, Fechas: {dates}")
        if not type or not dates:
            return Response({"error": "Faltan datos para obtener actividades."}, status=status.HTTP_400_BAD_REQUEST)
        
        file_path = os.path.join(settings.BASE_DIR, 'asistente', 'agents', 'data_json/activities_price.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        activities = [activity for activity in data if activity['id_type'] == type and activity['fecha'] in dates]
        if not activities:
            return Response({"error": "No se encontraron actividades disponibles para las fechas especificadas."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(activities, status=status.HTTP_200_OK)
    
class AgentPrevired(viewsets.GenericViewSet):

    def get_coberturas(*args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'asistente', 'agents', 'data_json/cities.json')
        with open(file_path, 'r') as file:
            data = json.load(file)                    
        
        return Response(data, status=status.HTTP_200_OK)
    
class AgentAuxTools(viewsets.GenericViewSet):

    def get_professionals(*args, **kwargs):
        """ 
        Obtiene la lista de los profesionales disponibles
        """
        api_base = os.getenv("URL_BASE")
        api_url = f"{api_base}/api/1.0/cda/tecnico/?expand=categoria_tecnicos"

        response = requests.get(api_url)
        if response.status_code != 200:
            return {"Error": "No se pudo obtener la lista de profesionales."}
        data = response.json()
        if not data:
            return {"Error": "No hay profesionales disponibles en este momento."}
        
        data_professional = data["results"]

        extract_data = [
            {
                "id": professional["id"],
                "nombre_completo": professional["nombre_completo"],
                "especialidad": professional["categoria_tecnicos"]["name"]                
            }
            for professional in data_professional
        ]                                 

        return Response(extract_data, status=200)
    
    def get_services_professional(self, request, id_professional):
        """
        Obtiene los servicios disponibles para un profesional específico.        
        """
        api_base = os.getenv("URL_BASE")
        api_url = f"{api_base}/api/1.0/cda/public_list/servicios/0/?tecnico={id_professional}"

        response = requests.get(api_url)
        if response.status_code != 200:
            return {"Error": "No se pudo obtener la lista de servicios."}
        
        data = response.json()
        if not data:
            return {"Error": "No hay servicios disponibles en este momento."}                                                 

        return Response(data, status=200)
    
    def get_hours(self, request):
        """
        Obtiene las horas disponibles para agendar una cita.
        """
        data = request.data
        startdate = data.get('startdate')
        tecnico_id = data.get('tecnicos_id')
        servicio_id = data.get('tipo')
        print(f"Fecha de inicio: {startdate}")
        print(f"Técnico ID: {tecnico_id}")
        print(f"Servicio ID: {servicio_id}")
        if not all([startdate, tecnico_id, servicio_id]):
            return Response({"error": "Faltan datos para obtener las horas disponibles."}, status=status.HTTP_400_BAD_REQUEST)
        api_base = os.getenv("URL_BASE")
        api_url = f"{api_base}/api/1.0/cda/public-calendar/servicio_dates/"
        payload = {
            "startdate": startdate,
            "tecnicos_id": [tecnico_id],
            "tipo": [servicio_id]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=payload, headers=headers)        

        if response.status_code != 200:
            return Response({"error": "No se pudo obtener las horas disponibles."}, status=response.status_code)
        data = response.json()
        horas = data[0]["horas_disponibles"]

        if not horas:
            return Response({"error": "No hay horas disponibles en este momento."}, status=status.HTTP_404_NOT_FOUND)
        return Response(horas, status=status.HTTP_200_OK)
