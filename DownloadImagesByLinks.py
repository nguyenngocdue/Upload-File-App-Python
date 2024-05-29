import requests
import sys
import os
sys.path.append('/home/duenguyen/NND/App/Due Filter Items App/')
from my_functions import*
from datetime import datetime

current_month = datetime.now().month
zero_padded_month = str(current_month).zfill(2)

# Destination folder to save the downloaded images
year_folder = input(f'Enter year folder name (default value: {default_year}): ') or default_year
mon_folder = input('Enter month folder name: ')


# Source directory containing the image files
root_dataOutput = f"{root_folder}DataOutput/"
source_directory = os.path.join(root_dataOutput, f'NegativeFiles/{year_folder}/{mon_folder}')

negative_files = getFiles(source_directory)
name150x150, primary_name = divide150AndPrimaryImage(negative_files)
if len(name150x150): print(f"Check files that is not primary file: {name150x150}")
strLink = f"https://minio.tlcmodular.com/tlc-app/output/"
image_links = addLinkForImageName(strLink, primary_name, '-150x150')

print(GREEN + f'======================={year_folder}/{mon_folder}===========================' + RESET)

destination_folder = f"{root_dataOutput}NegativeFiles_fix/{year_folder}/{mon_folder}/"

# Iterate over the image links
failed_imgs = set()

for link in image_links:
    # Extract the filename from the link
    filename = link.split("/")[-1]

    # Send a GET request to download the image
    response = requests.get(link)
    print(link)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the image to the destination folder
        if os.path.exists(destination_folder):
            with open(destination_folder + filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {filename}")
        else: failed_imgs.add(filename)
    else:
        failed_imgs.add(filename)
[print(f"Failed to download: {img}") for img in failed_imgs]
print('==================================================')
print(f'Check the number of items in "NegativeFiles_fix" \
    ===>{len(getFiles(destination_folder)) == len(getFiles(source_directory))}\
    "{len(getFiles(destination_folder))}/{len(getFiles(source_directory))}"')



