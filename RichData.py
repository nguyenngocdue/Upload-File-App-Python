import sys
from tqdm import tqdm
sys.path.append('/home/duenguyen/NND/App/Due Filter Items App/')
from my_functions import*

def copyFiles01(files, path_destination, mon_path):
    global count_items_not_save
    global count_items_saved
    for file in files:
        source_path = mon_path + file
        if os.path.exists(source_path):
            destination_path = path_destination + year + '/' + mon +'/'+ file
            print(source_path)
            isCheckSaved = shutil.copyfile(source_path, destination_path)
            if isCheckSaved:
                count_items_saved += 1
                # print(f"{file}, images copied successfully. =====> {count_items_saved}")
            else: count_items_not_save + 1


path_data1 = root_folder + 'DataOutput/DataUpload/Primary/' 
path_data2 = root_folder + 'DataOutput/NegativeFiles_fix/' 
path_destination = root_folder + 'DataOutput/DataUpload/RichData/' 




years = getFiles(path_data1)
months = sorted(getFile2(path_data1 + years[0]))
# print(f"{months}/{years}", path_data1)

for year in years:
    p1 = path_data1 + year + '/'
    _p1 = path_data2 + year + '/'
    for mon in months:
        p2 = p1 + mon + '/'
        _p2 = _p1 + mon + '/'
        files = getFiles(p2)
        _files = getFiles(_p2)
        copyFiles01(files, path_destination, p2)
        copyFiles01(_files, path_destination, _p2)

source_path = root_folder + 'DataOutput/DataUpload/RichData/'
print('\n================================================')
# print(f"{count_items_saved} files copied successfully.")
# print(f"{count_items_not_save} files was not copied successfully.")


              

