import os
import time
from flask import Flask, render_template, url_for, redirect, send_from_directory

# 共享文件夹的根目录
rootdir = '/home/fut/share'

app = Flask(__name__)


@app.route('/')
def main():
   return get_file_list(rootdir)


def get_file_list(dir):
    file_list = os.listdir(dir)
    contents = []
    for file in sorted(file_list):
        fullpath = dir + os.sep + file
        # 如果是目录，在后面添加一个sep
        if os.path.isdir(fullpath):
            file += os.sep
        content = {}
        content['filename'] = file
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(fullpath).st_mtime))
        content['size'] = str(round(os.path.getsize(fullpath) / 1024 / 1024)) + 'M'
        contents.append(content)
    return render_template('index.html', contents=contents, ossep=os.sep)


@app.route('/<fullname>/')
def downloader(fullname):
    fullname = rootdir + os.sep + fullname
    if os.path.isdir(fullname):
        return get_file_list(fullname)
    else:
        filename = fullname.split(os.sep)[-1]
        dirpath = fullname[:-len(filename)]
        return send_from_directory(dirpath, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(port=5006)
