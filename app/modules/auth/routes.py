from quart import Blueprint, request, jsonify
from app.modules.auth.viewmodel import auth_viewmodel, AuthError, AuthenticationError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.auth")

auth_bp = Blueprint("auth", __name__, url_prefix="/v2/auth")

@auth_bp.route("/login", methods=["POST"])
async def login():
    """
    Main login endpoint for BMU portal.
    """
    try:
        data = await request.get_json()
        if not data:
             return jsonify({
                "success": False,
                "message": "Request body must be valid JSON."
            }), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Missing required fields: 'username' and 'password'."
            }), 400

        logger.info(f"[BMU] /login called for user: {username}")

        result = await auth_viewmodel.login_with_credentials(username, password)
        
        return jsonify({
            "success": True,
            "message": "Login successful.",
            "data": result
        }), 200

    except AuthenticationError as e:
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
        logger.error(f"Unexpected error in /login: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@auth_bp.route("/google", methods=["POST", "PUT"])
async def google_auth():
    """
    Handle Google Login and Account Linking.
    """
    try:
        data = await request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Request body must be valid JSON."
            }), 400

        google_id = data.get("google_id")
        if not google_id:
            return jsonify({
                "success": False,
                "message": "Missing required field: 'google_id'."
            }), 400

        username = data.get("username")
        password = data.get("password")

        if request.method == "PUT" and (not username or not password):
             return jsonify({
                "success": False,
                "message": "Missing 'username' or 'password' for account linking."
            }), 400

        logger.info(f"[BMU] /google ({request.method}) called for google_id: {google_id}")

        result = await auth_viewmodel.google_login(google_id, username, password)

        return jsonify({
            "success": True,
            "message": "Google login successful.",
            "data": result
        }), 200

    except AuthError as e:
        if e.code in ["ACCOUNT_CREATED_NEEDS_LINKING", "ACCOUNT_NEEDS_LINKING", "ACCOUNT_ALREADY_LINKED"]:
            return jsonify({
                "success": True,
                "message": str(e),
                "code": e.code
            }), 200

        return jsonify({
            "success": False,
            "message": str(e),
            "error_code": e.code
        }), 401

    except Exception as e:
        logger.error(f"Unexpected error in /google: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@auth_bp.route("/session/validate", methods=["POST"])
async def validate_session():
    """
    Verify if the provided BMU session cookies are still valid.
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
        valid = await auth_viewmodel.check_student_session(session_cookies)

        return jsonify({
            "success": True,
            "message": "Session check completed.",
            "data": {
                "isSessionValid": valid
            }
        }), 200

    except Exception as e:
        logger.error(f"Unexpected error in /session/validate: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@auth_bp.route("/logout", methods=["POST"])
async def logout():
    """
    Logout from BMU portal.
    """
    try:
        data = await request.get_json()
        if not data or "session_cookies" not in data:
            return jsonify({
                "success": False,
                "message": "Missing 'session_cookies' in request body."
            }), 400

        session_cookies = data.get("session_cookies")
        await auth_viewmodel.logout(session_cookies)

        return jsonify({
            "success": True,
            "message": "Logout successful."
        }), 200

    except AuthenticationError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 401

    except ExternalServiceError as e:
        return jsonify({
            "success": False,
            "message": "Logout failed.",
            "details": str(e)
        }), 502

    except Exception as e:
        logger.error(f"Unexpected error in /logout: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
