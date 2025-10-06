import httpx  # for making HTTP requests
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

app = FastAPI(title="API Gateway")

# service registry
Services = {
    "auth": "http://auth_service:8001",
}

# JWT Configuration(should match auth service)
JWT_SECRET = "change-me"  # Use environment variable in production
JWT_ALGORITHM = "HS256"


def extract_service_from_path(path: str) -> tuple[str, str]:
    """
    Extract service name and remaining path from request.

    Examples:
        /auth/register -> ("auth", "/register")
        /users/profile -> ("users", "/profile")
    """
    parts = path.strip("/").split("/", 1)
    service = parts[0] if parts else None
    remaining_path = f"/{parts[1]}" if len(parts) > 1 else "/"
    return service, remaining_path


def verify_jwt(token: str) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(request: Request, path: str):
    """
    Main gateway endpoint that proxies requests to appropriate services.
    """
    service_name, service_path = extract_service_from_path(path)

    if service_name not in Services:
        raise HTTPException(status_code=404, detail="Internal server error")

    service_url = Services[service_name]
    target_url = f"{service_url}/auth{service_path}"

    # Get request body
    body = await request.body

    # Prepare headers
    headers = dict(request.headers)
    (headers.pop("host", None),)

    # JWT
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_jwt(token)
            headers["X-User_ID"] = str(payload.get("sub"))
            headers["X-User-Email"] = payload.get("email", "")
        except HTTPException:
            pass

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=request.url,
                content=body,
                headers=headers,
                params=request.query_params,
            )
            return response
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service unavailable: {e}",
            )


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "api-gateway"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
