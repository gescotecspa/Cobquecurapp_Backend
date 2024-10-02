from app.models import TouristPoint, Image, Rating, Status
from app import db
from ..common.image_manager import ImageManager
from config import Config

def create_tourist_point(data):
    # print("data recibida al crear punto",data)
    active_status = Status.query.filter_by(name="active").first()
    if not active_status:
        print("El estado 'active' no está disponible.")
        return None
    tourist_point = TouristPoint(
        title=data['title'],
        description=data.get('description'),
        latitude=data['latitude'],
        longitude=data['longitude'],
        status_id=active_status.id
    )
    
    db.session.add(tourist_point)
    db.session.commit()
    
    # Agregar imágenes si se proporcionan
    if 'images' in data:
        image_manager = ImageManager()
        for image_data in data['images']:
            filename = f"tourist_points/{tourist_point.id}/{image_data['filename']}"
            image_url = image_manager.upload_image(image_data['data'], filename)
            print(image_url, tourist_point.id)
            image = Image(image_path=image_url, tourist_point_id=tourist_point.id)
            db.session.add(image)
    
    db.session.commit()
    return tourist_point

def update_tourist_point(tourist_point_id, data):
    tourist_point = TouristPoint.query.get(tourist_point_id)
    
    if not tourist_point:
        return None
    
    # Actualizar los campos del punto turístico
    tourist_point.title = data.get('title', tourist_point.title)
    tourist_point.description = data.get('description', tourist_point.description)
    tourist_point.latitude = data.get('latitude', tourist_point.latitude)
    tourist_point.longitude = data.get('longitude', tourist_point.longitude)
        
    # Agregar nuevas imágenes
    if 'images' in data:
        image_manager = ImageManager()
        for image_data in data['images']:
            filename = f"tourist_points/{tourist_point.id}/{image_data['filename']}"
            image_url = image_manager.upload_image(image_data['data'], filename)
            image = Image(image_path=image_url, tourist_point_id=tourist_point_id)
            db.session.add(image)
    
    db.session.commit()
    return tourist_point.serialize()

def get_all_tourist_points():
    tourist_points = TouristPoint.query.all()
    return [tp.serialize() for tp in tourist_points]

def get_tourist_point_by_id(tourist_point_id):
    tourist_point = TouristPoint.query.get(tourist_point_id)
    return tourist_point.serialize() if tourist_point else None

def add_image(tourist_point_id, image_data):
    image_manager = ImageManager()
    filename = f"tourist_points/{tourist_point_id}/{image_data['filename']}"
    image_url = image_manager.upload_image(image_data['data'], filename)
    
    image = Image(image_path=image_url, tourist_point_id=tourist_point_id)
    db.session.add(image)
    db.session.commit()
    return image.serialize()  # Devuelve el resultado serializado

def add_rating(tourist_point_id, tourist_id, rating, comment=None):
    # Verificar si el turista ya ha calificado este punto turístico
    existing_rating = Rating.query.filter_by(
        tourist_point_id=tourist_point_id,
        tourist_id=tourist_id
    ).first()
    
    if (existing_rating):
        return {'message': 'You have already rated this tourist point'}, 400  
    
    # Crear la nueva calificación
    new_rating = Rating(
        tourist_point_id=tourist_point_id,
        tourist_id=tourist_id,
        rating=rating,
        comment=comment
    )
    db.session.add(new_rating)
    db.session.commit()
    
    return new_rating.serialize()

def delete_rating(rating_id):
    rating = Rating.query.get(rating_id)
    if not rating:
        return None
    db.session.delete(rating)
    db.session.commit()
    return True

def update_rating(rating_id, data):
    rating = Rating.query.get(rating_id)
    if not rating:
        return None

    rating.rating = data.get('rating', rating.rating)
    rating.comment = data.get('comment', rating.comment)
    db.session.commit()
    return rating.serialize()

def get_average_rating(tourist_point_id):
    ratings = Rating.query.filter_by(tourist_point_id=tourist_point_id).all()
    if not ratings:
        return {'average_rating': 'No ratings yet'}
    avg_rating = sum(r.rating for r in ratings) / len(ratings)
    return {'average_rating': avg_rating}

def get_ratings_by_tourist_point(tourist_point_id):
    return Rating.query.filter_by(tourist_point_id=tourist_point_id).all()

def delete_images(image_ids):
    image_manager = ImageManager()
    
    try:
        # Busca todas las imágenes por su ID
        images_to_delete = Image.query.filter(Image.id.in_(image_ids)).all()

        if not images_to_delete:
            return None

        # Elimina las imágenes del bucket y de la base de datos
        for image in images_to_delete:
            # Extrae la ruta completa desde la URL de la imagen
            file_path = image.image_path # Ajusta según el campo que uses en el modelo
            relative_path = file_path.split(f"{Config.GCS_BUCKET_NAME}/")[1]  # Obtener la ruta relativa (sin el primer "/")
            # print(relative_path)
            # file_path ahora contiene 'tourist_points/28/LOGOASOCIADOS.png', por ejemplo
            success = image_manager.delete_image(relative_path)  # Pasa la ruta relativa correcta
            if not success:
                print(f"Failed to delete image: {file_path}")

            # Elimina la entrada en la base de datos
            db.session.delete(image)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting images: {e}")
        return False

def delete_tourist_point(tourist_point_id):
    tourist_point = TouristPoint.query.get(tourist_point_id)
    
    if not tourist_point:
        return None

    # Cambiar el estado del punto turístico a "deleted"
    deleted_status = Status.query.filter_by(name='deleted').first()
    if deleted_status:
        tourist_point.status_id = deleted_status.id
        db.session.commit()
        return tourist_point.serialize()
    
    return None    