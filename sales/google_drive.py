from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from django.conf import settings
import io


class GoogleDriveService:

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/drive"]
        )

        self.service = build(
            "drive",
            "v3",
            credentials=credentials
        )

    # --------------------------------------------
    # List all folders (Testing)
    # --------------------------------------------
    def list_folders(self):

        results = self.service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id,name)"
        ).execute()

        return results.get("files", [])

    # --------------------------------------------
    # Find folder inside parent folder
    # --------------------------------------------
    def find_folder(self, folder_name, parent_id):

        query = (
            f"'{parent_id}' in parents "
            f"and name='{folder_name}' "
            f"and mimeType='application/vnd.google-apps.folder' "
            f"and trashed=false"
        )

        results = self.service.files().list(
            q=query,
            fields="files(id,name)"
        ).execute()

        folders = results.get("files", [])

        if folders:
            return folders[0]["id"]

        return None

    # --------------------------------------------
    # Create new folder
    # --------------------------------------------
    def create_folder(self, folder_name, parent_id):

        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }

        folder = self.service.files().create(
            body=metadata,
            fields="id"
        ).execute()

        print(f"Created Folder : {folder_name}")

        return folder["id"]

    # --------------------------------------------
    # Get folder or create if not exists
    # --------------------------------------------
    def get_or_create_folder(self, folder_name, parent_id):

        folder_id = self.find_folder(folder_name, parent_id)

        if folder_id:
            print(f"Folder Exists : {folder_name}")
            return folder_id

        return self.create_folder(folder_name, parent_id)