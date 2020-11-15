import glob
import os
import hashlib
import shutil
import sys


def get_file_md5(filename):
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            md5_hash.update(b)
    return md5_hash.hexdigest()


def delete_dir(base_path, dirname ,recursive=False):
    for dir in os.listdir(base_path):
        if os.path.isdir(base_path + '/' + dir):
            if dir == dirname:
                print(f"remove {base_path + '/' + dir}")
                shutil.rmtree(base_path + '/' + dir)
            elif recursive:
                delete_dir(base_path + '/' + dir, dirname, recursive)


def delete_node_module(base_path, recursive=False):
    delete_dir(base_path, 'node_modules', recursive)


def delete_maven_module(base_path, recursive=False):
    delete_dir(base_path, 'target', recursive)


def delete_dup(base_path, recursive=False):
    if not base_path.endswith('/'):
        base_path = base_path + '/'
    base_path = base_path + '**'
    md5_file_list = []
    file_list = glob.glob(base_path, recursive=recursive)
    for file in file_list:
        if os.path.isfile(file):
            if os.path.getsize(file) / 1024 / 1024 < 300:
                file_md5 = get_file_md5(file)
                if file_md5 in md5_file_list:
                    os.remove(file)
                    print(f'删除文件 {file}')
                else:
                    md5_file_list.append(file_md5)


usage = '''
Usage: [option] <type> file_path

delete useless file.

Example:
  node  /Users/zhangyunan/project/       # 删除 /Users/zhangyunan/project/ 目录下的 node_module 文件
  -r maven /Users/zhangyunan/project/    # 递归删除 /Users/zhangyunan/project/ 目录下的 target 文件

option:
  -r      递归删除

type:
  -n, node             node_module 文件
  -m, maven            target 文件
  -d, dup              根据md5sum 删除相同的文件
'''

if __name__ == '__main__':
    argv_count = len(sys.argv)
    if argv_count == 1:
        print(usage)
    elif argv_count == 2:
        print(usage)
    elif argv_count == 3:
        if sys.argv[1] == '-r':
            print(usage)
        elif not os.path.exists(sys.argv[2]):
            print(f'{sys.argv[2]} is not exists')
        elif not os.path.isdir(sys.argv[2]):
            print(f'{sys.argv} is not a dir')
        elif sys.argv[1] == '-n' or sys.argv[1] == 'node':
            delete_node_module(sys.argv[2])
        elif sys.argv[1] == '-d' or sys.argv[1] == 'dup':
            delete_dup(sys.argv[2])
        elif sys.argv[1] == '-m' or sys.argv[1] == 'maven':
            delete_maven_module(sys.argv[2])
        else:
            print('怎么回事呀')
            print(usage)
    elif argv_count == 4 and sys.argv[1] == '-r':
        if not os.path.exists(sys.argv[3]):
            print(f'{sys.argv[3]} is not exists')
        elif not os.path.isdir(sys.argv[3]):
            print(f'{sys.argv[3]} is not a dir')
        elif sys.argv[2] == '-n' or sys.argv[2] == 'node':
            delete_node_module(sys.argv[3], True)
        elif sys.argv[2] == '-d' or sys.argv[2] == 'dup':
            delete_dup(sys.argv[3], True)
        elif sys.argv[2] == '-m' or sys.argv[2] == 'maven':
            delete_maven_module(sys.argv[3], True)
        else:
            print('怎么回事呀')
            print(usage)
    else:
        print(usage)
