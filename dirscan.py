import os
import pathlib


directory = 'tmp/'

def listdir_base(directory):
    """ Показывает доступные файлы """
    files = os.listdir(directory)
    for i in range(len(files)):
        print(i, "|", files[i])

def listdir(directory):
    """ Показывает доступные файлы """
    files = os.listdir(directory)
    tmp = ""
    counter=0
    for i in range(len(files)):
        counter=i
        tmp = tmp + str(counter + 1) + " | " + files[i] + '\n'
    return tmp
    
def listdir_returnpath(directory, number):
    """ Возвращает путь к файлу """
    if(number > 0):
        file_path = directory
        number = number - 1
        files = os.listdir(directory)
        for i in range(len(files)):
            if(i == number):
                file_path = file_path + files[i]
                return file_path

def listdir_countfile(directory):
    """ Показывает количесво доступных файлов """
    files = os.listdir(directory)
    return len(files)

#print(listdir_countfile(directory))
#print(listdir(directory))
#print(listdir_returnpath(directory, 7))