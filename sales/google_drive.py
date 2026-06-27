"""
sales/google_drive.py

Google Drive integration service for Credo ERP.

Provides a high-level interface for authenticating with Google Drive via a
service account, managing folder hierarchies, and uploading PDF documents
with automatic deduplication.
"""

import io
import logging
import re
from datetime import datetime

from django.conf import settings


from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError


from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from sales.google_credentials import ensure_google_credentials

logger = logging.getLogger(__name__)

DRIVE_SCOPE = [
    "https://www.googleapis.com/auth/drive"
]

# Canonical document-type folder names.
# Use these keys when calling upload_document() to avoid spelling mistakes.
#
# Example:
#     document_type=DOCUMENT_TYPES["invoice"]
DOCUMENT_TYPES: dict[str, str] = {
    "invoice": "Invoices",
    "quotation": "Quotations",
    "receipt": "Receipts",
    "lpo": "LPO",
}


class GoogleDriveService:
    """
    Service class for interacting with Google Drive API v3.

    Authenticates using a service account and provides methods for managing
    folders and uploading PDF documents within a structured folder hierarchy.

    Attributes:
        service: Authenticated Google Drive API service instance.

    Example:
        >>> drive = GoogleDriveService()
        >>> result = drive.upload_document(
        ...     customer_name="Acme Corp",
        ...     document_type="Invoices",
        ...     file_name="INV-001.pdf",
        ...     pdf_bytes=b"...",
        ...     year=2026,
        ... )
    """

    def __init__(self) -> None:
        ensure_google_credentials()
        try:
            credentials = Credentials.from_authorized_user_file(
                settings.GOOGLE_TOKEN_FILE,
                scopes=DRIVE_SCOPE,
            )

            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

                with open(settings.GOOGLE_TOKEN_FILE, "w") as token:
                    token.write(credentials.to_json())

            self.service = build(
                "drive",
                "v3",
                credentials=credentials,
                cache_discovery=False,
            )

            logger.info("Google Drive service initialised successfully.")

        except FileNotFoundError:
            logger.error(
                "OAuth token file not found: %s",
                settings.GOOGLE_TOKEN_FILE,
            )
            raise

        except Exception:
            logger.exception("Failed to initialise Google Drive service.")
            raise

    # def __init__(self) -> None:
    #     """
    #     Authenticate with Google Drive using OAuth credentials.
    #     """

    #     try:
    #         credentials = Credentials.from_authorized_user_file(
    #             settings.GOOGLE_TOKEN_FILE,
    #             scopes=DRIVE_SCOPE,
    #         )

    #         # Refresh the access token automatically if required
    #         if credentials.expired and credentials.refresh_token:
    #             credentials.refresh(Request())

    #             # Save refreshed token
    #             with open(settings.GOOGLE_TOKEN_FILE, "w") as token:
    #                 token.write(credentials.to_json())

    #         self.service = build(
    #             "drive",
    #             "v3",
    #             credentials=credentials,
    #             cache_discovery=False,
    #         )

    #         logger.info("Google Drive service initialised successfully.")

    #     except FileNotFoundError:
    #         logger.exception("OAuth token file not found.")
    #         raise

    #     except Exception:
    #         logger.exception("Failed to initialise Google Drive service.")
    #         raise

    # def __init__(self) -> None:
    #     """
    #     Authenticate with Google Drive API using a service account.

    #     Reads the service account credentials file path from
    #     ``settings.GOOGLE_SERVICE_ACCOUNT_FILE`` and initialises the Drive
    #     API client scoped to ``DRIVE_SCOPE``.

    #     Raises:
    #         FileNotFoundError: If the service account file does not exist.
    #         google.auth.exceptions.MalformedError: If the credentials file is
    #             invalid.
    #         Exception: For any other authentication failure.
    #     """
    #     try:
    #         # credentials = service_account.Credentials.from_service_account_file(
    #         #     settings.GOOGLE_SERVICE_ACCOUNT_FILE,
    #         #     scopes=DRIVE_SCOPE,
    #         # )

          

    #         credentials = Credentials.from_authorized_user_file(
    #             settings.GOOGLE_TOKEN_FILE,
    #             DRIVE_SCOPE
    #         )
    #         self.service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    #         logger.info("Google Drive service initialised successfully.")
    #     except FileNotFoundError:
    #         logger.error(
    #             "Service account file not found: %s",
    #             settings.GOOGLE_SERVICE_ACCOUNT_FILE,
    #         )
    #         raise
    #     except Exception:
    #         logger.exception("Failed to initialise Google Drive service.")
    #         raise

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    def sanitize_name(self, name: str) -> str:
        """
        Sanitize a folder or file name for use in Google Drive.

        Replaces any character in the set ``<>:"/\\|?*`` with an underscore
        and strips leading/trailing whitespace.

        Args:
            name: The raw folder or file name to sanitize.

        Returns:
            A sanitized string safe for use as a Drive folder or file name.

        Example:
            >>> drive.sanitize_name('Invoice: "Acme/Corp" 2026')
            'Invoice_ _Acme_Corp_ 2026'
        """
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", name)
        return sanitized.strip()

    # ------------------------------------------------------------------
    # Folder operations
    # ------------------------------------------------------------------

    def list_folders(self) -> list[dict]:
        """
        List all folders accessible by the service account.

        Intended primarily for debugging and testing purposes.

        Returns:
            A list of dictionaries, each containing ``id`` and ``name`` keys
            for every folder found.

        Raises:
            HttpError: If the Drive API returns an error response.
            Exception: For any other unexpected failure.

        Example:
            >>> folders = drive.list_folders()
            >>> for f in folders:
            ...     print(f["name"], f["id"])
        """
        try:
            query = "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            results = (
                self.service.files()
                .list(q=query, fields="files(id, name)")
                .execute()
            )
            files = results.get("files", [])
            logger.info("Listed %d folder(s).", len(files))
            return [{"id": f["id"], "name": f["name"]} for f in files]
        except HttpError:
            logger.exception("HttpError while listing folders.")
            raise
        except Exception:
            logger.exception("Unexpected error while listing folders.")
            raise

    def find_folder(self, folder_name: str, parent_id: str) -> str | None:
        """
        Search for a folder by name within a specific parent folder.

        Args:
            folder_name: The exact name of the folder to search for.
            parent_id: The Google Drive ID of the parent folder to search in.

        Returns:
            The folder ID as a string if found, or ``None`` if no matching
            folder exists.

        Raises:
            HttpError: If the Drive API returns an error response.
            Exception: For any other unexpected failure.

        Example:
            >>> folder_id = drive.find_folder("Invoices", "1AbCdEfGhIjK...")
        """
        try:
            query = (
                f"mimeType = 'application/vnd.google-apps.folder' "
                f"and name = '{folder_name}' "
                f"and '{parent_id}' in parents "
                f"and trashed = false"
            )
            results = (
                self.service.files()
                .list(q=query, fields="files(id, name)")
                .execute()
            )
            files = results.get("files", [])
            if files:
                logger.info(
                    "Found folder '%s' with ID '%s'.", folder_name, files[0]["id"]
                )
                return files[0]["id"]
            logger.info("Folder '%s' not found in parent '%s'.", folder_name, parent_id)
            return None
        except HttpError:
            logger.exception(
                "HttpError while searching for folder '%s'.", folder_name
            )
            raise
        except Exception:
            logger.exception(
                "Unexpected error while searching for folder '%s'.", folder_name
            )
            raise

    def create_folder(self, folder_name: str, parent_id: str) -> str:
        """
        Create a new folder inside the specified parent folder.

        Args:
            folder_name: The name for the new folder.
            parent_id: The Google Drive ID of the parent folder.

        Returns:
            The Google Drive ID of the newly created folder.

        Raises:
            HttpError: If the Drive API returns an error response.
            Exception: For any other unexpected failure.

        Example:
            >>> new_id = drive.create_folder("Receipts", "1AbCdEfGhIjK...")
        """
        try:
            metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id],
            }
            folder = (
                self.service.files()
                .create(body=metadata, fields="id")
                .execute()
            )
            folder_id = folder["id"]
            logger.info(
                "Created folder '%s' with ID '%s' in parent '%s'.",
                folder_name,
                folder_id,
                parent_id,
            )
            return folder_id
        except HttpError:
            logger.exception(
                "HttpError while creating folder '%s'.", folder_name
            )
            raise
        except Exception:
            logger.exception(
                "Unexpected error while creating folder '%s'.", folder_name
            )
            raise

    def get_or_create_folder(self, folder_name: str, parent_id: str) -> str:
        """
        Return the ID of a folder, creating it if it does not already exist.

        Args:
            folder_name: The name of the folder to find or create.
            parent_id: The Google Drive ID of the parent folder.

        Returns:
            The Google Drive ID of the existing or newly created folder.

        Raises:
            HttpError: If the Drive API returns an error response.
            Exception: For any other unexpected failure.

        Example:
            >>> folder_id = drive.get_or_create_folder("2026", "root_folder_id")
        """
        existing_id = self.find_folder(folder_name, parent_id)
        if existing_id:
            logger.info(
                "Reusing existing folder '%s' (ID: %s).", folder_name, existing_id
            )
            return existing_id
        logger.info(
            "Folder '%s' not found; creating it under parent '%s'.",
            folder_name,
            parent_id,
        )
        return self.create_folder(folder_name, parent_id)

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def find_file(self, filename: str, parent_id: str) -> str | None:
        """
        Search for a file (non-folder) by name within a specific parent folder.

        Args:
            filename: The exact name of the file to search for.
            parent_id: The Google Drive ID of the folder to search in.

        Returns:
            The file ID as a string if found, or ``None`` if no matching
            file exists.

        Raises:
            HttpError: If the Drive API returns an error response.
            Exception: For any other unexpected failure.

        Example:
            >>> file_id = drive.find_file("INV-001.pdf", "1AbCdEfGhIjK...")
        """
        try:
            query = (
                f"mimeType != 'application/vnd.google-apps.folder' "
                f"and name = '{filename}' "
                f"and '{parent_id}' in parents "
                f"and trashed = false"
            )
            results = (
                self.service.files()
                .list(q=query, fields="files(id, name)")
                .execute()
            )
            files = results.get("files", [])
            if files:
                logger.info(
                    "Found file '%s' with ID '%s'.", filename, files[0]["id"]
                )
                return files[0]["id"]
            logger.info(
                "File '%s' not found in parent '%s'.", filename, parent_id
            )
            return None
        except HttpError:
            logger.exception(
                "HttpError while searching for file '%s'.", filename
            )
            raise
        except Exception:
            logger.exception(
                "Unexpected error while searching for file '%s'.", filename
            )
            raise

    def delete_file(self, file_id: str) -> bool:
        """
        Permanently delete a file from Google Drive.

        Args:
            file_id: The Google Drive ID of the file to delete.

        Returns:
            ``True`` if the file was deleted successfully, ``False`` otherwise.

        Example:
            >>> deleted = drive.delete_file("1AbCdEfGhIjK...")
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info("Deleted file with ID '%s'.", file_id)
            return True
        except HttpError:
            logger.exception(
                "HttpError while deleting file with ID '%s'.", file_id
            )
            return False
        except Exception:
            logger.exception(
                "Unexpected error while deleting file with ID '%s'.", file_id
            )
            return False

    def upload_file(
        self,
        pdf_bytes: bytes,
        filename: str,
        parent_folder_id: str,
    ) -> dict:
        """
        Upload a PDF file to a Google Drive folder, replacing any existing copy.

        Before uploading, searches for an existing file with the same name in
        the target folder and deletes it to prevent duplicates.

        Args:
            pdf_bytes: The raw bytes of the PDF file to upload.
            filename: The name to assign to the uploaded file.
            parent_folder_id: The Google Drive ID of the destination folder.

        Returns:
            A dictionary with the following keys:

            - ``id`` (str): The Google Drive file ID of the uploaded file.
            - ``name`` (str): The name of the uploaded file.
            - ``url`` (str): A shareable Google Drive view URL for the file.

        Raises:
            RuntimeError: If an existing duplicate file is found but cannot
                be deleted; upload is aborted to prevent duplicates.
            HttpError: If the Drive API returns an error during upload.
            Exception: For any other unexpected failure.

        Example:
            >>> result = drive.upload_file(pdf_bytes, "INV-001.pdf", "folder_id")
            >>> print(result["url"])
        """
        try:
            existing_id = self.find_file(filename, parent_folder_id)
            if existing_id:
                logger.warning(
                    "Duplicate file '%s' found (ID: %s). Deleting before re-upload.",
                    filename,
                    existing_id,
                )
                deleted = self.delete_file(existing_id)
                if not deleted:
                    raise RuntimeError(
                        f"Unable to delete existing file '{filename}' (ID: {existing_id}). "
                        "Upload aborted to prevent duplicates."
                    )

            metadata = {
                "name": filename,
                "parents": [parent_folder_id],
            }
            media = MediaIoBaseUpload(
                io.BytesIO(pdf_bytes),
                mimetype="application/pdf",
                resumable=False,
            )
            uploaded = (
                self.service.files()
                .create(body=metadata, media_body=media, fields="id, name")
                .execute()
            )
            file_id = uploaded["id"]
            file_name = uploaded["name"]
            url = f"https://drive.google.com/file/d/{file_id}/view"
            logger.info(
                "Uploaded file '%s' (ID: %s) to folder '%s'.",
                file_name,
                file_id,
                parent_folder_id,
            )
            return {"id": file_id, "name": file_name, "url": url}
        except HttpError:
            logger.exception(
                "HttpError while uploading file '%s'.", filename
            )
            raise
        except Exception:
            logger.exception(
                "Unexpected error while uploading file '%s'.", filename
            )
            raise

    # ------------------------------------------------------------------
    # High-level orchestration
    # ------------------------------------------------------------------

    def upload_document(
        self,
        *,
        customer_name: str,
        document_type: str,
        file_name: str,
        pdf_bytes: bytes,
        year: int | None = None,
    ) -> dict:
        """
        Orchestrate the full document upload workflow.

        Automatically creates the required folder hierarchy under the
        configured Drive root folder and uploads the PDF, replacing any
        existing file with the same name.

        Folder structure created::

            <GOOGLE_DRIVE_ROOT_FOLDER>/
            └── <year>/
                └── <customer_name>/
                    └── <document_type>/
                        └── <file_name>.pdf

        Supported ``document_type`` values — use the :data:`DOCUMENT_TYPES`
        constant to avoid spelling mistakes::

            document_type=DOCUMENT_TYPES["invoice"]   # → "Invoices"
            document_type=DOCUMENT_TYPES["quotation"] # → "Quotations"
            document_type=DOCUMENT_TYPES["receipt"]   # → "Receipts"
            document_type=DOCUMENT_TYPES["lpo"]       # → "LPO"

        Args:
            customer_name: The name of the customer. Used as a folder name;
                will be sanitized before use.
            document_type: The category of the document (e.g. ``"Invoices"``).
                Used as a sub-folder name.
            file_name: The desired filename for the uploaded PDF, including the
                ``.pdf`` extension. Will be sanitized before use.
            pdf_bytes: The raw bytes of the PDF to upload.
            year: The year under which the document should be stored. Defaults
                to the current year if ``None``.

        Returns:
            A dictionary as returned by :meth:`upload_file`:

            - ``id`` (str): Google Drive file ID.
            - ``name`` (str): Uploaded file name.
            - ``url`` (str): Shareable view URL.

        Raises:
            ValueError: If ``customer_name``, ``document_type``, or
                ``file_name`` is empty or blank.
            RuntimeError: If an existing duplicate file cannot be deleted
                prior to upload.
            HttpError: If any Drive API call fails.
            Exception: For any other unexpected failure.

        Example:
            >>> drive = GoogleDriveService()
            >>> result = drive.upload_document(
            ...     customer_name="Acme Corp",
            ...     document_type="Invoices",
            ...     file_name="INV-2026-001.pdf",
            ...     pdf_bytes=pdf_data,
            ...     year=2026,
            ... )
            >>> print(result["url"])
        """
        if not customer_name.strip():
            raise ValueError("customer_name cannot be empty.")
        if not document_type.strip():
            raise ValueError("document_type cannot be empty.")
        if not file_name.strip():
            raise ValueError("file_name cannot be empty.")

        if year is None:
            year = datetime.now().year

        safe_customer = self.sanitize_name(customer_name)
        safe_document_type = self.sanitize_name(document_type)
        safe_filename = self.sanitize_name(file_name)
        root_folder_id: str = settings.GOOGLE_DRIVE_ROOT_FOLDER

        logger.info(
            "Starting upload_document: customer='%s', type='%s', file='%s', year=%d.",
            safe_customer,
            safe_document_type,
            safe_filename,
            year,
        )

        # Step 1: Year folder
        year_folder_id = self.get_or_create_folder(str(year), root_folder_id)

        # Step 2: Customer folder
        customer_folder_id = self.get_or_create_folder(safe_customer, year_folder_id)

        # Step 3: Document-type folder
        document_folder_id = self.get_or_create_folder(safe_document_type, customer_folder_id)

        # Step 4 & 5: Upload file and return result
        result = self.upload_file(pdf_bytes, safe_filename, document_folder_id)
        logger.info(
            "upload_document complete. File available at: %s", result["url"]
        )
        return result