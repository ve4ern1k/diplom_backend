import os
from PIL import Image
from uuid import uuid4
from pathlib import Path


class ImgService:

    def __init__(self, folder: str = 'media'):
        self.folder = self.ensure_directory(folder)


    @staticmethod
    def ensure_directory(dir: str) -> str:
        Path(dir).mkdir(parents=True, exist_ok=True)
        return dir


    def save(self, image: Image.Image) -> str:
        img_name = str(uuid4()) + '.' + image.format
        image.save( os.path.join(self.folder, img_name), image.format, quality=90, optimize=True, progressive=True )
        return img_name


    def retreive_path(self):
        return self.folder
