"""
File Storage Manager
"""
import os
import uuid
from typing import Optional
from fastapi import UploadFile
from app.config import settings
from app.utils.exceptions import ValidationError


class FileStorageManager:
    """
    Local file storage manager
    """

    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self._ensure_upload_dir()

    def _ensure_upload_dir(self):
        """Create upload directory if not exists"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir, exist_ok=True)

    def validate_file(self, file: UploadFile) -> None:
        """
        Validate uploaded file

        Args:
            file: Uploaded file

        Raises:
            ValidationError: If file is invalid
        """
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning

        if file_size > settings.MAX_FILE_SIZE:
            raise ValidationError(f"파일 크기는 {settings.MAX_FILE_SIZE / 1024 / 1024}MB 이하여야 합니다")

        # Check MIME type (simple check for image/*)
        if not file.content_type or not file.content_type.startswith("image/"):
            raise ValidationError("이미지 파일만 업로드 가능합니다")

    def save_file(self, file: UploadFile) -> str:
        """
        Save uploaded file

        Args:
            file: Uploaded file

        Returns:
            File URL

        Raises:
            ValidationError: If file is invalid
        """
        # Validate file
        self.validate_file(file)

        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Return URL
        return f"/uploads/menu-images/{unique_filename}"

    def delete_file(self, file_url: str) -> None:
        """
        Delete file

        Args:
            file_url: File URL
        """
        # Extract filename from URL
        filename = os.path.basename(file_url)
        file_path = os.path.join(self.upload_dir, filename)

        # Delete file if exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # Log error but don't raise
                print(f"Failed to delete file {file_path}: {e}")


# Global file storage instance
file_storage = FileStorageManager()
