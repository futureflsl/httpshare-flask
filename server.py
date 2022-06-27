import os
import time
from flask import Flask, render_template, url_for, redirect, send_from_directory, request

# 共享文件夹的根目录
rootdir = '/home/fut/'

app = Flask(__name__)


@app.route('/')
def main():
    return get_file_list(rootdir)


def get_file_list(dir):
    file_list = []
    for file in os.listdir(dir):
        if file[0] == '.':
            continue
        file_list.append(file)
    #print('get file list:', file_list)
    contents = []
    for file in sorted(file_list):
        fullpath = os.path.join(dir, file)
        content = {}
        content['filename'] = file
        content['dir'] = dir
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(fullpath).st_mtime))
        if os.path.isdir(fullpath):
            content['size'] ='0M'
        else:
            content['size'] = str(round(os.path.getsize(fullpath) / 1024 / 1024)) + 'M'
        contents.append(content)
    return render_template('index.html', contents=contents, ossep=dir)


@app.route('/data')
def downloader():
    filename = request.args.get("filename")
    dir = request.args.get("rootdir")
    fullname = os.path.join(dir, filename)
    if os.path.isdir(fullname):
        return get_file_list(fullname)
    else:
        return send_from_directory(dir, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(port=5200)
