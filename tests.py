import os
import shutil

import string
from pathlib import Path


# TODO Add Unit Tests

def create_test_files(folder_path: Path):
    create_empty_file("Test - Normal Path 2023.opus", folder_path)  # Album Name: Normal Path - Album Date: 2023
    create_empty_file("T.e.s.t - N.o.r.m.a.l P.a.t.h 2.0.2.3.opus", folder_path)  #TODO Album Name: Normal Path - Album Date: 2023
    create_empty_file("Test - 1999 2023.opus", folder_path) #TODO Album Name: 1999 - Album Date: 2023
    create_empty_file("Test - 1999-2016 2023.opus", folder_path) #TODO Album Name: 1999-2016 - Album Date: 2023
    create_empty_file("R̲o̲b̲b̲i̲e̲ W̲i̲l̲l̲i̲a̲m̲s̲ - L̲i̲f̲e̲ T̲h̲r̲u̲ A̲ L̲e̲n̲s̲.opus", folder_path)
    create_empty_file("Th̲e Cur̲e̲ – Thre̲e̲ Imagi̲n̲ary B̲oys.opus", folder_path)
    create_empty_file("B̤ṳf̤f̤a̤l̤o̤ ̤V̤o̤l̤c̤a̤n̤i̤c̤ ̤- R̤o̤c̤k̤ 1973.opus", folder_path)
    create_empty_file("Th̲e Cur̲e̲ – Thre̲e̲ Imagi̲n̲ary B̲oys.opus", folder_path)
    create_empty_file("The Beatles - Magical Mystery Tour [Full Album] (1967).opus", folder_path)
    create_empty_file("Tschaikowsky - Nocturne d-Moll ∙ hr-Sinfonieorchester ∙ Mischa Maisky ∙ Paavo Järvi.opus",
                      folder_path)


def create_empty_file(file_name: string, folder_path: Path) -> bool:
    try:
        file_path: string = os.path.join(str(folder_path) + "/" + file_name)
        shutil.copy("./emptyOpusFile.opus", file_path)
        return True
    except Exception as ex:
        print("ERROR: Create empty file: " + str(ex))
        return False


def delete_all_files_in_folder(folder_path: string):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            os.remove(os.path.join(root, file))
