'''
Created on Oct 29, 2018

@author: alexs
'''

# Imports
import os
import json
import shutil
import platform
from pathlib import Path
from datetime import datetime
from uuid import getnode as get_mac

# Module functions
def createFolderInMainDrive(folderName):
    ''' Creates a folder in the main drive of the operating system. Can take an input of a directory
    pathway defined using back slashes, such as "TempFolder/default_folder/new_directory". '''
    # Define path name
    filePath = Path("/%s/"%folderName)
    
    # Check if folder already exists
    if (os.path.exists(filePath) != True):
        print("Creating Directory: %s"%filePath)
        os.makedirs(filePath)
    else:
        print("Directory already exists. No folders created")
    
    # Return the path
    return filePath

def createFolderInHomeDrive(folderName):
    ''' Creates a folder in the users home folder. Can take an input of a directory
    pathway defined using back slashes, such as "TempFolder/default_folder/new_directory". '''
    # Define path name
    filePath = Path.home()/folderName
    
    # Check if folder already exists
    if (os.path.exists(filePath) != True):
        print("Creating Directory: %s"%filePath)
        os.makedirs(filePath)
    else:
        print("Directory already exists. No folders created")
    
    # Return the path
    return filePath

def generateFileName(folder, fileName, ext):
    ''' Creates a filename that does not exist in the folder passed to the function. Returns the path
    to the file, which can be used in an open() function. '''
    # Declare variables
    i = 0
    modFileName = fileName
        
    # Get path to file
    filePath = folder/("%s.%s"%(modFileName, ext))
    
    # If file already exists, add numbers to it, until an unused filename is generated
    while os.path.isfile(filePath):
        i = i+1
        modFileName = fileName+str(i)
        filePath = folder/("%s.%s"%(modFileName, ext))
        
    # Return the modified filename
    return filePath

def zipFolder(folderPath):
    ''' Makes a zip archive of the directory passed to the function. '''
    
    # Check if folder exists
    if (os.path.exists(folderPath)):
        shutil.make_archive(folderPath, 'zip', folderPath)
        print("Archive made in %s.zip"%folderPath)
    else:
        print("Path doesn't exist. No archive made.")
    
    # Return path
    return "%s.zip"%folderPath

def documentComputerInfoInJson(folder, fileName):
    ''' Creates a JSON file in the folder passed to the function, storing information about the 
    computer running the script.'''
    # Create the output folder
    folderPath = createFolderInMainDrive(folder)
    
    # Get the proper file name
    filePath = generateFileName(folderPath, fileName, 'json')
    
    # Generate computer info
    computerInfo = {}
    computerInfo['Date'] = datetime.now().strftime('%m/%d/%Y')
    computerInfo['Time'] = datetime.now().strftime('%H:%M')
    computerInfo['Computer Information'] = {
        'ID': os.environ['COMPUTERNAME'],
        'MAC Address': '%X'%get_mac(),
        'Operating System': "%s %s"%(platform.system(), platform.version()),
        'Processor': platform.machine()
    }
    
    # Write to JSON file
    with open(filePath, 'w') as outfile:
        json.dump(computerInfo, outfile, indent=4)
    
    # End script
    print("JSON created in %s"%filePath)
    return folderPath
    
def main():
    ''' Example of using JSON writer, and archiving the folder '''
    
    folderPath = "ComputerInformation/JSONfiles"
    folderPath = documentComputerInfoInJson(folderPath, 'Info')
    
    # Make archive
    zipFolder(folderPath)
    
    
if __name__ == '__main__':
    main()
    
    