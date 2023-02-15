from flask import Flask, jsonify, request, render_template
import json
import base64
import os
import time
from img_generator import ImgGenerator
import threading 

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# class ImgPool(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.imgs = []
# 
#     def run(self):
#         pass

class ImgPool(threading.Thread):
    def __init__(self, size=100) -> None:
        threading.Thread.__init__(self)
        # super().__init__(self)
        self.imgs = []
        self.size = size
        self.last = ""
        self.img_gen = ImgGenerator()
        self.sem = threading.Semaphore(size)

    def run(self):
        while True:
            self.sem.acquire()
            img, args = self.img_gen.get_random_img()
            self.imgs.append((img, args))

    def get_img(self):
        if len(self.imgs) == 0:
            return self.last

        if len(self.imgs) > 0:
            ret = self.imgs.pop(0)
            self.sem.release()

        self.last = ret
        return ret
    
    def get_last(self):
        return self.last

img_pool = ImgPool(size=100)
img_pool.daemon = True
img_pool.start()

@app.route('/')
def get_picture():
    img_stream, args = img_pool.get_img()
    # render_template()函数是flask函数，它从模版文件夹templates中呈现给定的模板上下文。
    return render_template('index.html',img_stream=img_stream, args=json.dumps(args, indent=4))

folder = "favorite"
@app.route("/like", methods=["GET"])
def like():
    last, _ = img_pool.get_last()
    filename = f"{time.time_ns()}.png"
    open(os.path.join(folder, filename), "wb").write(base64.b64decode(last))
    return "ok"
  
if __name__ == '__main__':
    # app.run(host, port, debug, options)
    app.run(host="0.0.0.0", port=7861)