from bottle import route, run, template, static_file, abort, redirect
from os import listdir,remove
from os.path import isfile, isdir, join, dirname

filesPath = join(dirname(__file__), 'files')

def toLink(n, f):
    return template('<li><a href="/download/{{n}}" download="{{n}}">{{text}}</a> <a href="/delete/{{n}}" class="del">&times;</a></li>', n=n, text=f)

def getFiles():
    filesDict = dict()
    for f in listdir(filesPath):
        filesDict[str(hash(f))] = f  
    return filesDict

@route('/')
def index():
    return redirect('/files')

@route('/files')
def files():
    html = ['<style>.del {color:red;text-decoration:none}</style><ul>']
    files = getFiles()
    for key in files.keys():
        html.append(toLink(key, files[key]))
    html.append('</ul>')
    return '\n'.join(html)

@route('/download/<n>')
def download(n):
    files = getFiles()
    if n not in files:
        abort(404, 'file not found - ' + n)
    return static_file(files[n], root=filesPath)

@route('/delete/<n>')
def delete(n):
    files = getFiles()
    if n not in files:
        abort(404, 'no such file')
    remove(join(filesPath, files[n]))
    return redirect('/files')

run(host='localhost', port=8080)
