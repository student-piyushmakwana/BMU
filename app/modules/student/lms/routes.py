from quart import Blueprint, request, jsonify
from app.modules.student.lms.viewmodel import student_lms_viewmodel, LMSError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.student.lms")

student_lms_bp = Blueprint("student_lms", __name__, url_prefix="/v2/student")

@student_lms_bp.route("/lms", methods=["POST"])
async def get_lms_dashboard():
    """
    Fetch LMS dashboard.
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
        semester = data.get("semester")
        
        dashboard_data = await student_lms_viewmodel.fetch_lms_dashboard(session_cookies, semester)

        return jsonify({
            "success": True,
            "message": "LMS dashboard fetched successfully.",
            "data": dashboard_data.dict()
        }), 200

    except ExternalServiceError as e:
        logger.error(f"External service error: {e}")
        return jsonify({
            "success": False,
            "message": "External service unavailable.",
            "details": str(e)
        }), 502

    except LMSError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 401

    except Exception as e:
        logger.error(f"Unexpected error in /lms: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_lms_bp.route("/lms/subject", methods=["POST"])
async def get_lms_subject_details():
    """
    Fetch detailed LMS information for a single subject.
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
        path = data.get("path")

        if not path:
             return jsonify({
                "success": False,
                "message": "Missing 'path' in request body."
            }), 400
        
        subject_data = await student_lms_viewmodel.fetch_lms_subject_details(session_cookies, path)

        return jsonify({
            "success": True,
            "message": "Subject details fetched successfully.",
            "data": subject_data.dict()
        }), 200

    except LMSError as e:
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
        logger.error(f"Unexpected error in /lms/subject: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_lms_bp.route("/lms/pdf", methods=["POST"])
async def get_lms_pdf():
    """
    Fetch PDF via postback.
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
        postback_id = data.get("postback_id")
        form_action = data.get("form_action")

        if not postback_id or not form_action:
             return jsonify({
                "success": False,
                "message": "Missing 'postback_id' or 'form_action' in request body."
            }), 400
        
        pdf_response = await student_lms_viewmodel.fetch_pdf_via_postback(session_cookies, postback_id, form_action)

        return jsonify({
            "success": True,
            "message": "PDF fetched successfully.",
            "data": pdf_response.dict()
        }), 200

    except LMSError as e:
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
        logger.error(f"Unexpected error in /lms/pdf: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_lms_bp.route("/lms/rating", methods=["POST"])
async def submit_lms_rating():
    """
    Submit a rating for an LMS content item.
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
        path = data.get("path")
        postback_id = data.get("postback_id")

        if not path or not postback_id:
             return jsonify({
                "success": False,
                "message": "Missing 'path' or 'postback_id' in request body."
            }), 400
        
        success = await student_lms_viewmodel.submit_rating(session_cookies, path, postback_id)

        if success:
            return jsonify({
                "success": True,
                "message": "Rating submitted successfully."
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to submit rating."
            }), 500

    except LMSError as e:
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
        logger.error(f"Unexpected error in /lms/rating: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
