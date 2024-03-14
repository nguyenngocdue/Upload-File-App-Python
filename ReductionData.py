import os
import shutil
import sys
sys.path.append('/home/duenguyen/NND/App/Due Filter Items App/')
from my_functions import*


def createFoldersYearsAndMonths():
    root_folder = "/home/duenguyen/NND/App/uploads_app1/"
    n = int(input("Enter the number of years to create: "))
    array_years = []
    for i in range(n):
        element = input(f"Enter years {i+1}: ")
        array_years.append(element)
    p = root_folder +'/ReduceData/'
    [os.mkdir(p + i) for i in array_years]
    for y in array_years:[os.mkdir(p + y + '/' + i ) for i in ['01','02','03','04','05','06','07','08','09','10','11','12'] ]

def getAllFiles(source_directory):
    files = [ file_name
    for file_name in os.listdir(source_directory)
    if os.path.isfile(os.path.join(source_directory, file_name))]
    return set(files)

def getTypesOfFailNames(dash_endIndex, file):
    fail_positive_name, fail_strange_name = set(), set()
    if file_name[dash_endIndex+1:].replace('x', '').isnumeric():
        name = file_name[:dash_endIndex] + file_extension
        fail_positive_name.add(name)
    else:
        fail_strange_name.add(file)
    return fail_positive_name, fail_strange_name

def createFileNames(files, img_files):
    result = set()
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        types_name = [
            file_name + file_extension.upper(),
            file_name + file_extension.lower(),
            file_name + '-150x150' + file_extension.upper(),
            file_name + '-150x150' + file_extension.lower()
        ]
        result.update(name for name in types_name if name in img_files)
    return result

def isImage(file):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    if os.path.splitext(file)[1].lower() in image_extensions: return True
    return False

def copyAndSaveItems(data, source_directory, destination_directory):
    global count_images_saved
    global count_others_save
    global not_exist_files
    count_images_saved = 0
    count_others_save = 0
    not_exist_files = 0
    for file in data:
        source_path = os.path.join(source_directory, file)
        destination_path = os.path.join(destination_directory, file)
        if os.path.exists(source_path):
            isCheckSaved = shutil.copyfile(source_path, destination_path)
            if isCheckSaved:
                if isImage(file):
                    count_images_saved += 1
                    # print(f"File '{file}' copied successfully. {count_images_saved}")
                    print(f"{file}, images copied successfully. {count_images_saved}")
                else:
                    count_others_save += 1
                    print(f"{file}, other files copied successfully. {count_others_save}")
        else:
            not_exist_files +=1
            print(f"{destination_path} does not exist. ==> {not_exist_files}")

def reduce_positive_name(fail_positive_names):
    positive_name = set()
    for file in fail_positive_names:
        file_name, file_extension =  os.path.splitext(file)
        dash_endIndex = file_name.rfind("-")
        tail_name = file_name[dash_endIndex+1:]
        if tail_name.replace('x', '').isnumeric() and '-150x150' in tail_name and dash_endIndex > 0:
            name = file_name[:dash_endIndex] + file_extension.lower()
            positive_name.add(name)
        else: 
            name = file_name + file_extension.lower()
            positive_name.add(name)
    return positive_name

def getErrorFilesSaveFailed(all_primary_files, file_names):
    diff_primary_file =all_primary_files.difference(file_names)
    name_saved_failed = set()
    for file in diff_primary_file:
        file_name, file_extension =  os.path.splitext(file)
        dash_endIndex = file_name.rfind("-")
        if dash_endIndex > 0:
            wxh = file_name[dash_endIndex+1:]
            if wxh == '-150x150':
                name_saved_failed.add(file)
        else:
                name_saved_failed.add('check ==>'+ file)
    return name_saved_failed

# Get the home directory
# root_folder = os.path.expanduser("~")
root_dataInput = f"{root_folder}DataInput/"
root_dataOutput = f"{root_folder}DataOutput/"
destination_dataOutput = 'DataUpload/Primary/'
negative_folder = 'NegativeFiles/'

# ask = input('Do you want to create new folders for years and months:')
# if ask:
#     createFoldersYearsAndMonths()

