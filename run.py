from DriveClass import Drive, IS_NOT_ANY_FILE
import datetime
import os

file = input("Введите путь к файлу: \n")
if file[0]=='"' and file[-1]=='"':
    file=file[1:len(file)-1]
while (not os.path.exists(file)):
    file = input("Неверное имя! Введите путь к файлу: \n")
    if file[0]=='"' and file[-1]=='"':
        file=file[1:len(file)-1]

drive = Drive(file[:file.find(":")])
set_file_bytes = drive.get_file_as_set_bytes(file)
print("Происходит поиск одинаковых секторов, ожидайте.")

start=datetime.datetime.now()
files_and_sectors=drive.find_equals_sectors_by_file(set_file_bytes)
end=datetime.datetime.now()

print(f"Поиск завершен за", end-start)
print("Ожидайте. Сейчас будут найдены оставшиеся одинаковые блоки.")

result_file=open("result.txt",'w+t')
result_file.writelines(drive.get_result_for_everyone_file(files_and_sectors,set_file_bytes))
result_file.close()
print("Готово!")



