from django.urls import path
from .views import AgentViewset, AgentDataset

urlpatterns = [   
    path('responder/', AgentViewset.as_view({'post': 'post'}), name='openai'),
    path('responder-ia/', AgentViewset.as_view({'post': 'responder'}), name='responder_ia'),
    path('webhook-ultra/', AgentViewset.as_view({'post': 'ultramsg_webhook'}), name='ultramsg_webhook'),
    path('pacientes/<int:document>/', AgentDataset.as_view({'get': 'list_clients'}), name='clients'),
    path('hoteles/', AgentDataset.as_view({'post': 'list_hoteles'}), name='list_hoteles'),
    path('book-hotel/', AgentDataset.as_view({'post': 'book_hotel'}), name='book_hotel'),
    path('get-activities/', AgentDataset.as_view({'get': 'list_type_activities'}), name='list_type_activities'),
    path('get-variations/<int:type>/', AgentDataset.as_view({'get': 'list_activities'}), name='list_activities'),
]
