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

        if not mensaje:
            return JsonResponse({'error': 'Falta el mensaje.'}, status=400)

        try:
            respuesta = responder_ia_langchain(mensaje)
            return JsonResponse({'respuesta': respuesta}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @action(detail=False, methods=['post'])    
    def ultramsg_webhook(self, request, *args, **kwargs):
        try:
            url_ngrok = os.getenv("URL_BASE_NGROK")
            print("URL de Ngrok:", url_ngrok)
            if not url_ngrok:
                return JsonResponse({'error': 'URL de Ngrok no configurada.'}, status=500)
            
            data = json.loads(request.body)
            print("Datos completos recibidos:", data)
            message_data = data.get('data', {})
            sender = message_data.get('from', '').replace('@c.us', '')
            print("Remitente:", sender)
            user_message = message_data.get('body', '')
            print("Usuario remitente:", user_message)
            
            if not user_message:
                return JsonResponse({'error': 'Falta el mensaje.'}, status=400)

            agent_api_url = url_ngrok + 'api/responder-ia/'
            payload = {'mensaje': user_message}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(agent_api_url, json=payload, headers=headers)
            print("Respuesta del agente:", response.json())

            if response.status_code != 200:
                return JsonResponse({'error': 'Error al procesar el mensaje del agente.'}, status=response.status_code)

            response_data = response.json()
            botreply = response_data.get('respuesta', '')
            print("Respuesta del bot:", botreply)

            ultramsg_url = os.getenv("URL_ULTRAMSG")
            ultramsg_token = os.getenv("ULTRAMSG_TOKEN")
            if not ultramsg_url or not ultramsg_token:
                return JsonResponse({'error': 'URL o token de UltraMsg no configurados.'}, status=500)
            ultramsg_payload = {
                'token': ultramsg_token,
                'to': sender,
                'body': botreply
            }
            ultramsg_response = requests.post(ultramsg_url, data=ultramsg_payload)
            print("Respuesta de UltraMsg:", ultramsg_response.json())
            if ultramsg_response.status_code != 200:
                return JsonResponse({'error': 'Error al enviar el mensaje a UltraMsg.'}, status=ultramsg_response.status_code)                    

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