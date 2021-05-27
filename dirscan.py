import os
import pathlib

# directory = 'tmp/'

# def listdir_base(directory):
#     """ Показывает доступные файлы """
#     files = os.listdir(directory)
#     for i in range(len(files)):
#         print(i, "|", files[i])

def listdir(directory):
    """ Показывает доступные файлы """
    files = os.listdir(directory)
    tmp = ""
    counter=0
    for i in range(len(files)):
        counter=i
        tmp = tmp + str(counter + 1) + " | " + files[i] + '\n'
    return tmp
    
# def listdir_returnpath(directory, number):
#     """ Возвращает путь к файлу """
#     if(number > 0):
#         file_path = directory
#         number = number - 1
#         files = os.listdir(directory)
#         for i in range(len(files)):
#             if(i == number):
#                 file_path = file_path + files[i]
#                 return file_path

def listdir_countfile(directory):
    """ Показывает количесво доступных файлов """
    files = os.listdir(directory)
    return len(files)

# Создание репозиотрия пользователя, если он уже есть - вернет 1
# если его нет, создаёт его и возвращает 0
def create_dir(directory, name):
    """ Создание и проверка репозиотрия пользователя """
    nmdir= directory + name
    if os.path.exists(nmdir):
        return 1
    else:
        os.mkdir(nmdir)
        return 0

# Показывает доступные файлы для пользователя
def listdir_user(diruser):
    """ Показывает доступные файлы """
    files = os.listdir(diruser)
    tmp = ""
    counter=0
    for i in range(len(files)):
        counter=i
        tmp = tmp + str(counter + 1) + " | " + files[i] + '\n'
    return tmp

# Возвращает путь к файлу пользователя по его запросу
def listdir_returnpath_user(diruser, number):
    """ Возвращает путь к файлу пользователя"""
    if(number > 0): 
        file_path = diruser
        number = number - 1
        files = os.listdir(diruser)
        for i in range(len(files)):
            if(i == number):
                file_path = file_path + files[i]
                return file_path

def take_file_from_sql():
    """ """