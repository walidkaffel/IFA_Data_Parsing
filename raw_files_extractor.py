# -*- coding: utf-8 -*-
"""
Created on Sun May  8 16:52:06 2022

@author: walid
"""

import parameters as param
import os
import glob
import zipfile

def extractor():
    
    # removing existing files in destination
    list_of_files = glob.glob(param.extracted_files_repo+'/*')
    for pdf_file in list_of_files:
        os.remove(pdf_file)
    
    # extracting zipped files
    list_of_files = glob.glob(param.raw_files_repo+'/*')
    for raw_file in list_of_files :
        with zipfile.ZipFile(raw_file, 'r') as zip_ref:
            zip_ref.extractall(param.extracted_files_repo)
    
    # removing pdf files
    list_of_files = glob.glob(param.extracted_files_repo+'/*.pdf')
    for pdf_file in list_of_files:
        os.remove(pdf_file)


extractor()
