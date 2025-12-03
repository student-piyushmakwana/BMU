from quart import Blueprint, jsonify, request
from app.modules.departments.viewmodel import departments_viewmodel, DepartmentsError, ExternalServiceError
import logging

logger = logging.getLogger("bmu.modules.departments")

departments_bp = Blueprint("departments", __name__, url_prefix="/v2")

@departments_bp.route("/departments", methods=["GET"])
async def get_all_departments():
    """
    Fetch list of all departments.
    """
    try:
        departments = await departments_viewmodel.get_all_departments()
        return jsonify({
            "success": True,
            "message": "Departments fetched successfully.",
            "data": departments
        }), 200
    except Exception as e:
        logger.error(f"Error fetching departments: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500

@departments_bp.route("/department/details", methods=["POST"])
async def get_department_details():
    """
    Fetch department details by BMU ID.
    Expects JSON body: { "bmu_id": <id> }
    """
    try:
        body = await request.get_json()
        if not body:
            return jsonify({"success": False, "message": "Request body is required"}), 400
            
        bmu_id = body.get("bmu_id")
        
        if not bmu_id:
             return jsonify({
                "success": False,
                "message": "bmu_id is required."
            }), 400

        # 1. Check if department exists in our DB
        department_doc = await departments_viewmodel.get_department_details(bmu_id)
        
        if not department_doc:
             return jsonify({
                "success": False,
                "message": "Department not found."
            }), 404

        # 2. Fetch from external source
        target_id = department_doc.get("bmu_id")
        if not target_id:
             return jsonify({
                "success": False,
                "message": "Invalid department configuration (missing ID)."
            }), 500

        institute_details = await departments_viewmodel.fetch_institute_details(target_id)
        
        # 3. Merge and return
        department_doc.update(institute_details.dict())
        if "_id" in department_doc:
            department_doc["_id"] = str(department_doc["_id"])

        return jsonify({
            "success": True,
            "message": "Department details fetched successfully (live).",
            "data": department_doc
        }), 200

    except DepartmentsError as e:
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
        logger.error(f"Unexpected error in /department/details: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error.",
            "details": str(e)
        }), 500
