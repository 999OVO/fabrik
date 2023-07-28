import os
import shutil
import time
def opencardsZip(image_id):
    filename = '07-25'
    name = 'unit_test-opencard-0725'  # unit_test-opencard-0725
    abs_path = os.getcwd()  # D:\study-nn\nn\project\fab_test\fa_test\fa_test
    print('abs_path', abs_path)
    file_path = abs_path + '\\' + name.rsplit('.', 1)[0]
    print('file_path', file_path)

    if os.path.exists(file_path + '\\images\\{}\\'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename)):
        shutil.rmtree(file_path + '\\images\\{}\\'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename))
        time.sleep(1)

    # os.makedirs(abs_path + '\\images\\{}'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename), 0o777)
    os.makedirs(file_path + '\\images\\{}\\'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename,image_id), 0o777)
    # os.makedirs(file_path + '\\images\\{}\\'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename), 0o777)
    # os.makedirs(abs_path + '\\images\\{}\\{}'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename, image_id), 0o777)

    shutil.copytree(
        abs_path + '\\images\\{}\\{}'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename,
                                             image_id),
        file_path + '\\images\\{}\\{}'.format(str(time.strftime("%Y", time.localtime())) + '-' + filename,
                                              image_id))


opencardsZip(image_id='abc')




