from pydantic import BaseModel

class GetPacientInput(BaseModel):
    document: int

class ListHotelsInput(BaseModel):
    fecha_inicio: str
    fecha_fin: str
    ciudad: str

class BookHotelInput(BaseModel):
    document: str
    email: str
    name_hotel: str
    name_client: str
    date_init: str
    date_end: str

class TypeActivitiesInput(BaseModel):
    type: int

class ServicesProfessionalInput(BaseModel):
    id_professional: int

class HoursInput(BaseModel):
    id_professional: int
    date: str
    id_service: int