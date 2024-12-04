from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from db import users_collection

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get('x-real-ip')
        print(f'Headers: {request.headers}')
        print(f'Origin: {origin}')
        data = await request.json()
        api_key = data['api_key']
        try:
            response = users_collection.find_one({'api_key': api_key})
            if origin in response['allowed_origins']:
                return await call_next(request)
            else:
                # Return a 403 response if the origin is not allowed
                response_content = {'detail': 'Origin not allowed'}
                return JSONResponse(content=response_content, status_code=403)
        except Exception as e:
            print(e)
            # Return a 401 response if the Authorization header is missing
            response_content = {'detail': 'Missing or invalid API keys'}
            return JSONResponse(content=response_content, status_code=401)
