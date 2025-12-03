from quart import Blueprint, request, jsonify
from app.modules.student.profile.viewmodel import student_profile_viewmodel, ProfileError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.student.profile")

student_profile_bp = Blueprint("student_profile", __name__, url_prefix="/v2/student")

@student_profile_bp.route("/profile", methods=["POST"])
async def get_profile():
    """
    Fetch student profile using valid BMU session cookies.
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
        
        profile_data = await student_profile_viewmodel.fetch_student_profile(session_cookies)

        return jsonify({
            "success": True,
            "message": "Profile fetched successfully.",
            "data": profile_data.dict()
        }), 200

    except ProfileError as e:
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
        logger.error(f"Unexpected error in /profile: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