year_folder = input(f'Enter the year folder name to get data (default value: {default_year}): ') or default_year


# Specify the folder name
month_folder = input('Enter the month folder name to get data: ')

# Source directory containing the image files
source_folder =  year_folder +"/" + month_folder
source_directory = os.path.join(root_dataInput, source_folder)

# Destination directory to copy the image files
destination_folder = destination_dataOutput +year_folder +"/" + month_folder
destination_directory = os.path.join(root_dataOutput, destination_folder)

if os.path.exists(source_directory) and os.path.isdir(source_directory):
    other_files, img_files = divideFiles(source_directory)
    
    array_names  = set()
    fail_strange_names = set()
    fail_positive_names = set()
    for file in img_files:
        file_name, file_extension =  os.path.splitext(file)
        file150 = file_name + "-150x150" + file_extension
        if file150 in img_files:
            array_names.add(file)
            fail_positive_names.add(file)
        else:
            dash_endIndex = file_name.rfind("-")
            if dash_endIndex > 0:
                fail_positive_name, fail_strange_name = getTypesOfFailNames(dash_endIndex, file)
                fail_positive_names.update(fail_positive_name)
                fail_strange_names.update(fail_strange_name)
                array_names.update(fail_positive_name)
            else:
                fail_positive_names.add(file)
                array_names.add(file)

    file_names = createFileNames(array_names,img_files)
    all_files_to_save =  file_names.union(other_files)
    fail_negative_images = set()
    for file in file_names:
        fail_negative_name, positive_image = getNegativeAndPositiveName(file, img_files)
        fail_negative_images.update(fail_negative_name)
    copyAndSaveItems(all_files_to_save, source_directory, destination_directory)

    # CODE CHECK
    all_primary_files = getAllFiles(source_directory)
    diff_files = all_primary_files.difference(all_files_to_save)
    total_filter_files = len(other_files) + len(fail_positive_names) + len(fail_strange_names)
    str_total_filter_files = str(len(other_files)) + '+' + str(len(fail_positive_names)) + '+' + str(len(fail_strange_names))
    fail_neg_pos_name = fail_positive_names.union(fail_strange_names)
    str_check_other_files_saved = str(len(all_files_to_save.difference(img_files))) + '=' +  str(len(other_files))
    
    print(f"\n||||||||||||||||||||||||{year_folder}/{month_folder}||||||||||||||||||||||||\n")
    print(f"Source file does not exist: {not_exist_files}" )
    print(f"Total other files saved: {count_others_save}" )
    print(f"Total images saved: {count_images_saved}" )
    print(f"Total files saved: {count_images_saved + count_others_save - not_exist_files}" )

    print("========================================================================")
    print(f"all_primary_files: {len(all_primary_files)}")
    print(f"all_image_names: {len(img_files)}")
    print(f"all_other_file: {len(other_files)}")
    print(f"fail_positive_names: {len(fail_positive_names)}")
    print(f"total images to save: {len(reduce_positive_name(fail_positive_names))} (not 150x150)")
    print(GREEN + "=======================NEGATIVE IMAGES==================================" + RESET)
    print(f"fail_negative_images: {len(fail_negative_images)} \n", fail_negative_images)
    print("========================================================================")
    print(f"check total the number of files: {len(all_primary_files)} = {total_filter_files} ({str_total_filter_files})")
    print("difference() between set 'img_files' and set 'fail_neg_pos_name':",len(img_files.difference(fail_neg_pos_name)))
    print(f"check Other files saved: {len(other_files) == len(all_files_to_save.difference(img_files))}, {str_check_other_files_saved}")
    print(f"check for that were not saved successfully: {len(getErrorFilesSaveFailed(all_primary_files, all_files_to_save)) == 0}", f",{getErrorFilesSaveFailed(all_primary_files, all_files_to_save)}") 

    print(GREEN + "=======================SAVE NEGATIVE FILES==============================" + RESET)
    destination_directory = f"{root_dataOutput}{negative_folder}{year_folder}/{month_folder}"
    print(destination_directory)

    copyAndSaveItems(fail_negative_images, source_directory, destination_directory)

else:
    print("Folder does not exist:", source_directory)
