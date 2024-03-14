import os
import shutil



# Global variable
not_exist_files = 0
count_images_not_save = 0 
count_images_saved = 0
count_items_saved = 0
count_items_not_save = 0
default_year = '2023'
root_folder = '/home/duenguyen/NND/App/uploads_app1/'
default_del_path = '/home/duenguyen/NND/App/uploads_app1/DataOutput/DataUpload/RichData/'

# Define color escape codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def divideFiles(source_directory):
    other_files, img_files = set(), set()
    image_extensions = [".jpg","JPG", ".jpeg",".JPEG", ".png",".PNG", ".gif",".GIF", ".bmp", ".BMP"]
    for file_name in os.listdir(source_directory):
        if os.path.isfile(os.path.join(source_directory, file_name)) and os.path.splitext(file_name)[1].lower() in image_extensions:
            img_files.add(file_name)
        else:
            other_files.add(file_name)
    return other_files, img_files

def divide150AndPrimaryImage(images):
    name150x150, primary_name = set() , set()
    for img in images:
        file_name, file_extension =  os.path.splitext(img)
        dash_endIndex = img.rfind("-")
        tail_name = file_name[dash_endIndex:]
        if dash_endIndex > 0 and '-150x150' in tail_name and tail_name[1:].replace('x', '').isnumeric():
            name150x150.add(img)
        primary_name.add(img)
    return name150x150, primary_name
def getFiles(source_directory):
    return [file for file in os.listdir(source_directory)]

def getFile2(source_directory):
    return [name for name in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, name))]

def addLinkForImageName(strLink, files, addName):
    array_links = set()
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        array_links.add(strLink + file_name + addName + file_extension)
    return array_links

def getNegativeAndPositiveName(file, img_files):
    fail_negative_name = set()
    positive_image = set()
    file_name, file_extension = os.path.splitext(file)
    dash_endIndex = file_name.rfind("-")
    tail_name = file_name[dash_endIndex:]
    if dash_endIndex > 0 and '-150x150' in tail_name and tail_name[1:].replace('x', '').isnumeric():
        file_name = file_name[:dash_endIndex]
        if (file_name + file_extension) in img_files and (file_name + '-150x150' + file_extension) in img_files:
            positive_image.add(file)
        elif (file_name + '-150x150' + file_extension.lower()) in img_files and (file_name + file_extension.upper()) in img_files:
            positive_image.add(file)
        elif (file_name + '-150x150' + file_extension.upper()) in img_files and (file_name + file_extension.lower()) in img_files:
            positive_image.add(file)
        else:
            fail_negative_name.add(file)
    else:
        if (file_name + file_extension) in img_files and (file_name + '-150x150' + file_extension) in img_files:
            positive_image.add(file)
        elif (file_name + file_extension) in img_files and (file_name + '-150x150' + file_extension.lower()) in img_files:
            positive_image.add(file)
        elif (file_name + file_extension.upper()) in img_files and (file_name + '-150x150' + file_extension.lower()) in img_files:
            positive_image.add(file)
        else:
            fail_negative_name.add(file)
    return fail_negative_name, positive_image

def flatten(arr):
    flattened = []
    for i in arr:
        if isinstance(i, list):
            flattened.extend(flatten(i))
        else:
            flattened.append(i)
    return flattened

def getLastFilesInDirectoryFromFolderPath(year, source_path):
    months = getFiles(source_path + year)
    files = [getFiles(source_path + year + '/'+ mon) for mon in months]
    return flatten(files)

def createFolder(root_folder, folder_name):
    folder_path = root_folder + f"{folder_name}/"
    if not os.path.exists(folder_path): 
        os.mkdir(folder_path)
        print(f"===>{folder_path} created successfully.")
    else:
        print(f"===>{folder_path} exists.")

def createFoldersYearsAndMonths(root_folder, folder_name):
    n = int(input("Enter the number of years to create: "))
    array_years = [input(f"Enter years {i+1}: ") for i in range(n)]
    folder_path = root_folder + f"{folder_name}/"
    [createFolder(folder_path,i)for i in array_years]
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    [createFolder(folder_path + year + '/', mon) for year in array_years for mon in months]
