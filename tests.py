import os
import shutil

import string


def create_test_files(folderPath: string):
    create_empty_file("R̲o̲b̲b̲i̲e̲ W̲i̲l̲l̲i̲a̲m̲s̲ - L̲i̲f̲e̲ T̲h̲r̲u̲ A̲ L̲e̲n̲s̲.opus", folderPath)
    create_empty_file("Th̲e Cur̲e̲ – Thre̲e̲ Imagi̲n̲ary B̲oys.opus", folderPath)
    create_empty_file("B̤ṳf̤f̤a̤l̤o̤ ̤V̤o̤l̤c̤a̤n̤i̤c̤ ̤- R̤o̤c̤k̤ 1973.opus", folderPath)
    create_empty_file("Th̲e Cur̲e̲ – Thre̲e̲ Imagi̲n̲ary B̲oys.opus", folderPath)
    create_empty_file("The Beatles - Magical Mystery Tour [Full Album] (1967).opus", folderPath)
    create_empty_file("Tschaikowsky - Nocturne d-Moll ∙ hr-Sinfonieorchester ∙ Mischa Maisky ∙ Paavo Järvi.opus", folderPath)


def create_empty_file(fileName: string, folderPath: string) -> bool:
    try:
        filePath: string = os.path.join(folderPath + fileName)
        shutil.copy("./emptyOpusFile.opus", filePath)
        return True
    except Exception as ex:
        print("ERROR: Create empty file: " + str(ex))
        return False
