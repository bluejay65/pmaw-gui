from app_info import AppInfo


with open(AppInfo.get_log_path(), 'w') as f:
    for i in range(1200):
        f.write(str(i)+'\n')
