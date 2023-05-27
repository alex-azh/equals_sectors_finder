import os
from DriveClass import Drive
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


d = Drive("C")
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
