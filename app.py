import webview
import threading
import http.server
import socketserver
import os
import time

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")

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

def inject_auto_back_handler(window):
    js = """
    if (!window.__back_timer_started) {
      window.__back_timer_started = true;
      setTimeout(() => {
          window.location.href = "/";
      }, 180000); // 3분
    }
    """
    window.evaluate_js(js)

def monitor_page(window):
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
                    inject_auto_back_handler(window)

            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

if __name__ == '__main__':
    threading.Thread(target=start_server, daemon=True).start()

    window = webview.create_window(
        "Daybird Kiosk",
        f"http://localhost:{PORT}/",
        width=600,
        height=1024,
        resizable=False,
        frameless=False
    )

    webview.start(func=lambda: threading.Thread(target=monitor_page, args=(window,), daemon=True).start())
