# -*- coding: utf-8 -*-

import os
import sys
from traceback import *
#import pwd
#import grp
from shutil import rmtree
from django.conf import settings



allowImagesList = ['png', 'jpg', 'jpeg', 'tif', 'gif']


class MediaStorage(object):
    """ 
    Documentation

    Supported methods:
        1. self.save(): save a new file
        2. self.rm():   delete an existing file
        3. self.mkdir(): create a new directory
        4. self.rmdir(): delete an existing directory
        5. self.flushdir(): delete the files included to a directory
        6. self.size(): get the size of a file in MB
        7. self.validateImage(): validate an image based on its type
        8. self.validateFile(): validate a file based on its type

    Usage:
        from MediaStorage import *

        object = MediaStorage()
        object.save(file)
        object.rm()
        object.mkdir()
        object.rmdir()
        object.flushdir()
        object.size()
        object.validateImage()
        object.validateFile()
    """


    def __init__(self, path, folder, filename):        
        """Instatiates a new object"""        

        self.folder     = str(folder)
        self.filename   = str(filename)
        self.path       = path + self.folder
        self.full_path = self.path + "/" + self.filename


    def validateImage(self):
        """Validate the image type"""
        format = self.filename.split('.')[-1]
        format = format.lower()
        if format not in allowImagesList:
            return False
        return True


    def save(self, fd):
        try:
            with open(self.full_path, 'wb+') as destination:
                for chunk in fd.chunks():
                    destination.write(chunk)
            return True
        except:
            if settings.DEBUG:
                print_exc()
            return False

    def rm(self):
        """Delete an existing file"""
        try:
            os.remove(self.full_path)
            return True
        except OSError:
            if settings.DEBUG:
                print_exc()            
            return False

    def mkdir(self):
        """Create a directory"""       
        try:        
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            return True
        except:
            if settings.DEBUG:
                print_exc()            
            return False

    def rmdir(self):
        """Delete a directory"""
        try:
            if os.path.isdir(self.path):
                rmtree(self.path)
            return True
        except OSError:
            if settings.DEBUG:
                print_exc()            
            return False

    def flushdir(self):
        """Delete all files that are included in a directory"""

        try: 
            for fitem in os.listdir(self.path):
                curpath = os.path.join(self.path, fitem)
                try:
                    if os.path.isfile(curpath):
                        os.unlink(curpath)
                    return True
                except Exception, e:
                    print e
                    return False
        except:
            if settings.DEBUG:
                print_exc()            
            return False

    def size(self):
        """Yield the object's size"""
        try:
            import math
            size = os.stat(self.full_path)

            i = int(math.floor(math.log(size.st_size,1024)))
            p = math.pow(1024,i)
            s = round(size.st_size/p,2)
            if s > 0:
                return s
            return 0
        except:
            if settings.DEBUG:
                print_exc()            
            return -1


if __name__ == '__main__':
    if DEBUG:
        print MediaStorage.__doc__