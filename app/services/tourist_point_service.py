from app.models import TouristPoint, Image, Rating
from app import db

def create_tourist_point(data):
    tourist_point = TouristPoint(
        title=data['title'],
        description=data.get('description'),
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    
    db.session.add(tourist_point)
    db.session.commit()
    
    # Agregar imágenes si se proporcionan
    if 'images' in data:
        for image_path in data['images']:
            image = Image(image_path=image_path, tourist_point_id=tourist_point.id)
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
    
    # Eliminar todas las imágenes existentes
    Image.query.filter_by(tourist_point_id=tourist_point_id).delete()
    
    # Agregar nuevas imágenes
    if 'images' in data:
        for image_path in data['images']:
            image = Image(image_path=image_path, tourist_point_id=tourist_point_id)
            db.session.add(image)
    
    db.session.commit()
    return tourist_point.serialize()

def get_all_tourist_points():
    tourist_points = TouristPoint.query.all()
    return [tp.serialize() for tp in tourist_points]


def get_tourist_point_by_id(tourist_point_id):
    tourist_point = TouristPoint.query.get(tourist_point_id)
    return tourist_point.serialize() if tourist_point else None

def add_image(tourist_point_id, image_path):
    image = Image(image_path=image_path, tourist_point_id=tourist_point_id)
    db.session.add(image)
    db.session.commit()
    return image.serialize()  # Devuelve el resultado serializado
def add_rating(tourist_point_id, tourist_id, rating, comment=None):
    # Verificar si el turista ya ha calificado este punto turístico
    existing_rating = Rating.query.filter_by(
        tourist_point_id=tourist_point_id,
        tourist_id=tourist_id
    ).first()
    
    if existing_rating:
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