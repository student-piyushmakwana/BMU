from quart import Blueprint, request, jsonify
from app.modules.student.dashboard.viewmodel import student_dashboard_viewmodel, DashboardError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.student.dashboard")

student_dashboard_bp = Blueprint("student_dashboard", __name__, url_prefix="/v2/student")

@student_dashboard_bp.route("/dashboard", methods=["POST"])
async def get_dashboard():
    """
    Fetch student dashboard using valid BMU session cookies.
    """
    try:
        data = await request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Request body must be valid JSON."
            }), 400

        if "session_cookies" not in data:
            return jsonify({
                "success": False,
                "message": "Missing 'session_cookies' in request body."
            }), 400

        session_cookies = data.get("session_cookies")
        
        dashboard_data = await student_dashboard_viewmodel.fetch_student_dashboard(session_cookies)

        return jsonify({
            "success": True,
            "message": "Dashboard fetched successfully.",
            "data": dashboard_data.dict()
        }), 200

    except DashboardError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 401

    except ExternalServiceError as e:
        logger.error(f"External service error: {e}")
        return jsonify({
            "success": False,
            "message": "External service unavailable.",
            "details": str(e)
        }), 502

    except Exception as e:
        logger.error(f"Unexpected error in /dashboard: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
