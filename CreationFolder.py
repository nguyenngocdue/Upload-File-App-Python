import os
import shutil
import sys
sys.path.append('/home/duenguyen/NND/App/Due Filter Items App/')
from my_functions import*

root_folder = f"{root_folder}DataOutput/"
default_folder = "NegativeFiles"

print(f'Root folder: {root_folder}')
root_input = input('Do you want to change your root? (0 = No / 1 = Yes):')
if root_input == '1':
    root_folder = input('Enter new root:')+'/'
folder_name = input(f'Enter a new folder name (default folder: {default_folder}):') or default_folder
createFolder(root_folder, folder_name)
folder = createFoldersYearsAndMonths(root_folder, folder_name)