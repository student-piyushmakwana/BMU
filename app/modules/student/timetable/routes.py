from quart import Blueprint, request, jsonify
from app.modules.student.timetable.viewmodel import student_timetable_viewmodel, TimetableError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.student.timetable")

student_timetable_bp = Blueprint("student_timetable", __name__, url_prefix="/v2/student")

@student_timetable_bp.route("/timetable", methods=["POST"])
async def get_timetable():
    """
    Fetch student's timetable.
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
        timetable_date = data.get("timetable_date")
        
        timetable_data = await student_timetable_viewmodel.fetch_student_timetable(session_cookies, timetable_date)

        return jsonify({
            "success": True,
            "message": "Timetable fetched successfully.",
            "data": timetable_data.dict()
        }), 200

    except TimetableError as e:
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
        logger.error(f"Unexpected error in /timetable: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
