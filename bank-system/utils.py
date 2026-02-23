from typing import Dict, Any

def create_response(success: bool, message: str, data: Any = None, status_code: int = 200) -> Dict[str, Any]:
    """Create a standardized response format"""
    response = {
        "success": success,
        "message": message,
        "status_code": status_code
    }
    if data is not None:
        response["data"] = data
    return response