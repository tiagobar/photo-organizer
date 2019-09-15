#!/usr/bin/env python3
import os
import sys
import shutil
from datetime import datetime
from PIL import Image


class PhotoOrganizer:
    DATETIME_EXIF_INFO_ID = 36867
    extensions = ['jpg', 'jpeg', 'png']

    def folder_path_from_photo_date(self, file):
        date = self.photo_shooting_date(file)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m-%d')

    def photo_shooting_date(self, file):
        date = None
        photo = Image.open(file)
        if hasattr(photo, '_getexif'):
            info = photo._getexif()
            if info:
                if self.DATETIME_EXIF_INFO_ID in info:
                    date = info[self.DATETIME_EXIF_INFO_ID]
                    date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        if date is None:
            date = datetime.fromtimestamp(os.path.getmtime(file))
        return date

    def move_photo(self, file):
        file_dir = os.path.dirname(file)
        file_name = os.path.basename(file)

        new_folder = file_dir + '/' + self.folder_path_from_photo_date(file)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        shutil.move(file, new_folder + '/' + file_name)

    def organize(self, dir_to_process=None):
        if dir_to_process is None:
            dir_to_process = '.'

        photos = [
            dir_to_process + '/' + filename for filename in os.listdir(dir_to_process)
                if os.path.isfile(dir_to_process + '/' + filename) and any(filename.lower().endswith('.' + ext.lower()) for ext in self.extensions)
        ]
        for filename in photos:
            self.move_photo(filename)


arg_dir = sys.argv[1] if len(sys.argv) > 1 else None
PO = PhotoOrganizer()
PO.organize(arg_dir)
