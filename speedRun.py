import os
from DriveClass import Drive, chunk
from datetime import datetime as dt


def get_filename():
    file = input("Введите путь к файлу: \n")
    if file[0] == '"' and file[-1] == '"':
        file = file[1:len(file)-1]
    while (not os.path.exists(file)):
        file = input(
            "Неверное имя! Введите путь к файлу: \n")
        if file[0] == '"' and file[-1] == '"':
            file = file[1:len(file)-1]
    return file


def get_time_iteration_on_disk(iterations, sector_count=1):
    start = dt.now()
    for i, b in enumerate(Drive.get_bytes_from_file_as_sector_size(d.path, d.sector_size*sector_count)):
        if (i == iterations):
            break
    end = dt.now()
    return end-start

def get_time_iteration_on_disk_with_set(iterations, file_set: set, sector_count=1):
    start = dt.now()
    for i, b in enumerate(Drive.get_bytes_from_file_as_sector_size(d.path, d.sector_size*sector_count)):
        if (i == iterations):
            break
        for part in chunk(b,512):
            if part in file_set:
                pass
    end = dt.now()
    return end-start

d = Drive("C")

def get_time_iterations():
    # 1гб по 512 байт = 1073741824 байт или по 512байт секторов - 2097152
    # будем считать по 100мб в буфер, 200, 50 мб.

    # 100 мб в 1гб = 10 циклов, в 100 мб 204800 секторов.
    print(get_time_iteration_on_disk(10, 204800))

    # 200 мб в 1гб = 5 циклов, в 200 мб 409600 секторов.
    print(get_time_iteration_on_disk(5, 409600))

    # 64 мб в 1гб = 16 циклов, в 64 мб 131072 секторов.
    print(get_time_iteration_on_disk(16, 131072))

    # 0:00:00.650670 - 100 мб
    # 0:00:00.741837 - 200 мб
    # 0:00:00.698289 - 64 мб
    # вывод - 100 мб оптимальный способ чтения.

    # 100 мб в 20гб = 200 циклов, в 100 мб 204800 секторов.
    print(get_time_iteration_on_disk(200, 204800))

    # 200 мб в 20гб = 5 циклов, в 200 мб 409600 секторов.
    print(get_time_iteration_on_disk(100, 409600))

    # 64 мб в 20гб = 16 циклов, в 64 мб 131072 секторов.
    print(get_time_iteration_on_disk(320, 131072))

    # 0:00:11.429399
    # 0:00:11.554083
    # 0:00:11.772447
    # вывод - 100мб чтения остаются оптимальным вариантом.

def get_time_iterations_set(file_set:set):
    # 1гб по 512 байт = 1073741824 байт или по 512байт секторов - 2097152
    # будем считать по 100мб в буфер, 200, 50 мб.

    # 100 мб в 1гб = 10 циклов, в 100 мб 204800 секторов.
    print(get_time_iteration_on_disk_with_set(10,file_set, 204800))

    # 200 мб в 1гб = 5 циклов, в 200 мб 409600 секторов.
    print(get_time_iteration_on_disk_with_set(5,file_set, 409600))

    # 64 мб в 1гб = 16 циклов, в 64 мб 131072 секторов.
    print(get_time_iteration_on_disk_with_set(16,file_set, 131072))

    # 100 мб в 20гб = 200 циклов, в 100 мб 204800 секторов.
    print(get_time_iteration_on_disk_with_set(200,file_set, 204800))

    # 200 мб в 20гб = 5 циклов, в 200 мб 409600 секторов.
    print(get_time_iteration_on_disk_with_set(100,file_set, 409600))

    # 64 мб в 20гб = 16 циклов, в 64 мб 131072 секторов.
    print(get_time_iteration_on_disk_with_set(320,file_set, 131072))

    # 0:00:02.239386
    # 0:00:02.342898
    # 0:00:02.235027
    # 0:00:41.631407
    # 0:00:41.762049
    # 0:00:41.969329
    # вывод - 100мб чтения остаются оптимальным вариантом.

file_set=d.get_file_as_set_bytes(r"C:\Users\digital\Downloads\vs_BuildTools.exe")
get_time_iterations_set(file_set)