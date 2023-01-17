import os
from backend import file_names
from backend.search_pmaw import CallPmaw
from cairosvg import svg2png
from PIL import Image, ImageTk


class ResourceManager():

    # loads files in resource folder to dict and creates resource files that are missing
    def __init__(self, resource_folder:str):
        self.resource_file_dict = {}
        resource_files = [CallPmaw.remove_file_type(file) for file in os.listdir(resource_folder)]

        for filename in os.listdir(os.path.join(os.getcwd(), 'resources')):
            with open((os.path.join(os.path.join(os.getcwd(), 'resources'), filename)), 'r') as f:
                imported_file_name = CallPmaw.replace_file_type(os.path.basename(f.name), '.png')

                if CallPmaw.remove_file_type(f.name) not in resource_files:

                    # generates png from svg files
                    if file_names.get_file_type(f.name) == '.svg':
                        svg2png(file_obj=f, write_to=os.path.join(resource_folder, imported_file_name))

                self.resource_file_dict[imported_file_name] = os.path.join(resource_folder, imported_file_name)
            
    # returns an image for tkinter from the resource dict
    def load_image(self, name, size=(0,0)):
        loader = Image.open(self.resource_file_dict[name])
        if size[0] > 0 and size[1] > 0:
            loader = loader.resize(size)
        return ImageTk.PhotoImage(loader)


    def get_resource_file(self, name):
        return self.resource_file_dict[name]