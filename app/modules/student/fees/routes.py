from quart import Blueprint, request, jsonify
from app.modules.student.fees.viewmodel import student_fees_viewmodel, FeesError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.student.fees")

student_fees_bp = Blueprint("student_fees", __name__, url_prefix="/v2/student")

@student_fees_bp.route("/fees", methods=["POST"])
async def get_fee_history():
    """
    Fetch student's complete fee history.
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
        
        fee_data = await student_fees_viewmodel.fetch_fee_history(session_cookies)

        return jsonify({
            "success": True,
            "message": "Fee history fetched successfully.",
            "data": fee_data.dict()
        }), 200

    except FeesError as e:
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
        logger.error(f"Unexpected error in /fees: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_fees_bp.route("/fees/details", methods=["POST"])
async def get_fee_posting_details():
    """
    Fetch detailed fee posting information for a specific FeePostingID.
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
        fee_posting_id = data.get("fee_posting_id")

        if not fee_posting_id:
             return jsonify({
                "success": False,
                "message": "Missing 'fee_posting_id' in request body."
            }), 400
        
        posting_data = await student_fees_viewmodel.fetch_fee_posting_details(session_cookies, fee_posting_id)

        return jsonify({
            "success": True,
            "message": "Fee posting details fetched successfully.",
            "data": posting_data.dict()
        }), 200

    except FeesError as e:
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
        logger.error(f"Unexpected error in /fees/details: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_fees_bp.route("/fees/pending", methods=["POST"])
async def get_pending_fees():
    """
    Fetch pending fees.
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
        
        pending_data = await student_fees_viewmodel.fetch_pending_fees(session_cookies)

        return jsonify({
            "success": True,
            "message": "Pending fees fetched successfully.",
            "data": pending_data.dict()
        }), 200

    except FeesError as e:
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
        logger.error(f"Unexpected error in /fees/pending: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_fees_bp.route("/fees/pay", methods=["POST"])
async def initiate_payment():
    """
    Initiate fee payment.
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
        
        # We don't necessarily need the payment_info from the client if we rescrape,
        # but if we wanted to be more specific (e.g. paying specific amount), we'd need it.
        # For now, we assume "Pay Now" pays the default pending amount.
        
        payment_response = await student_fees_viewmodel.initiate_payment(session_cookies)

        return jsonify({
            "success": True,
            "message": payment_response.message,
            "data": payment_response.dict()
        }), 200

    except FeesError as e:
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
        logger.error(f"Unexpected error in /fees/pay: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@student_fees_bp.route("/fees/receipt", methods=["POST"])
async def download_receipt():
    """
    Download a fee receipt.
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
        
        receipt_identifier = data.get("receipt_identifier")
        if not receipt_identifier:
             return jsonify({
                "success": False,
                "message": "Missing 'receipt_identifier' in request body."
            }), 400

        session_cookies = data.get("session_cookies")
        
        file_content, filename = await student_fees_viewmodel.download_receipt(session_cookies, receipt_identifier)

        import base64
        base64_content = base64.b64encode(file_content).decode('utf-8')

        return jsonify({
            "success": True,
            "message": "Receipt downloaded successfully.",
            "data": {
                "filename": filename,
                "file_base64": base64_content,
                "content_type": "application/pdf"
            }
        }), 200

    except FeesError as e:
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
        logger.error(f"Unexpected error in /fees/receipt: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
