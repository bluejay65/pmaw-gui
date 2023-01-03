import uuid
import os
from cryptography.fernet import Fernet
from secret_constants import APP_INFO_KEY
import constants
import logging

log = logging.getLogger('__name__')

data_file_name = 'data'
cache_file_name = 'cache'
log_file_name = 'dcfr.log'
resource_folder_name = 'resources'

app_data_dir = os.path.join(os.environ['APPDATA'], constants.APP_NAME)

class AppInfo():
    def save_data(info: str):
        info_path = AppInfo.get_file_path(data_file_name)
        if not os.path.exists(app_data_dir):
            os.mkdir(app_data_dir)
        
        with open(info_path, 'wb') as f:
            f.write(AppInfo.encrypt_txt(info))


    def encrypt_txt(text: str):
        return Fernet(APP_INFO_KEY).encrypt(text.encode())

    def save_to_cache(text: str):
        cache_path = AppInfo.get_file_path(data_file_name)
        if not os.path.exists(app_data_dir):
            os.mkdir(app_data_dir)
        with open(cache_path, 'r') as f:
            num_lines = sum(1 for line in f)
        with open(cache_path, 'w') as f:
            pass

    def get_device_id():
        info_path = AppInfo.get_file_path(data_file_name)
        if os.path.exists(info_path):
            with open(info_path, 'rb') as f:
                try:
                    id = Fernet(APP_INFO_KEY).decrypt(f.read()).decode()
                    if len(id) == 30:
                        return id
                except:
                    log.info('Key invalid. Generating a new one.')
        id = uuid.uuid4().hex[:-2]
        AppInfo.save_data(id)
        return id

    def configure_log():
        if os.path.isfile(AppInfo.get_log_path()):
            with open(AppInfo.get_log_path(), 'r+') as log:
                lines = log.readlines()
                if len(lines) > 1000:
                    log.seek(0)
                    log.truncate()
                    for line in lines[len(lines)-1000:]:
                        log.write(line)
                

    def get_log_path():
        return AppInfo.get_file_path(log_file_name)

    def get_file_path(file_name):
        return os.path.join(app_data_dir, file_name)

    def get_resource_folder():
        return AppInfo.get_file_path(resource_folder_name)
