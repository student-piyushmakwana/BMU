from quart import Blueprint, request, jsonify
from app.modules.student.attendance.viewmodel import student_attendance_viewmodel, AttendanceError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.student.attendance")

student_attendance_bp = Blueprint("student_attendance", __name__, url_prefix="/v2/student")

@student_attendance_bp.route("/attendance", methods=["POST"])
async def get_attendance():
    """
    Fetch student attendance summary.
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
        
        attendance_data = await student_attendance_viewmodel.fetch_student_attendance(session_cookies)

        return jsonify({
            "success": True,
            "message": "Attendance fetched successfully.",
            "data": attendance_data.dict()
        }), 200

    except AttendanceError as e:
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
        logger.error(f"Unexpected error in /attendance: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_attendance_bp.route("/attendance/absent", methods=["POST"])
async def get_absent_days():
    """
    Fetch student's absent-day details for the given semester.
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
        selected_semester = data.get("selected_semester", "")
        
        absent_data = await student_attendance_viewmodel.fetch_absent_days(session_cookies, selected_semester)

        return jsonify({
            "success": True,
            "message": "Absent days fetched successfully.",
            "data": absent_data.dict()
        }), 200

    except AttendanceError as e:
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
        logger.error(f"Unexpected error in /attendance/absent: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_attendance_bp.route("/attendance/date", methods=["POST"])
async def get_attendance_by_date():
    """
    Fetch detailed attendance records for a specific date.
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
        attendance_date = data.get("attendance_date")

        if not attendance_date:
             return jsonify({
                "success": False,
                "message": "Missing 'attendance_date' in request body."
            }), 400
        
        date_data = await student_attendance_viewmodel.fetch_attendance_by_date(session_cookies, attendance_date)

        return jsonify({
            "success": True,
            "message": "Attendance details fetched successfully.",
            "data": date_data.dict()
        }), 200

    except AttendanceError as e:
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
        logger.error(f"Unexpected error in /attendance/date: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
