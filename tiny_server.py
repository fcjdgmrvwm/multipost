from bottle.bottle import *
import threading

def new_app(homepage ,root, port):
    app = Bottle()
    @app.route('/')
    def callback():
        return static_file(homepage, root=root)
    @app.route('/<path:path>')
    def callback(path):
        if path=='/':
            return static_file(homepage, root=root)
        return static_file(path, root=root)
    run(app, host="localhost", port=port)

apps = []
appnum = 3
for i in range(appnum):
    apps.append(threading.Thread(target=new_app, args=('index.html', 'web/zjsgcc', 8080+i)))
apps.append(threading.Thread(target=new_app, args=('index1.html', 'web/zjsgcc', 8080+appnum)))
apps.append(threading.Thread(target=new_app, args=('index1.html', 'web/zjsgcc', 8080+appnum+1)))
# controller
apps.append(threading.Thread(target=new_app, args=('index1.html', 'web/zjsgcc', 12345)))

for i in apps:
    i.start()

for i in apps:
    threading.Thread.join(i)