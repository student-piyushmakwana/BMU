from quart import jsonify, make_response

async def error_response(message: str, status_code: int):
    """Return a standardized JSON error response."""
    return await make_response(jsonify({"success": False, "error": message}), status_code)

def clean_labelled_text(text: str) -> str:
    if not text:
        return ""
    return text.split(":", 1)[-1].strip()
