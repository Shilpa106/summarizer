import os


def validate_file_extension(serializer):
    try:
        ext = os.path.splitext(serializer.initial_data['upload_file'].name)[1]
        valid_extenstion = [".txt", ".pdf", ".jpg", ".jpeg", ".gif", ".png", ".docs", ".docx", ".doc", ".xlsx", "xls"]
        
        if ext.lower() in valid_extenstion:
            return True
        else:
            return False
    except Exception as e:
        return 'Please select file first'