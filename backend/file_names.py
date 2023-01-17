from backend.constants import FileType


# returns the file extension if it is a member of FileType
def get_file_type(filename: str):
    file_type_list = [member.value for member in FileType]
    for file_type in file_type_list:
        if filename.endswith(file_type):
            return file_type
    return ''