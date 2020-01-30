# coding: utf-8
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os
from shutil import rmtree

courses_url = 'https://www.datacamp.com/courses/'
course = 'parallel computing with dask'
course_url = courses_url + course.replace(' ', '-')

r = requests.get(course_url)
html = r.content
soup = BeautifulSoup(html, 'html.parser')
datasets = soup.find_all('li', class_='course__dataset')

home = os.path.expanduser('~')  # Home folder
course = course.replace(' ', '_')
folder = os.path.join(home, 'datacamp', course, 'datasets/')
if not os.path.exists(os.path.join(home, course)):
    os.makedirs(folder)
else:
    os.mkdir(folder)

for dataset in datasets:
    dataset_url = dataset.a.get('href')
    filename = dataset_url.split('/')[-1]
    resp = requests.get(dataset_url)
    if resp.status_code == 200:
        # Download files to our folder
        file_path = folder + filename
        with open(file_path, 'wb') as file:
            file.write(resp.content)
    
        # Unzip .zip files
        if filename.endswith('.zip'):
            with ZipFile(file_path, 'r') as zip_file:
                zip_file.extractall(folder)

os.chdir(folder)
if os.path.exists('__MACOSX'):
    rmtree('__MACOSX')

# Remove .zip files in our folder
dir_iterator = os.scandir()
for entry in dir_iterator:
    if entry.name.endswith('.zip'):
        os.remove(entry)

