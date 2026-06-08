import os
import cloudinary
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing env variable: {key}")
    return value

def to_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in ("true", "1", "yes", "on")

cloudinary.config(
    cloud_name=get_env("CLOUDINARY_CLOUD_NAME"),
    api_key=get_env("CLOUDINARY_API_KEY"),
    api_secret=get_env("CLOUDINARY_API_SECRET"),
    secure=to_bool(os.getenv("CLOUDINARY_SECURE"), True)
)
print("ENV CHECK:", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("Cloudinary configured")