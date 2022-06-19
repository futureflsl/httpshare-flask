import os
import time
from flask import Flask, render_template, url_for, redirect, send_from_directory,request

# 共享文件夹的根目录
rootdir = '/home/fut/'

app = Flask(__name__)


@app.route('/')
def main():
   return get_file_list(rootdir)


def get_file_list(dir):
    file_list=[]
    for file in os.listdir(dir):
        if file[0]=='.':
            continue
        file_list.append(os.path.join(dir,file).replace(rootdir,''))
    print('get file list:',file_list)
    contents = []
    for file in sorted(file_list):
        fullpath = os.path.join(rootdir,file)
        content = {}
        content['filename'] = file
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(fullpath).st_mtime))
        content['size'] = str(round(os.path.getsize(fullpath) / 1024 / 1024)) + 'M'
        contents.append(content)
    return render_template('index.html', contents=contents, ossep=os.sep)


@app.route('/data')
def downloader():
    fullname=request.args.get("fullname")
    print('fullname=',fullname)
    fullname = os.path.join(rootdir, fullname)
    print('fullname join=',fullname)
    if os.path.isdir(fullname):
        return get_file_list(fullname)
    else:
        filename = fullname.split(os.sep)[-1]
        dirpath = fullname[:-len(filename)]
        return send_from_directory(dirpath, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(port=5200)
