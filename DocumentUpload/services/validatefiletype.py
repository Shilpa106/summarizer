import os


def validate_file_extension(serializer):

    ext = os.path.splitext(serializer.initial_data['upload_file'].name)[1]
    valid_extenstion = [".pdf", ".jpg", ".jpeg", ".gif", ".png", ".docs", ".doc", ".xlsx", "xls"]

    if ext.lower() in valid_extenstion:
        return True
    else:
        return False