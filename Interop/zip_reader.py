import os
import zipfile
import re

path = 'E:/p4_avatars/ACT/AssetStaging/'

def get_name(zip_path):
    archive = zipfile.ZipFile(zip_path, 'r')
    items = archive.read('asset_metadata')
    asset_name = re.search(r'Name":"(.*?)","VersionNumber', items).group(1)  # Parsing asset name from the string.
    return asset_name

for filename in os.listdir(path):
    zip_path = path + filename
    print get_name(zip_path)



