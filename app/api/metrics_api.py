from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

metrics_bp = Blueprint('metrics_api', __name__)

@metrics_bp.route('/update-metrics', methods=['POST'])
def update_all_metrics():
    """Actualiza todas las métricas desde la función insert_all_metrics()."""
    try:
        db.session.execute(text("SELECT public.insert_all_metrics();"))
        db.session.commit()
        return jsonify({"message": "Métricas actualizadas correctamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/growth', methods=['GET'])
def get_growth_metrics():
    """Devuelve métricas de crecimiento de usuarios (metrics_users)."""
    try:
        result = db.session.execute(text("SELECT * FROM metrics_users ORDER BY month"))
        data = [dict(row) for row in result.mappings()]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/conversion', methods=['GET'])
def get_conversion_metrics():
    """Devuelve métricas de conversión por categoría (metrics_promotions)."""
    try:
        result = db.session.execute(text("SELECT * FROM metrics_promotions ORDER BY published_percentage DESC"))
        data = [dict(row) for row in result.mappings()]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/activity', methods=['GET'])
def get_activity_metrics():
    """Devuelve métricas de actividad comercial (metrics_activity)."""
    try:
        result = db.session.execute(text("SELECT * FROM metrics_activity ORDER BY avg_promotions_per_active_partner DESC"))
        data = [dict(row) for row in result.mappings()]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
