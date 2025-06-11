from django.urls import path
from .views import AgentViewset, AgentDataset, AgentPrevired, AgentAuxTools


urlpatterns = [   
    # API endpoints for the virtual assistant surgeon
    path('responder/', AgentViewset.as_view({'post': 'post'}), name='openai'),
    path('responder-ia/', AgentViewset.as_view({'post': 'responder'}), name='responder_ia'),
    path('webhook/', AgentViewset.as_view({'post': 'ultramsg_webhook'})),
    path('pacientes/<int:document>/', AgentDataset.as_view({'get': 'list_clients'}), name='clients'),
    path('hoteles/', AgentDataset.as_view({'post': 'list_hoteles'}), name='list_hoteles'),
    path('book-hotel/', AgentDataset.as_view({'post': 'book_hotel'}), name='book_hotel'),
    path('get-activities/', AgentDataset.as_view({'get': 'list_type_activities'}), name='list_type_activities'),
    path('get-variations/<int:type>/', AgentDataset.as_view({'get': 'list_activities'}), name='list_activities'),
    path('activities-date/<int:type>/', AgentDataset.as_view({'get': 'get_activities_dates'}), name='get_activities_dates'),

    # API endpoints for the virtual assistant previred
    path('coberturas/', AgentPrevired.as_view({'get': 'get_coberturas'}), name='get_coberturas'),


    # API endpoints for the virtual assistant previred auxiliary tools
    path('professionals/', AgentAuxTools.as_view({'get': 'get_professionals'}), name='get_professionals'),
    path('services/<int:id_professional>/', AgentAuxTools.as_view({'get': 'get_services_professional'}), name='get_services_professional'),
    path('get-hours/', AgentAuxTools.as_view({'post': 'get_hours'}), name='get_hours'),
    path('get-all-services/', AgentAuxTools.as_view({'get': 'get_all_services'}), name='get_all_services'),
    path('post-cita/', AgentAuxTools.as_view({'post': 'post_appointment'}), name='post_appointment'),
    path('service/', AgentAuxTools.as_view({'post': 'get_service_id'}), name='get_service_id'),

]
