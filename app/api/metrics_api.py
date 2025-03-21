from flask import Blueprint, jsonify
from app import db  # Importamos la instancia de SQLAlchemy
from sqlalchemy import text  # Importamos text() para ejecutar consultas SQL

# Crear un Blueprint para métricas
metrics_bp = Blueprint('metrics_api', __name__)

@metrics_bp.route('/update-metrics', methods=['POST'])
def update_metrics():
    """Endpoint para actualizar la tabla metrics manualmente."""
    try:
        query = text("""
            INSERT INTO metrics (month, total_users, growth_percentage, viewed_offers, redeemed_offers, conversion_rate, category, published_offers_avg, available_coupons)
            SELECT 
                month_data.month AS month,
                COALESCE(users_data.total_users, 0) AS total_users,
                COALESCE(
                    (users_data.total_users - LAG(users_data.total_users) OVER (ORDER BY month_data.month)) / 
                    NULLIF(LAG(users_data.total_users) OVER (ORDER BY month_data.month), 0) * 100, 0
                ) AS growth_percentage,
                COALESCE(offers_data.viewed_offers, 0) AS viewed_offers,
                COALESCE(offers_data.redeemed_offers, 0) AS redeemed_offers,
                CASE 
                    WHEN COALESCE(offers_data.viewed_offers, 0) > 0 THEN 
                        (COALESCE(offers_data.redeemed_offers, 0) * 100.0) / COALESCE(offers_data.viewed_offers, 1)
                    ELSE 0
                END AS conversion_rate,
                COALESCE(category_data.name, 'Desconocido') AS category,
                COALESCE(category_offers_data.published_offers_avg, 0) AS published_offers_avg,
                COALESCE((SELECT SUM(p.available_quantity) FROM promotions p WHERE DATE_TRUNC('month', p.start_date) = month_data.month), 0) AS available_coupons
            FROM 
                (SELECT generate_series('2023-01-01'::date, CURRENT_DATE, '1 month') AS month) AS month_data
            LEFT JOIN (
                SELECT DATE_TRUNC('month', terms_accepted_at) AS month, COUNT(user_id) AS total_users
                FROM users
                WHERE terms_accepted_at IS NOT NULL
                GROUP BY month
            ) AS users_data
            ON month_data.month = users_data.month
            LEFT JOIN (
                SELECT DATE_TRUNC('month', p.start_date) AS month, 
                       COUNT(DISTINCT p.promotion_id) AS viewed_offers,
                       SUM(pc.quantity_consumed) AS redeemed_offers
                FROM promotions p
                LEFT JOIN promotion_consumed pc ON p.promotion_id = pc.promotion_id
                WHERE p.start_date IS NOT NULL
                GROUP BY month
            ) AS offers_data
            ON month_data.month = offers_data.month
            LEFT JOIN promotion_categories AS pc 
            ON pc.promotion_id = (
                SELECT p.promotion_id FROM promotions p 
                WHERE DATE_TRUNC('month', p.start_date) = month_data.month 
                LIMIT 1
            )
            LEFT JOIN categories AS category_data
            ON category_data.category_id = pc.category_id
            LEFT JOIN (
                SELECT DATE_TRUNC('month', p.start_date) AS month, 
                       c.name AS category, 
                       COUNT(p.promotion_id) / NULLIF(COUNT(DISTINCT p.partner_id), 0) AS published_offers_avg
                FROM promotions p
                JOIN promotion_categories pc ON p.promotion_id = pc.promotion_id
                JOIN categories c ON pc.category_id = c.category_id
                WHERE p.start_date IS NOT NULL
                GROUP BY month, c.name
            ) AS category_offers_data
            ON month_data.month = category_offers_data.month AND category_data.name = category_offers_data.category;
        """)
        
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
        query = text("SELECT * FROM metrics ORDER BY month DESC")
        result = db.session.execute(query)
        metrics = [dict(row) for row in result.mappings()]
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
