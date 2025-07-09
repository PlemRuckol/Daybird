import webview  # pip install pywebview
import threading
import http.server
import socketserver
import os
import time
from datetime import datetime

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")

timer_reset_event = threading.Event()
timer_lock = threading.Lock()
timer_start_time = None

class SPARequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not os.path.exists(self.translate_path(self.path)) and "." not in self.path:
            self.path = "/index.html"
        return super().do_GET()

def start_server():
    os.chdir(DIST_DIR)
    handler = SPARequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

def reset_timer():
    global timer_start_time
    with timer_lock:
        timer_start_time = datetime.now()
    timer_reset_event.set()
    timer_reset_event.clear()
    print("[INFO] Timer reset.")

def auto_back_countdown(window):
    while True:
        with timer_lock:
            start_time = timer_start_time
        elapsed = (datetime.now() - start_time).total_seconds()

        if elapsed >= 180:
            print("[INFO] 3분 경과. / 으로 이동")
            window.evaluate_js('window.location.href = "/"')
            break

        timer_reset_event.wait(timeout=1)

def inject_touch_handler(window):
    js = """
    document.addEventListener('click', () => {
        window.location.href = "/chat";
    }, { once: true });
    document.addEventListener('touchstart', () => {
        window.location.href = "/chat";
    }, { once: true });
    """
    window.evaluate_js(js)

def inject_js_reset_timer(window):
    js = """
    function notifyPython() {
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.reset_timer();
        }
    }

    new MutationObserver(() => {
        notifyPython();
    }).observe(document.body, { childList: true, subtree: true });

    document.addEventListener('click', notifyPython);
    document.addEventListener('touchstart', notifyPython);
    """
    window.evaluate_js(js)

def monitor_page(window):
    global timer_start_time
    last_url = ""
    while True:
        try:
            current_url = window.get_current_url()
            if current_url != last_url:
                last_url = current_url
                print(f"[INFO] URL changed to: {current_url}")

                if current_url.endswith("/"):
                    inject_touch_handler(window)
                elif current_url.endswith("/chat"):
                    reset_timer()
                    inject_js_reset_timer(window)
                    threading.Thread(target=auto_back_countdown, args=(window,), daemon=True).start()

            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

class JSBridge:
    def reset_timer(self):
        reset_timer()

if __name__ == '__main__':
    threading.Thread(target=start_server, daemon=True).start()

    window = webview.create_window(
        "Daybird Kiosk",
        f"http://localhost:{PORT}/",
        width=600,
        height=1024,
        resizable=False,
        frameless=False,
        js_api=JSBridge()
    )

    webview.start(
        func=lambda: threading.Thread(target=monitor_page, args=(window,), daemon=True).start(),
        gui='qt',
        debug=True
    )
