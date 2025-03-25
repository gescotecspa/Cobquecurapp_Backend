from flask import Blueprint, jsonify
from app import db  # Importamos la instancia de SQLAlchemy
from sqlalchemy import text  # Importamos text() para ejecutar consultas SQL

# Crear un Blueprint para métricas
metrics_bp = Blueprint('metrics_api', __name__)

@metrics_bp.route('/update-metrics', methods=['POST'])
def update_metrics():
    """Endpoint para actualizar la tabla metrics manualmente."""
    try:
        query = text("SELECT insert_metrics();")
        
        db.session.execute(query)
        db.session.commit()
        
        return jsonify({"message": "Métricas actualizadas correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@metrics_bp.route('', methods=['GET'])
def get_metrics():
    """Endpoint para obtener todas las métricas de la base de datos."""
    try:
        query = text("SELECT * FROM get_metrics()")
        result = db.session.execute(query)
        metrics = [dict(row) for row in result.mappings()]
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
