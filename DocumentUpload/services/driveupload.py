from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
from middlewares.request_middleware import get_request


def get_gd_storage():
    # user_email = str(get_request().user.email)

    # Google Drive Permissions for read and write files
    permission =  GoogleDriveFilePermission(
    GoogleDrivePermissionRole.READER,
    GoogleDrivePermissionType.USER,
    'globalkhabariabdulla@gmail.com' 
    )
    gd_storage = GoogleDriveStorage(permissions=(permission, ))
    return gd_storage