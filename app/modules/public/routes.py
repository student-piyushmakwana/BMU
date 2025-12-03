from quart import Blueprint, jsonify
from app.modules.public.viewmodel import public_viewmodel, PublicInfoError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.public")

public_bp = Blueprint("public", __name__, url_prefix="/v2/public")

@public_bp.route("/info", methods=["GET"])
async def get_public_info():
    """
    Fetch public information (events, news, testimonials).
    """
    try:
        data = await public_viewmodel.fetch_public_info()

        return jsonify({
            "success": True,
            "message": "Public information fetched successfully.",
            "data": data.dict()
        }), 200

    except PublicInfoError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except ExternalServiceError as e:
        logger.error(f"External service error: {e}")
        return jsonify({
            "success": False,
            "message": "External service unavailable.",
            "details": str(e)
        }), 502

    except Exception as e:
        logger.error(f"Unexpected error in /public/info: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
