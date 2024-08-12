import requests
from app import db
from app.models.country import Country

class CountryService:

    @staticmethod
    def load_countries():
        if Country.query.count() > 0:
            print("Los países ya están cargados en la base de datos.")
            return
        
        response = requests.get("https://restcountries.com/v3.1/all")
        
        if response.status_code == 200:
            countries_data = response.json()

            countries = sorted(countries_data, key=lambda x: x['name']['common'])

            for country in countries:
                name = country['name']['common']
                
                # Obtener el código del país (puede ser 'cca2', 'cca3', etc.)
                code = country.get("cca3", "UNKNOWN")  # Usando 'cca3' como código, o 'UNKNOWN' si no existe
                
                phone_code = ""
                if 'idd' in country:
                    if 'root' in country['idd'] and len(country['idd']['suffixes']) > 0:
                        phone_code = country['idd']['root'] + country['idd']['suffixes'][0]

                # Crear una nueva entrada de país con el código
                new_country = Country(name=name, code=code, phone_code=phone_code)
                db.session.add(new_country)

            db.session.commit()
            print("Países cargados exitosamente en la base de datos.")
        else:
            print("Error al cargar los países desde la API.")

    @staticmethod
    def get_all_countries():
        return Country.query.all()