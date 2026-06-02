import cloudinary.uploader


class UploadService:

    @staticmethod
    def upload_image(file):
        result = cloudinary.uploader.upload(file.file)

        return result["secure_url"]
