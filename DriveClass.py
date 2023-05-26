import subprocess
import math
IS_NOT_ANY_FILE="is not in any file"

def chunk(lst, n, start=0):
    """Разделение списка на равные части.

    Args:
        lst (list): список для разделения.
        n (int): количество, на которое будет разделен список.

    Yields:
        list: часть списка.
    """
    for i in range(start, len(lst), n):
        yield lst[i:i+n]


class Drive:
    """Диск для работы с байтовыми представлениями на нём.
    """
    def __init__(self, driveWord: str, sector_size: int = 512, max_bytes_read: int = 104857600):
        self.drive_word = driveWord
        self.path = fr'\\.\{driveWord}:'
        self.sector_size = sector_size
        self.max_bytes_read = max_bytes_read

    @staticmethod
    def get_bytes_from_file_as_sector_size(path, sector_size):
        """Итератор наборов байт, равных заданному размеру сектора на диске.

        Args:
            path (str): путь к файлу (может быть путь к диску).
            sector_size (int): размер сектора на диске.

        Yields:
            bytes: набор байт, размером в сектор.
        """
        try:
            with open(path, 'rb') as f:
                while (True):
                    b = f.read(sector_size)
                    if not b:
                        break
                    yield b
        except Exception as ex:
            print(ex)

    @staticmethod
    def IsZeroBytes(b):
        """Проверяет, являются ли байты набором пустых строк.

        Args:
            b (bytes): набор байт для проверки.

        Returns:
            bool: True, если байты содержат в основном пробелы, иначе - False
        """
        zero = 0
        for i in b:
            if i == 32 or i==0 or i==255:
                zero += 1
        return zero/len(b) > 0.9

    def get_file_as_set_bytes(self, filepath):
        """Получить уникальные байты по-секторно из файла.

        Args:
            filepath (str): путь к файлу.

        Returns:
            set(): уникальный список типа set.
        """
        myfile = set()
        for b in Drive.get_bytes_from_file_as_sector_size(filepath, self.sector_size):
            if not Drive.IsZeroBytes(b):
                myfile.add(b)
        return myfile

    def find_equals_sectors_by_file(self, set_file_bytes):
        """Найти одинаковые секторы на текущем диске по указанному набору байт, принадлежащих файлу.

        Args:
            set_file_bytes (set): set из байтов у заданного файла.

        Returns:
            dict: cловарь, ключ: имя файла, значение: набор строк [начало-конец] - секторов.
        """
        sectors_in_max_bytes_read = self.max_bytes_read//self.sector_size
        drive_sectors = Drive.get_bytes_from_file_as_sector_size(
            self.path, self.max_bytes_read)
        all_sectors={IS_NOT_ANY_FILE: []}
        start_chunk=0
        chunk_size=math.ceil(self.max_bytes_read/self.sector_size)
        for i, b in enumerate(drive_sectors):
            start_chunk=0
            while(start_chunk<=chunk_size):
                cnt=self.sector_size*start_chunk
                part_b = b[cnt:cnt+self.sector_size]
                if part_b in set_file_bytes:
                    sector=i * sectors_in_max_bytes_read+start_chunk
                    name, sectors=self.get_filename_with_sectors_by_sector(sector)
                    if name==IS_NOT_ANY_FILE:
                        all_sectors[IS_NOT_ANY_FILE].append(sectors)
                        start_chunk+=1
                        continue
                    else:
                        # прыгнуть сразу на конечный сектор в отрезке
                        if not all_sectors.get(name):
                            all_sectors[name]=sectors
                        for range in sectors:
                            values=range.split("-")
                            start_sector,end_sector=int(values[0]),int(values[1])
                            if sector>=start_sector and sector<=end_sector:
                                # v2 внутри текущего сhunk или выходит за пределы 
                                if end_sector<=chunk_size*i:
                                    # продолжить текущие циклы
                                    start_chunk+=end_sector-sector+1
                                else:
                                    # в след.порции 100 мб будет проход смещен
                                    next=True
                                break
                        if next:
                            next=False
                            break # завершение в сhunk
                else:
                    start_chunk+=1
        return all_sectors

    def get_filename_with_sectors_by_sector(self, sector):
        """Получить имя файла по заданному сектору и все остальные принадлежащие файлу номера секторов на диске.

        Args:
            sector (int): номер сектора на данном диске.

        Returns:
            str, list(str): имя файла по данному сектору, набор адресов в виде строки 'начало-конец', принадлежащие данному файлу.
        """
        result = subprocess.run(
            fr"nfi.exe {self.drive_word}: {sector}", capture_output=True)
        if result.returncode == 1:
            return "Ошибка в исполнении nfi.exe. Возможно, неверно указан путь к программе.", []
        result = result.stdout.decode()
        index = result.find(IS_NOT_ANY_FILE)
        if index != -1:
            return IS_NOT_ANY_FILE, []
        else:
            sectors = []
            name = result[result.find(".",result.find("***"))+4:result.find("    ")-3]
            logical_sectors = "logical sectors "
            index = result.find(logical_sectors)
            while (index != -1):
                result = result[index+len(logical_sectors):]
                local_index = result.find("(")
                sectors.append(result[:local_index-1])
                result = result[local_index:]
                index = result.find(logical_sectors)
            return name, sectors
    
    # TODO: не работает.
    def set_zero_sector(self,sector):
        try:
            with open(self.path, 'rb+') as f:
                f.seek(self.sector_size*sector)
                f.write(bytes(self.sector_size))
        except Exception as ex:
            print(ex)

    # TODO: не работает.
    def set_zero_sectors_with_start_count(self,start_sector, count):
        try:
            with open(self.path, 'rb+') as f:
                f.seek(self.sector_size*start_sector)
                f.write(bytes(self.sector_size*count))
        except Exception as ex:
            print(ex)

    def get_sector(self,sector):
        try:
            with open(self.path, 'rb') as f:
                f.seek(self.sector_size*sector)
                b=f.read(self.sector_size)
            return b
        except Exception as ex:
            print(ex)
    
    def get_seq_sectors(self,sector,count):
        try:
            with open(self.path, 'rb') as f:
                f.seek(self.sector_size*sector)
                for i in range(count):
                    b = f.read(self.sector_size)
                    if not b:
                        break
                    yield b
            return b
        except Exception as ex:
            print(ex)
    
    def get_result_for_everyone_file(self,files_and_sectors: dict, file_set: set):
        while(len(files_and_sectors)>0):
            result_string=""
            item=files_and_sectors.popitem()
            result_string+=f"Файл: \n{item[0]}\n\nСекторы "
            ss=""
            for range in item[1]:
                ss+=f"{range} "
            result_string+=ss
            eq=[]
            for range in item[1]:
                values=range.split("-")
                start_sector,end_sector=int(values[0]), int(values[1])
                count=end_sector-start_sector+1
                for i,b in enumerate(self.get_seq_sectors(sector=start_sector,count=count)):
                    if b in file_set:
                        eq.append(start_sector+i)
            eq_count=len(eq)
            procent=eq_count/len(file_set)
            result_string+='\n'
            result_string+=f"Одинаковые: {eq_count}, % = {procent}:\n"
            result_string+=",".join(map(str,eq))
            result_string+='\n\n'
            yield result_string