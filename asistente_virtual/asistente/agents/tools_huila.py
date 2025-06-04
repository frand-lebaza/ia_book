from langchain.tools import Tool

def obtener_hoteles_huila(ciudad):    
    hoteles = {
        "Neiva": ["Hotel Neiva Plaza", "Hotel Chicalá"],
        "San Agustín": ["Hotel San Agustín Internacional", "Hotel Monasterio"],
        "Pitalito": ["Hotel Kahve"]
    }
    if ciudad and ciudad in hoteles:
        return hoteles[ciudad]
    return sum(hoteles.values(), [])

def obtener_sitios_turisticos_huila(ciudad):
    sitios = {
        "Neiva": ["Parque Isla", "Malecón del Río Magdalena", "Museo Arqueológico Regional"],
        "San Agustín": ["Parque Arqueológico de San Agustín", "Alto de los Ídolos"],
        "Pitalito": ["Parque Principal Pitalito", "Sendero Ecológico El Salto"]
    }
    if ciudad and ciudad in sitios:
        return sitios[ciudad]
    return sum(sitios.values(), [])

def obtener_restaurantes_huila(ciudad):
    restaurantes = {
        "Neiva": ["Restaurante La Casa del Río", "El Solar", "El Asador del Huila"],
        "San Agustín": ["Fogón Andino", "El Balcón de San Agustín"],
        "Pitalito": ["Sabores del Laboyano", "La Parrilla de Pitalito"]
    }
    if ciudad and ciudad in restaurantes:
        return restaurantes[ciudad]
    return sum(restaurantes.values(), [])

def obtener_lugares_recuperacion_huila(ciudad):
    lugares = {
        "Neiva": ["Hotel Pacandé Spa & Wellness", "Hospedaje Los Arrayanes"],
        "San Agustín": ["Hotel Monasterio San Agustín", "Finca La Herencia"],
        "Pitalito": ["EcoHotel El Encanto", "Casa Campestre Oasis"]
    }
    if ciudad and ciudad in lugares:
        return lugares[ciudad]
    return sum(lugares.values(), [])

def obtener_servicios_esteticos_huila(ciudad=None):
    servicios = {
        "Neiva": ["Limpieza facial profunda", "Relleno de labios", "Tratamiento de acné", "Depilación láser"],
        "San Agustín": ["Masajes relajantes", "Microblading de cejas"],
        "Pitalito": ["Peeling químico", "Planchado de cejas"]
    }
    if ciudad and ciudad in servicios:
        return servicios[ciudad]
    return sum(servicios.values(), [])

def obtener_servicios_medicos_huila(ciudad=None):
    servicios = {
        "Neiva": ["Cirugía plástica facial", "Liposucción", "Rinoplastia", "Consulta de medicina general"],
        "San Agustín": ["Consulta de medicina alternativa", "Terapias de relajación"],
        "Pitalito": ["Control de peso", "Chequeo médico general"]
    }
    if ciudad and ciudad in servicios:
        return servicios[ciudad]
    return sum(servicios.values(), [])

tools = [
    Tool(
        name="obtener_hoteles_huila",
        func=obtener_hoteles_huila,
        description="Obtiene una lista de hoteles recomendados en el Huila. Recibe un parámetro opcional 'ciudad' para filtrar los resultados"
    ),
    Tool(
        name="obtener_sitios_turisticos_huila",
        func=obtener_sitios_turisticos_huila,
        description="Obtiene una lista de sitios turísticos recomendados en el Huila."
    ),
    Tool(
        name="obtener_restaurantes_huila",
        func=obtener_restaurantes_huila,
        description="Obtiene una lista de restaurantes recomendados en el Huila."
    ),
    Tool(
        name="obtener_lugares_recuperacion_huila",
        func=obtener_lugares_recuperacion_huila,
        description="Obtiene una lista de lugares recomendados para la recuperación en el Huila."
    ),
    Tool(
        name="obtener_servicios_esteticos_huila",
        func=obtener_servicios_esteticos_huila,
        description="Obtiene una lista de servicios estéticos disponibles en el Huila. Puede recibir un parámetro opcional 'ciudad' para filtrar los resultados."
    ),
    Tool(
        name="obtener_servicios_medicos_huila",
        func=obtener_servicios_medicos_huila,
        description="Obtiene una lista de servicios médicos disponibles en el Huila. Puede recibir un parámetro opcional 'ciudad' para filtrar los resultados."
    )
]