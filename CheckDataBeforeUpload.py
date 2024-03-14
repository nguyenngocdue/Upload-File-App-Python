from tqdm import tqdm
import time
import sys
sys.path.append('/home/duenguyen/NND/App/Due Filter Items App/')
from my_functions import*

def updateDestinationPath(root_name,folder_name):
    des_path = root_name + folder_name + '/'
    os.mkdir(des_path)
    return des_path

source_path = root_folder + 'DataOutput/DataUpload/RichData/'
years = getFiles(source_path)
months  = sorted(getFiles(source_path + years[0]))
fail_negative_images = set()

count_images_checked = 0
count_other_files = 0
for year in years:
    # progress_bar = tqdm(year, desc="Processing")
    for mon in months:
        path = source_path + year + '/' + mon
        other_files, img_files = divideFiles(path)
        count_other_files += int(len(other_files))
        for img_file in img_files:
            count_images_checked += 1
            # custom_message = "{}/{}: {}".format(year,mon,mon)
            # progress_bar.set_description(custom_message)
            fail_negative_names, positive_images = getNegativeAndPositiveName(img_file, img_files)
            if len(positive_images): fail_negative_images.update(fail_negative_names)
        print(f"Check month: {mon}/{year}: {count_images_checked} / {len(img_files)} items")

print(GREEN + '=======================CHECK DATA========================='+ RESET)
if len(fail_negative_names): print("Please to check 'FAIL NEGATIVE IMAGES': {fail_negative_images}")
else: print(f"{count_images_checked} images were checked, fail_negative_images: {len(fail_negative_images) == 0}, {len(fail_negative_images)} = 0")
print (f"{count_images_checked + count_other_files} items were checked before uploading to https://console.tlcmodular.com/")