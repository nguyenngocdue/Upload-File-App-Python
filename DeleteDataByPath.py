import sys
import atexit
sys.path.append('/home/duenguyen/NND/App/Due Filter Items App/')
from my_functions import*

def delete_files_in_folder(folder_path):
    count_del_files = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                count_del_files += 1
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error occurred while deleting file: {file_path}")
                print(str(e))
    print(f'Total items deleted: {count_del_files}')

def delete_end_files_in_year(folder_path):
    years = getFiles(folder_path)
    months = sorted(getFiles(folder_path + years[0]))
    return [delete_files_in_folder(folder_path + year + '/' + mon ) for year in years for mon in months ]


# Specify the folder path
print(f'Root: {root_folder}' )
folder_path = input(f'Enter your path before year folder (default value: {default_del_path}): ') or default_del_path
# Register the delete_files_in_folder function to be called at program exit
level = input('Enter level:' ) or '1'
if int(level):
    atexit.register(delete_end_files_in_year, folder_path)
else:
    atexit.register(delete_files_in_folder, folder_path)