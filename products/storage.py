from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class ProductFileStorage:
    def __init__(self,name: str,id: str):
        self.table_name = str(name)
        self.product_id = str(id)
    
    @property
    def imageFileStorage(self):
        self.file_path_str = '{}/{}'.format(self.table_name,self.product_id)
        self.file_path = os.path.join(settings.MEDIA_ROOT, self.file_path_str)
        print("FILE",self.file_path)
        fs = FileSystemStorage(location=self.file_path,file_permissions_mode=0o644)
        return fs