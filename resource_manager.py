import os
import csv
from cairosvg import svg2png
from PIL import Image, ImageTk


class ResourceManager():
    def __init__(self, resource_folder:str):
        self.resource_file_dict = {}
        resource_files = os.listdir(resource_folder)

        with open(os.path.join(os.getcwd(), 'resource_links.txt')) as file:
            for line in csv.DictReader(file):
                if line['name'] not in resource_files:
                    if line['type'] == 'svg':
                        svg2png(url=line['url'], write_to=os.path.join(resource_folder, line['name']))

                self.resource_file_dict[line['name']] = os.path.join(resource_folder, line['name'])
            
                
    def load_image(self, name, size=(0,0)):
        loader = Image.open(self.resource_file_dict[name])
        if size[0] > 0 and size[1] > 0:
            loader = loader.resize(size)
        return ImageTk.PhotoImage(loader)


    def get_resource_file(self, name):
        return self.resource_file_dict[name]

    def get_image(self, name):
        return self.image_dict['name']


