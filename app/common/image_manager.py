import base64
import io
from google.cloud import storage
from PIL import Image
import os
import google.auth
from config import Config

class ImageManager:
    def __init__(self):
        self.bucket_name = Config.GCS_BUCKET_NAME

        # Utiliza las credenciales desde Config.GOOGLE_CREDENTIALS
        # print("imprimiendo credenciales",Config.GOOGLE_CREDENTIALS)

        self.client = storage.Client.from_service_account_info(Config.GOOGLE_CREDENTIALS)

        self.bucket = self.client.get_bucket(self.bucket_name)

    def upload_image(self, image_base64, filename):
        # Decodificar la imagen desde base64
        try:
            image_data = base64.b64decode(image_base64)
        except Exception as e:
            raise ValueError("Failed to decode Base64 image data") from e
        
        # Verificar que los datos decodificados son una imagen válida
        try:
            image = Image.open(io.BytesIO(image_data))
            image.load()  # Carga la imagen en memoria completamente
        except Exception as e:
            raise ValueError("Decoded data is not a valid image file") from e

        # Redimensionar la imagen si es necesario
        resized_image = self.resize_image(image)

        # Subir la imagen redimensionada a Google Cloud Storage
        blob = self.bucket.blob(filename)
        output = io.BytesIO()
        resized_image.save(output, format='PNG')
        output.seek(0)
        blob.upload_from_file(output, content_type='image/png')

        # Hacer pública la imagen
        blob.make_public()

        # Devolver la URL pública de la imagen
        return blob.public_url

    def resize_image(self, image, max_size=(800, 800)):
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    def delete_image(self, filename):
        """Elimina una imagen del bucket de Google Cloud Storage"""
        blob = self.bucket.blob(filename)
        if blob.exists():
            blob.delete()
            return True
        else:
            return False

