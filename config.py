class Config:
    SECRET_KEY = 'tu_llave_secreta'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:javiMono1981@localhost:5432/AppTurismo_DB'
    
    # NEON conexion
    SQLALCHEMY_DATABASE_URI = 'postgresql://AppTurismo_DB_owner:v9GxYRWcKw7j@ep-soft-tree-a5w6w6eq.us-east-2.aws.neon.tech/AppTurismo_DB?sslmode=require'
    
    # Configuración de SMTP
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'oaxacaappedidos@gmail.com'
    SMTP_PASSWORD = 'ikhy geej xvca byjt'
    SMTP_DEFAULT_SENDER = 'oaxacaappedidos@gmail.com'
    
    