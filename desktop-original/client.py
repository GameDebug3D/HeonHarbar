import os
import sys
import time
import socket
import threading
import http.server
import socketserver
import traceback

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")


def resource_dir():
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


BASE = resource_dir()
APP_TITLE = "Neon Harbor"
LOCAL_PORT = int(os.environ.get("HARBOR_CLIENT_PORT", "5173"))
WINDOW_W = int(os.environ.get("HARBOR_WIN_W", "1360"))
WINDOW_H = int(os.environ.get("HARBOR_WIN_H", "800"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)

    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


def free_port(start):
    for p in range(start, start + 40):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    return start


def serve(port):
    socketserver.TCPServer.allow_reuse_address = True

    class Server(socketserver.ThreadingTCPServer):
        daemon_threads = True

    with Server(("127.0.0.1", port), Handler) as httpd:
        httpd.serve_forever()


def log_path():
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), "NeonHarbor_log.txt")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "NeonHarbor_log.txt")


def log(msg):
    try:
        with open(log_path(), "a", encoding="utf-8") as f:
            f.write("[%s] %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass


class Api:
    def __init__(self):
        self.window = None

    def set_fullscreen(self, flag):
        try:
            if self.window is None:
                return False
            flag = bool(flag)
            if bool(getattr(self.window, "fullscreen", False)) != flag:
                self.window.toggle_fullscreen()
            return True
        except Exception:
            log("set_fullscreen failed\n" + traceback.format_exc())
            return False

    def set_size(self, w, h):
        try:
            if self.window is None:
                return False
            if bool(getattr(self.window, "fullscreen", False)):
                self.window.toggle_fullscreen()
            self.window.resize(int(w), int(h))
            return True
        except Exception:
            log("set_size failed\n" + traceback.format_exc())
            return False

    def minimize(self):
        try:
            self.window.minimize()
            return True
        except Exception:
            return False

    def quit(self):
        try:
            if self.window is not None:
                self.window.destroy()
            return True
        except Exception:
            return False


def load_webview():
    try:
        import webview
        log("webview package ok")
        return webview
    except Exception:
        log("import webview failed\n" + traceback.format_exc())
    if getattr(sys, "frozen", False):
        return None
    log("pywebview missing - trying pip install (one time, needs internet)")
    print("[client] pywebview is missing - trying to install it (needs internet, one time)...")
    sys.stdout.flush()
    import subprocess
    for args in (["-m", "pip", "install", "--user", "pywebview"],
                 ["-m", "pip", "install", "pywebview"],
                 ["-m", "pip", "install", "--user", "pywebview", "-i",
                  "https://pypi.tuna.tsinghua.edu.cn/simple"]):
        try:
            subprocess.check_call([sys.executable] + args)
        except Exception:
            continue
        try:
            import webview
            log("pywebview installed")
            print("[client] pywebview installed.")
            return webview
        except Exception:
            continue
    return None


def main():
    log("client start, base=%s" % BASE)
    if not os.path.exists(os.path.join(BASE, "index.html")):
        log("index.html missing in %s" % BASE)
        print("[client] index.html not found")
        return

    port = free_port(LOCAL_PORT)
    threading.Thread(target=serve, args=(port,), daemon=True).start()
    url = "http://127.0.0.1:%d/" % port

    print("=" * 52)
    print("  %s  -  desktop client" % APP_TITLE)
    print("=" * 52)
    print("  Game files served at %s" % url)
    print("  Single player needs no server.")
    print("  To play with friends, enter the server IP and port")
    print("  on the launcher screen (the host runs server.py).")
    print("  Press Ctrl+C to stop.")
    print("=" * 52)
    sys.stdout.flush()

    webview = load_webview()
    if webview is None:
        log("pywebview unavailable, opening in the default browser instead")
        print("[client] pywebview unavailable - falling back to your default browser.")
        import webbrowser
        webbrowser.open(url)
        if not getattr(sys, "frozen", False):
            input("Press Enter to quit...")
        else:
            time.sleep(60)
        return

    log("pywebview %s, backend=edgechromium, opening %s" % (getattr(webview, "__version__", "?"), url))
    api = Api()
    window = webview.create_window(APP_TITLE, url, width=WINDOW_W, height=WINDOW_H,
                                   min_size=(1000, 640), text_select=False,
                                   confirm_close=False, js_api=api)
    api.window = window
    window.events.loaded += lambda: window.maximize()
    print("[client] Embedded browser window opened.")
    sys.stdout.flush()
    webview.start(private_mode=False)
    log("window closed")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("FATAL\n" + traceback.format_exc())
        raise
