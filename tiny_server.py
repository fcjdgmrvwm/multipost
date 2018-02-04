from locallib.bottle import *
import threading

def path_fix(path):
    flag = 0
    bpath = ""
    for i in path:
        if i == '/':
            if flag == 0:
                bpath += "/"
                flag = 1
        else:
            bpath += i
            flag = 0
    return bpath

def new_app(homepage ,root, port):
    app = Bottle()
    @app.route('/')
    def callback():
        return static_file(homepage, root=root)
    @app.route('/<path:path>')
    def callback(path):
        path = path_fix(path)
        if path=='/':
            return static_file(homepage, root=root)
        return static_file(path, root=root)
    run(app, host="localhost", port=port)

apps = []
appnum = 3
myweb = "../../multipost/web/zjsgcc/"

for i in range(appnum):
    apps.append(threading.Thread(target=new_app, args=('index.html', myweb, 8080+i)))
apps.append(threading.Thread(target=new_app, args=('index1.html', myweb, 8080+appnum)))
apps.append(threading.Thread(target=new_app, args=('index1.html', myweb, 8080+appnum+1)))
# controller
apps.append(threading.Thread(target=new_app, args=('index1.html', myweb, 12345)))

for i in apps:
    i.start()

for i in apps:
    threading.Thread.join(i)