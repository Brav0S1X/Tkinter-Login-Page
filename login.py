from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk, Image
from datetime import datetime
from gtts import gTTS
from time import sleep as slp
from io import BytesIO
from multicolorcaptcha import CaptchaGenerator as CG
import cairosvg, hashlib, platform, threading, webbrowser, uuid, socket, sys, os, re, requests as req

def clear_terminal():
    command = "cls" if os.name == "nt" else "clear"
    try:
        os.system(command)
    except Exception:
        pass

def safe_resize(image, size):
    try:
        return image.resize(size, Image.Resampling.LANCZOS)
    except AttributeError:
        return image.resize(size, Image.LANCZOS)

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.currentDir = os.path.dirname(os.path.abspath(__file__))
        self.vcmd_alpha = (self.master.register(self.validate_alphanumeric), "%P")
        self.vcmd_pass = (self.master.register(self.validate_password), "%P")
        self.vcmd_digit = (self.master.register(self.validate_digits), "%P")
        self.current_theme = "dark"
        self.current_audio_file = None
        self.current_captcha_text = ""
        self.current_captcha_answer = ""
        self.current_captcha_id = None
        self.show_password = "*"
        self.tap_window = None
        self.network_watchdog_running = False
        self.apply_theme_variables("dark")
        self.texts = {
            "title": "Sign In",
            "setting": "⚙️ Setting",
            "theme": "🎨 | Theme",
            "about_menu": "👥 About",
            "help": "❔ Help",
            "light_theme": "🔆 | Light theme",
            "dark_theme": "🌙 | Dark theme",
            "welcome": "Welcome Dear user;\nTo use the program, just enter your username & password",
            "need_new": "or call                        if u need a new one!",
            "support": "SUPPORT",
            "login_info": "Login Informations",
            "bot_verification": "Bot Verification",
            "username": "Username:",
            "password": "Password:",
            "captcha_placeholder": " write your ANSWER Here...",
            "agreement": "By click on this, you agreed to our                          &",
            "privacy": "PRIVACY POLICY",
            "terms": "TERMS of USE",
            "login": "LOGIN",
            "help_text": "Enter username, password, solve captcha, accept terms, then click LOGIN.",
            "captcha_not_ready": "Captcha is not ready yet.",
            "audio_error": "Something went wrong while creating/playing captcha audio.",
            "captcha_question": "What is the answer to equation {equation}?",
            "username_only_numbers": "Username cannot be only numbers!",
            "captcha_no_data": "Please enter the numbers which you see in image, at captcha section\n\nCannot See Numbers?\n    [1] Use listener\n    [2] Refresh CAPTCHA",
            "captcha_invalid": "You cannot enter anything except numbers in CAPTCHA Field!",
            "captcha_wrong": "Captcha code does not match!",
            "password_empty": "Password field cannot be empty!",
            "username_empty": "Please enter something in the Username field as your username!\nEx: John1234",
            "network_error": "Make sure that you are connected to an internet server!",
            "wrong_login": "Username or Password is not correct!",
            "expired": "Your Login Data has been expired.\nContact support to get a new one!",
            "logged_in": "Now! You logged in :) Thx for using this repo",
            "terms_title": "Terms and privacy policy",
            "terms_header": "Read this to avail our services:",
            "done": "DONE"
        }
        self.svg_icons = {
            "eye_on": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 499 499"><g transform="translate(0 499) scale(.1 -.1)" fill="#ADFF2F"><path d="M2405 3581 c-11 -4 -65 -11 -120 -15 -199 -12 -521 -86 -672 -152 -17 -8 -35 -14 -39 -14 -14 0 -255 -116 -330 -158 -363 -209 -660 -516 -657 -682 2 -133 227 -388 523 -591 685 -471 1610 -561 2435 -236 107 42 324 154 390 201 16 11 37 26 46 31 97 61 151 106 269 225 286 290 290 430 18 711 -163 168 -338 293 -573 407 -150 74 -193 92 -330 137 -127 43 -325 91 -435 105 -227 31 -489 46 -525 31z m309 -262 c140 -47 227 -106 337 -228 62 -69 119 -227 126 -346 21 -399 -441 -735 -832 -605 -672 223 -597 1077 105 1204 51 9 205 -5 264 -25z m-856 -62 c2 -9 -7 -30 -21 -46 -167 -199 -205 -573 -83 -819 60 -122 68 -133 150 -217 207 -211 567 -320 806 -245 19 6 58 17 85 25 62 17 180 71 196 91 6 8 16 14 21 14 32 0 169 133 229 221 180 266 179 644 -2 897 -81 114 -8 124 196 27 17 -8 55 -25 85 -38 125 -56 152 -70 267 -141 190 -117 428 -338 475 -441 21 -46 -75 -187 -194 -287 -29 -24 -62 -52 -74 -63 -38 -34 -52 -44 -142 -104 -165 -109 -309 -183 -467 -241 -633 -231 -1349 -194 -1906 100 -163 87 -207 114 -349 218 -89 66 -316 291 -330 328 -20 53 78 171 291 349 147 123 432 280 656 361 37 13 69 27 72 29 10 11 36 -1 39 -18z"/></g></svg>',
            "eye_out": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 499 499"><g transform="translate(0 499) scale(.1 -.1)" fill="#ADFF2F"><path d="M2330 3549 c-164 -13 -398 -58 -517 -98 -34 -12 -69 -21 -78 -21 -9 0 -35 -9 -57 -20 -23 -11 -46 -20 -51 -20 -22 0 -322 -141 -392 -185 -371 -229 -605 -474 -605 -631 0 -126 250 -397 535 -579 33 -21 76 -48 95 -61 48 -31 326 -165 364 -175 17 -4 69 -21 116 -38 144 -50 263 -78 480 -115 60 -10 631 -7 695 4 179 30 452 96 533 129 28 11 76 30 105 42 201 80 478 232 495 271 2 5 8 8 14 8 37 0 338 297 338 334 0 3 10 20 23 39 55 80 53 198 -3 276 -11 16 -20 32 -20 36 0 4 -27 40 -61 80 -135 163 -370 338 -615 456 -71 34 -141 68 -155 75 -37 19 -176 67 -285 98 -80 23 -169 43 -339 76 -137 26 -417 35 -615 19z m555 -209 c143 -17 375 -75 522 -131 366 -139 727 -389 842 -585 36 -61 18 -100 -118 -239 -122 -125 -326 -267 -506 -354 -38 -18 -78 -37 -88 -43 -356 -184 -1059 -253 -1502 -147 -287 69 -498 158 -760 322 -73 45 -202 144 -234 180 -14 15 -31 27 -38 27 -6 0 -33 26 -60 57 -26 31 -60 70 -75 86 -45 48 -38 80 35 164 307 353 868 622 1400 672 121 11 454 6 582 -9z"/><path d="M770 1919 c-117 -72 -140 -95 -140 -139 0 -73 81 -108 141 -62 13 10 45 30 70 45 108 62 137 120 84 172 -35 36 -77 32 -155 -16z"/><path d="M4156 1924 c-22 -21 -31 -62 -20 -93 9 -27 177 -146 221 -157 81 -21 126 97 59 153 -113 92 -224 134 -260 97z"/><path d="M1324 1653 c-21 -4 -33 -17 -115 -121 -95 -121 -5 -258 98 -149 152 160 161 296 17 270z"/><path d="M3693 1650 c-74 -30 -65 -90 29 -210 85 -108 137 -125 178 -57 35 56 12 105 -119 258 -11 13 -66 18 -88 9z"/><path d="M1893 1412 c-12 -9 -27 -37 -33 -62 -6 -25 -20 -73 -32 -106 -34 -105 39 -185 120 -129 25 19 74 167 76 231 2 75 -73 112 -131 66z"/><path d="M3089 1409 c-39 -39 17 -280 68 -300 94 -36 148 46 104 158 -10 26 -22 64 -26 83 -16 76 -97 108 -146 59z"/><path d="M2500 1348 c-25 -14 -43 -205 -25 -275 15 -61 122 -57 146 5 14 35 8 247 -7 262 -18 18 -86 22 -114 8z"/></g></svg>',
            "headphone": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 499 499"><g transform="translate(0 499) scale(.1 -.1)" fill="#ADFF2F"><path d="M2310 4244 c-14 -3 -77 -14 -140 -26 -235 -43 -449 -130 -655 -266 -55 -36 -109 -74 -120 -83 -119 -104 -207 -192 -269 -269 -20 -25 -41 -50 -46 -57 -29 -35 -139 -216 -164 -268 -15 -33 -34 -71 -41 -85 -87 -170 -136 -419 -142 -735 l-5 -260 -42 -40 c-277 -271 -185 -740 168 -858 94 -32 85 -111 89 701 l3 717 27 105 c90 357 299 694 537 868 19 14 40 31 45 37 22 23 163 110 255 156 522 262 1183 195 1638 -165 54 -42 269 -262 295 -301 156 -231 214 -359 275 -600 l26 -100 3 -718 c4 -811 -5 -732 89 -700 360 120 447 633 148 875 -20 17 -22 28 -27 280 -4 169 -11 286 -21 328 -7 36 -19 90 -26 120 -22 103 -81 263 -148 400 -15 30 -93 153 -171 269 -79 118 -320 328 -501 437 -288 175 -805 288 -1080 238z"/><path d="M1994 2736 c-27 -20 -36 -1892 -9 -1933 17 -25 62 -32 83 -11 22 22 17 1927 -5 1944 -23 17 -45 17 -69 0z"/><path d="M1220 2654 c-112 -40 -169 -99 -190 -194 -17 -82 -10 -1380 9 -1434 72 -214 418 -198 469 23 19 84 17 1371 -3 1437 -33 111 -189 203 -285 168z"/><path d="M3660 2651 c-90 -29 -152 -88 -175 -165 -20 -67 -22 -1377 -2 -1442 67 -223 403 -232 469 -13 18 62 19 1394 1 1455 -36 115 -186 200 -293 165z"/><path d="M2360 2481 c-7 -13 -10 -258 -10 -725 l0 -706 24 -15 c29 -19 71 -4 80 29 15 56 6 1391 -10 1414 -20 28 -69 30 -84 3z"/><path d="M2170 2394 c-18 -47 -8 -1273 10 -1284 26 -17 69 -11 80 9 14 27 14 1255 0 1282 -17 31 -78 26 -90 -7z"/><path d="M2550 2180 c-27 -27 -32 -789 -4 -828 20 -28 69 -30 84 -3 21 39 13 815 -8 834 -25 22 -48 21 -72 -3z"/><path d="M1807 2112 c-15 -17 -17 -55 -17 -346 0 -359 1 -366 55 -366 54 0 55 7 55 364 0 313 -1 327 -20 346 -25 25 -52 26 -73 2z"/><path d="M2742 1974 c-29 -20 -35 -390 -6 -418 23 -24 61 -20 79 8 26 40 18 392 -9 412 -25 18 -36 18 -64 -2z"/><path d="M2919 1884 c-46 -56 -15 -264 40 -264 51 0 86 179 49 250 -17 31 -68 39 -89 14z"/><path d="M3106 1844 c-25 -24 -22 -138 4 -164 46 -46 90 -9 90 77 0 95 -45 137 -94 87z"/><path d="M1608 1785 c-15 -34 12 -75 50 -75 45 0 65 36 46 84 -11 28 -82 21 -96 -9z"/><path d="M3286 1795 c-18 -49 1 -85 45 -85 67 0 70 93 3 98 -31 2 -43 -1 -48 -13z"/></g></svg>',
            "refresh": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 499 499"><g transform="translate(0 499) scale(.1 -.1)" fill="#ADFF2F"><path d="M2305 4254 c-163 -16 -441 -88 -532 -138 -16 -8 -59 -29 -97 -47 -38 -17 -81 -39 -95 -48 -14 -10 -46 -31 -71 -47 -147 -94 -324 -256 -429 -392 -44 -57 -141 -203 -141 -212 0 -25 -30 -30 -72 -11 -120 54 -161 71 -169 71 -5 0 -34 12 -65 26 -31 14 -58 23 -61 20 -6 -5 9 -145 32 -306 8 -52 17 -129 20 -170 4 -41 15 -131 25 -200 10 -69 23 -172 30 -230 27 -256 39 -313 58 -285 6 9 346 268 432 330 15 11 107 81 205 155 97 74 187 142 199 150 107 72 121 94 69 111 -21 7 -53 20 -71 31 -18 10 -37 18 -42 18 -5 0 -39 14 -75 30 -36 17 -69 30 -74 30 -72 0 146 268 329 404 83 62 189 121 283 156 28 12 61 25 72 30 187 86 630 78 875 -17 225 -88 488 -286 596 -452 16 -24 41 -62 56 -85 15 -22 39 -63 52 -91 39 -79 36 -77 87 -60 24 8 62 24 84 34 22 10 65 29 95 41 184 77 201 87 189 117 -26 70 -141 267 -191 328 -4 5 -22 28 -39 50 -342 450 -974 716 -1564 659z"/><path d="M4095 2590 c-71 -54 -134 -102 -140 -107 -5 -4 -100 -76 -210 -158 -370 -279 -460 -349 -460 -358 0 -7 35 -24 190 -89 115 -48 115 -48 115 -73 0 -13 -6 -30 -12 -37 -7 -7 -33 -40 -57 -73 -70 -95 -284 -295 -316 -295 -3 0 -21 -11 -38 -24 -255 -191 -738 -248 -1097 -130 -327 109 -622 363 -757 654 -32 69 -40 71 -119 35 -30 -14 -57 -25 -60 -25 -3 0 -24 -8 -47 -19 -23 -10 -79 -35 -123 -55 -45 -20 -86 -36 -92 -36 -22 0 -21 -20 5 -76 128 -280 401 -588 655 -739 167 -99 318 -165 478 -209 751 -206 1569 112 1974 767 58 93 58 93 104 74 335 -141 312 -136 301 -64 -5 28 -18 131 -29 228 -11 97 -24 201 -29 230 -5 30 -14 104 -21 164 -6 61 -18 155 -25 210 -8 55 -20 146 -27 203 -14 123 -3 123 -163 2z"/></g></svg>'
        }
        self.master.title(self.t("title"))
        self.master.geometry("374x519")
        self.master.resizable(0, 0)
        self.master.config(bg=self.dfbg)
        self.create_menu()
        self.create_widgets()
        self.start_network_watchdog()

    def t(self, key):
        return self.texts.get(key, key)

    def is_connected(self):
        test_hosts = [
            ("1.1.1.1", 53),
            ("8.8.8.8", 53)
        ]
        for host, port in test_hosts:
            try:
                socket.create_connection((host, port), timeout=2).close()
                return True
            except OSError:
                continue
        return False

    def start_network_watchdog(self):
        self.network_watchdog_running = True
        threading.Thread(target=self._network_watchdog_loop, daemon=True).start()

    def handle_network_loss(self):
        try:
            msg.showerror("Network Error", "Internet connection lost. The program will close.")
        except Exception:
            pass
        try:
            self.network_watchdog_running = False
            self.master.destroy()
        except Exception:
            os._exit(0)

    def _network_watchdog_loop(self):
        while getattr(self, "network_watchdog_running", False):
            try:
                if not self.is_connected():
                    self.master.after(0, self.handle_network_loss)
                    break
            except Exception:
                self.master.after(0, self.handle_network_loss)
                break
            for _ in range(10):
                if not getattr(self, "network_watchdog_running", False):
                    return
                slp(1)

    def validate_alphanumeric(self, value):
        if value == "":
            return True
        return bool(re.fullmatch(r"[a-zA-Z0-9]*", value))

    def validate_password(self, value):
        if value == "":
            return True
        return bool(re.fullmatch(r"[a-zA-Z0-9@#$%^&*()\-_=\+\[\]{};:,.<>/?!|\\]*", value))

    def validate_digits(self, value):
        if value == "" or value == self.t("captcha_placeholder"):
            return True
        return value.isdigit()

    def apply_theme_variables(self, theme):
        self.current_theme = theme
        if theme == "light":
            self.dfbg = "#F5F5F5"
            self.entry_bg = "#FFFFFF"
            self.primary_fg = "#0F5132"
            self.secondary_fg = "#6C4E00"
            self.button_fg = "#104E8B"
            self.login_button_bg = "#DFF6DD"
            self.login_button_fg = "#006400"
            self.disabled_button_bg = "#D5D5D5"
            self.disabled_button_fg = "#777777"
            self.text_bg = "#FFFFFF"
            self.text_fg = "#222222"
        else:
            self.dfbg = "#1F1F1F"
            self.entry_bg = "#3D3D3D"
            self.primary_fg = "#ADFF2F"
            self.secondary_fg = "#FFF68F"
            self.button_fg = "#FFF68F"
            self.login_button_bg = "#FFF68F"
            self.login_button_fg = "Green"
            self.disabled_button_bg = "#3D3D3D"
            self.disabled_button_fg = "#1F1F1F"
            self.text_bg = "#3D3D3D"
            self.text_fg = "#FFF68F"

    def render_svg_as_image(self, svg_xml, color, size=(20, 20)):
        colored_svg = re.sub(r'fill="[^"]+"', f'fill="{color}"', svg_xml)
        png_data = cairosvg.svg2png(
            bytestring=colored_svg.encode("utf-8"),
            output_width=size[0],
            output_height=size[1]
        )
        return ImageTk.PhotoImage(Image.open(BytesIO(png_data)))

    def set_theme(self, theme):
        try:
            self.apply_theme_variables(theme)
            self.apply_theme()
            self.create_menu()
        except Exception as error:
            msg.showerror("Theme Error", f"Failed to apply theme: {error}")

    def update_icons(self):
        icon_color = self.primary_fg
        self.img_eye_on = self.render_svg_as_image(self.svg_icons["eye_on"], icon_color)
        self.img_eye_out = self.render_svg_as_image(self.svg_icons["eye_out"], icon_color)
        self.img_headphone = self.render_svg_as_image(self.svg_icons["headphone"], icon_color)
        self.img_refresh = self.render_svg_as_image(self.svg_icons["refresh"], icon_color)
        if hasattr(self, "log_pwd_show"):
            current_eye = self.img_eye_out if self.show_password == "" else self.img_eye_on
            self.log_pwd_show.config(image=current_eye)
        if hasattr(self, "get_captcha_listen_btn"):
            self.get_captcha_listen_btn.config(image=self.img_headphone)
        if hasattr(self, "get_new_captcha_btn"):
            self.get_new_captcha_btn.config(image=self.img_refresh)

    def apply_theme(self):
        self.master.config(bg=self.dfbg)
        background_widgets = [
            "login_hint_01",
            "login_hint_02",
            "login_support_button",
            "log_main_login_frame",
            "log_main_bot_verification",
            "log_usr_lbl",
            "log_pwd_lbl",
            "log_pwd_show",
            "captcha_image_label",
            "get_captcha_listen_btn",
            "get_new_captcha_btn",
            "get_agreement",
            "agreement_txt_label",
            "privacy",
            "terms",
            "agreement_txt_done"
        ]
        for name in background_widgets:
            widget = getattr(self, name, None)
            if widget:
                try:
                    widget.config(bg=self.dfbg)
                except Exception:
                    pass
        for name in ["log_usr_ent", "log_pwd_ent", "get_captcha"]:
            widget = getattr(self, name, None)
            if widget:
                try:
                    widget.config(bg=self.entry_bg, fg=self.primary_fg)
                except Exception:
                    pass
        for name in ["login_hint_01", "login_hint_02", "agreement_txt_label", "agreement_txt_done"]:
            widget = getattr(self, name, None)
            if widget:
                try:
                    widget.config(fg=self.primary_fg)
                except Exception:
                    pass
        for name in ["log_usr_lbl", "log_pwd_lbl", "login_support_button", "privacy", "terms"]:
            widget = getattr(self, name, None)
            if widget:
                try:
                    widget.config(fg=self.secondary_fg)
                except Exception:
                    pass
        for name in ["log_main_login_frame", "log_main_bot_verification"]:
            widget = getattr(self, name, None)
            if widget:
                try:
                    widget.config(fg=self.primary_fg)
                except Exception:
                    pass
        if hasattr(self, "get_logging_in"):
            if self.get_agreement_accepted.get():
                self.get_logging_in.config(bg=self.login_button_bg, fg=self.login_button_fg)
            else:
                self.get_logging_in.config(bg=self.disabled_button_bg, fg=self.disabled_button_fg)
        if hasattr(self, "svg_icons"):
            self.update_icons()

    def create_menu(self):
        menubar = Menu(self.master, fg=self.secondary_fg, bg=self.dfbg, bd=0)
        submenu_setting = Menu(menubar, tearoff=0, fg=self.secondary_fg, bg=self.dfbg, bd=0)
        submenu_theme = Menu(submenu_setting, tearoff=0, fg=self.secondary_fg, bg=self.dfbg, bd=0)
        submenu_theme.add_command(label=self.t("light_theme"), command=lambda: self.set_theme("light"))
        submenu_theme.add_command(label=self.t("dark_theme"), command=lambda: self.set_theme("dark"))
        submenu_setting.add_cascade(label=self.t("theme"), menu=submenu_theme)
        menubar.add_cascade(label=self.t("setting"), menu=submenu_setting)
        menubar.add_command(label=self.t("about_menu"), command=self.submenu_about)
        menubar.add_command(label=self.t("help"), command=self.help_dialog)
        self.master.config(menu=menubar)
        self.menubar = menubar

    def cleanup_captcha_audio(self):
        if not self.current_audio_file:
            return
        try:
            if os.path.exists(self.current_audio_file):
                os.remove(self.current_audio_file)
        except PermissionError:
            pass
        except Exception:
            pass
        finally:
            self.current_audio_file = None

    def cleanup_old_captcha_audios(self):
        try:
            for filename in os.listdir(self.currentDir):
                if filename.startswith("captcha_") and filename.endswith(".mp3"):
                    path = os.path.join(self.currentDir, filename)
                    try:
                        os.remove(path)
                    except Exception:
                        pass
        except Exception:
            pass

    def captcha(self):
        captcha_generator = CG(2)
        captcha_data = captcha_generator.gen_math_captcha_image(
            multicolor=True,
            margin=False,
            difficult_level=5
        )
        image = captcha_data["image"]
        image = image.crop(image.getbbox())
        captcha_path = os.path.join(self.currentDir, "captcha.png")
        image.save(captcha_path, "PNG")
        self.current_captcha_text = str(captcha_data["equation_str"])
        self.current_captcha_answer = str(captcha_data["equation_result"])
        self.current_captcha_id = uuid.uuid4().hex

    def render_captcha_image(self):
        captcha_path = os.path.join(self.currentDir, "captcha.png")
        if not os.path.exists(captcha_path):
            self.captcha()
        image = Image.open(captcha_path)
        image = safe_resize(image, (image.width // 2, image.height))
        self.my_captcha = ImageTk.PhotoImage(image)
        if hasattr(self, "captcha_image_label") and self.captcha_image_label:
            self.captcha_image_label.config(image=self.my_captcha)
            self.captcha_image_label.image = self.my_captcha
            return
        self.captcha_image_label = Label(
            self.log_main_bot_verification,
            image=self.my_captcha,
            bg=self.dfbg,
            highlightthickness=1,
            highlightcolor="#9C9C9C"
        )
        self.captcha_image_label.place(x=16, y=10)

    def set_captcha_placeholder(self):
        if hasattr(self, "captcha_get"):
            self.captcha_get.set(self.t("captcha_placeholder"))
        if hasattr(self, "get_captcha"):
            self.get_captcha.config(fg=self.primary_fg)
            self.get_captcha.icursor(0)

    def clear_captcha_input(self):
        if hasattr(self, "captcha_get"):
            self.captcha_get.set("")
        if hasattr(self, "get_captcha"):
            self.get_captcha.config(fg=self.secondary_fg)

    def new_captcha(self):
        self.cleanup_captcha_audio()
        self.captcha()
        self.render_captcha_image()
        self.set_captcha_placeholder()
        if hasattr(self, "get_captcha"):
            self.get_captcha.focus_set()

    def reset_login_form(self):
        self.cleanup_captcha_audio()
        if hasattr(self, "usr_get"):
            self.usr_get.set("")
        if hasattr(self, "pwd_get"):
            self.pwd_get.set("")
        self.show_password = "*"
        if hasattr(self, "log_pwd_ent"):
            self.log_pwd_ent.config(show="*")
        if hasattr(self, "log_pwd_show"):
            try:
                self.log_pwd_show.config(image=self.img_eye_on)
            except Exception:
                pass
        if hasattr(self, "get_agreement_accepted"):
            self.get_agreement_accepted.set(False)
        if hasattr(self, "get_logging_in"):
            self.get_logging_in.config(
                command=None,
                fg=self.disabled_button_fg,
                bg=self.disabled_button_bg
            )
        self.new_captcha()

    def listen_captcha(self):
        if not self.current_captcha_text:
            msg.showerror("Error", self.t("captcha_not_ready"))
            return
        self.cleanup_captcha_audio()
        spoken_equation = (
            self.current_captcha_text
            .replace("-", " minus ")
            .replace("+", " plus ")
            .replace("*", " multiplied by ")
            .replace("/", " divided by ")
        )
        sound_text = self.t("captcha_question").format(equation=spoken_equation)
        audio_name = f"captcha_{self.current_captcha_id}.mp3"
        audio_path = os.path.join(self.currentDir, audio_name)
        captcha_id_snapshot = self.current_captcha_id

        def worker():
            try:
                captcha_sound = gTTS(text=sound_text, lang="en")
                captcha_sound.save(audio_path)
                def play_on_main_thread():
                    if captcha_id_snapshot != self.current_captcha_id:
                        try:
                            if os.path.exists(audio_path):
                                os.remove(audio_path)
                        except Exception:
                            pass
                        return
                    self.current_audio_file = audio_path
                    try:
                        if platform.system() == "Windows":
                            os.startfile(audio_path)
                        else:
                            msg.showinfo("Audio", f"Audio file created:\n{audio_path}")
                    except Exception as error:
                        msg.showerror("Error", f"{self.t('audio_error')}\n\n{error}")
                self.master.after(0, play_on_main_thread)
            except Exception as error:
                self.master.after(
                    0,
                    lambda: msg.showerror("Error", f"{self.t('audio_error')}\n\n{error}")
                )
        threading.Thread(target=worker, daemon=True).start()

    def create_widgets(self):
        self.cleanup_old_captcha_audios()
        self.captcha()
        self.login_hint_01 = Label(
            self.master,
            text=self.t("welcome"),
            font=("Ebrima", 10, "bold"),
            fg=self.primary_fg,
            bg=self.dfbg,
            justify=LEFT
        )
        self.login_hint_01.pack(anchor="w", padx=6, pady=(4, 0))
        self.login_hint_02 = Label(
            self.master,
            text=self.t("need_new"),
            font=("Ebrima", 9, "bold"),
            fg=self.primary_fg,
            bg=self.dfbg,
            justify=LEFT
        )
        self.login_hint_02.place(x=4, y=42)
        self.login_support_button = Button(
            self.master,
            text=self.t("support"),
            command=self.support,
            font=("Ebrima", 9, "bold", "underline"),
            fg=self.secondary_fg,
            bg=self.dfbg,
            bd=0
        )
        self.login_support_button.place(x=46, y=42)
        self.log_main_login_frame = LabelFrame(
            self.master,
            text=self.t("login_info"),
            font=("Ebrima", 9, "bold"),
            fg=self.primary_fg,
            bg=self.dfbg,
            width=358,
            height=90
        )
        self.log_main_login_frame.place(x=7, y=70)
        self.log_main_bot_verification = LabelFrame(
            self.master,
            text=self.t("bot_verification"),
            font=("Ebrima", 9, "bold"),
            fg=self.primary_fg,
            bg=self.dfbg,
            width=358,
            height=218
        )
        self.log_main_bot_verification.place(x=7, y=175)
        self.log_usr_lbl = Label(
            self.log_main_login_frame,
            text=self.t("username"),
            font=("Ebrima", 10, "bold"),
            fg=self.secondary_fg,
            bg=self.dfbg
        )
        self.log_usr_lbl.place(x=4, y=4)
        self.usr_get = StringVar()
        self.log_usr_ent = Entry(
            self.log_main_login_frame,
            width=38,
            textvariable=self.usr_get,
            font=("Ebrima", 10),
            fg=self.primary_fg,
            bg=self.entry_bg,
            bd=0,
            validate="key",
            validatecommand=self.vcmd_alpha
        )
        self.log_usr_ent.place(x=78, y=7)
        self.log_pwd_lbl = Label(
            self.log_main_login_frame,
            text=self.t("password"),
            font=("Ebrima", 10, "bold"),
            fg=self.secondary_fg,
            bg=self.dfbg
        )
        self.log_pwd_lbl.place(x=4, y=34)
        self.pwd_get = StringVar()
        self.log_pwd_ent = Entry(
            self.log_main_login_frame,
            width=34,
            textvariable=self.pwd_get,
            show="*",
            font=("Ebrima", 10),
            fg=self.primary_fg,
            bg=self.entry_bg,
            bd=0,
            validate="key",
            validatecommand=self.vcmd_pass
        )
        self.log_pwd_ent.place(x=78, y=37)
        self.load_password_eye_images()
        self.log_pwd_show = Button(
            self.log_main_login_frame,
            image=self.on_target_photo,
            command=self.pwd_check,
            bg=self.dfbg,
            bd=0
        )
        self.log_pwd_show.place(x=322, y=36)
        self.render_captcha_image()
        self.captcha_get = StringVar()
        self.get_captcha = Entry(
            self.log_main_bot_verification,
            width=38,
            textvariable=self.captcha_get,
            font=("Ebrima", 10),
            fg=self.primary_fg,
            bg=self.entry_bg,
            highlightthickness=1,
            highlightcolor="#9C9C9C",
            validate="key",
            validatecommand=self.vcmd_digit
        )
        self.set_captcha_placeholder()
        self.get_captcha.bind("<FocusIn>", self.on_captcha_focus_in)
        self.get_captcha.bind("<FocusOut>", self.on_captcha_focus_out)
        self.get_captcha.place(x=16, y=155)
        self.load_captcha_button_images()
        self.get_captcha_listen_btn = Button(
            self.log_main_bot_verification,
            image=self.headphone_photo,
            command=self.listen_captcha,
            bd=0,
            bg=self.dfbg
        )
        self.get_captcha_listen_btn.place(x=320, y=155)
        self.get_new_captcha_btn = Button(
            self.log_main_bot_verification,
            image=self.refresh_photo,
            command=self.new_captcha,
            bd=0,
            bg=self.dfbg
        )
        self.get_new_captcha_btn.place(x=293, y=155)
        self.get_logging_in = Button(
            self.master,
            text=self.t("login"),
            command=None,
            font=("Segoe UI", 12, "bold"),
            fg=self.disabled_button_fg,
            bg=self.disabled_button_bg,
            bd=0,
            padx=148
        )
        self.get_logging_in.place(x=10, y=475)
        self.get_agreement_accepted = BooleanVar()
        self.get_agreement = Checkbutton(
            self.master,
            text="",
            variable=self.get_agreement_accepted,
            command=self.agreement_changed,
            fg="Red",
            bg=self.dfbg,
            bd=0,
            activebackground=self.dfbg
        )
        self.get_agreement.place(x=6, y=410)
        self.agreement_txt_label = Label(
            self.master,
            text=self.t("agreement"),
            font=("Ebrima", 10, "bold"),
            fg=self.primary_fg,
            bg=self.dfbg
        )
        self.agreement_txt_label.place(x=25, y=408)
        self.privacy = Button(
            self.master,
            text=self.t("privacy"),
            command=self.terms_n_privacy,
            font=("Ebrima", 9, "bold", "underline"),
            fg=self.secondary_fg,
            bg=self.dfbg,
            bd=0
        )
        self.privacy.place(x=243, y=410)
        self.terms = Button(
            self.master,
            text=self.t("terms"),
            command=self.terms_n_privacy,
            font=("Ebrima", 9, "bold", "underline"),
            fg=self.secondary_fg,
            bg=self.dfbg,
            bd=0
        )
        self.terms.place(x=26, y=432)
        self.agreement_txt_done = Label(
            self.master,
            text=".",
            font=("Ebrima", 10, "bold"),
            fg=self.primary_fg,
            bg=self.dfbg
        )
        self.agreement_txt_done.place(x=108, y=432)
        self.apply_theme()

    def load_password_eye_images(self):
        eyes_on_path = os.path.join(self.currentDir, "eyes_on.png")
        eyes_out_path = os.path.join(self.currentDir, "eyes_out.png")
        if os.path.exists(eyes_on_path):
            image = Image.open(eyes_on_path)
            image = safe_resize(image, (max(1, image.width // 160), max(1, image.height // 160)))
            self.on_target_photo = ImageTk.PhotoImage(image)
        else:
            self.on_target_photo = PhotoImage(width=20, height=20)
        if os.path.exists(eyes_out_path):
            image = Image.open(eyes_out_path)
            image = safe_resize(image, (max(1, image.width // 160), max(1, image.height // 160)))
            self.out_of_target_photo = ImageTk.PhotoImage(image)
        else:
            self.out_of_target_photo = PhotoImage(width=20, height=20)

    def load_captcha_button_images(self):
        headphone_path = os.path.join(self.currentDir, "Headphone.png")
        refresh_path = os.path.join(self.currentDir, "Refresh.png")
        if os.path.exists(headphone_path):
            image = Image.open(headphone_path)
            image = safe_resize(image, (max(1, image.width // 145), max(1, image.height // 145)))
            self.headphone_photo = ImageTk.PhotoImage(image)
        else:
            self.headphone_photo = PhotoImage(width=20, height=20)
        if os.path.exists(refresh_path):
            image = Image.open(refresh_path)
            image = safe_resize(image, (max(1, image.width // 145), max(1, image.height // 145)))
            self.refresh_photo = ImageTk.PhotoImage(image)
        else:
            self.refresh_photo = PhotoImage(width=20, height=20)

    def on_captcha_focus_in(self, event=None):
        current_value = self.captcha_get.get().strip()
        placeholder = self.t("captcha_placeholder").strip()
        if current_value == placeholder:
            self.clear_captcha_input()
        else:
            self.get_captcha.config(fg=self.secondary_fg)

    def on_captcha_focus_out(self, event=None):
        if self.captcha_get.get().strip() == "":
            self.set_captcha_placeholder()
        else:
            self.get_captcha.config(fg=self.secondary_fg)

    def agreement_changed(self):
        if self.get_agreement_accepted.get():
            self.get_logging_in.config(
                command=self.log_in,
                fg=self.login_button_fg,
                bg=self.login_button_bg
            )
        else:
            self.get_logging_in.config(
                command=None,
                fg=self.disabled_button_fg,
                bg=self.disabled_button_bg
            )
        self.get_logging_in.place(x=10, y=475)

    def pwd_check(self):
        if self.show_password == "*":
            self.show_password = ""
            self.log_pwd_ent.config(show=self.show_password)
            self.log_pwd_show.config(image=self.img_eye_out)
        else:
            self.show_password = "*"
            self.log_pwd_ent.config(show=self.show_password)
            self.log_pwd_show.config(image=self.img_eye_on)

    def support(self):
        webbrowser.open("mailto:contact@mrkia.ir?subject=Help%20Request", new=2)

    def submenu_about(self):
        webbrowser.open("https://github.com/Brav0S1X/Tkinter-Login-Page", new=2)

    def help_dialog(self):
        msg.showinfo("Help", self.t("help_text"))

    def terms_n_privacy(self):
        if self.tap_window is not None and self.tap_window.winfo_exists():
            self.tap_window.lift()
            return
        tap = Toplevel(self.master)
        self.tap_window = tap
        tap.title(self.t("terms_title"))
        tap.geometry("374x365")
        tap.resizable(0, 0)
        tap.config(bg=self.dfbg)
        tap.transient(self.master)
        tap.grab_set()
        tap_msg = Label(
            tap,
            text=self.t("terms_header"),
            font=("Ebrima", 10, "bold"),
            bg=self.dfbg,
            fg="#1E90FF",
            justify=LEFT
        )
        tap_msg.place(x=2, y=2)
        tap_terms_text = Text(
            tap,
            width=49,
            height=17,
            wrap=WORD,
            font=("Ebrima", 10, "bold"),
            bg=self.text_bg,
            fg=self.text_fg,
            bd=0
        )
        tap_terms_text.place(x=6, y=30)
        tap_scrollbar = Scrollbar(tap, orient=VERTICAL, command=tap_terms_text.yview)
        tap_scrollbar.pack(side=RIGHT, fill=Y)
        tap_terms_text.config(yscrollcommand=tap_scrollbar.set)
        url = "https://raw.githubusercontent.com/Brav0S1X/Tkinter-Login-Page/main/agreement.txt"
        try:
            response = req.get(url, timeout=5)
            if response.status_code == 200:
                tap_terms_text.insert(INSERT, response.text)
            else:
                tap_terms_text.insert(
                    INSERT,
                    f"Error: Could not load terms (Status: {response.status_code})"
                )
        except Exception as error:
            tap_terms_text.insert(INSERT, f"Could not connect to server.\n\n{error}")
        tap_terms_text.config(state="disabled")

        def delete_terms_page():
            try:
                tap.grab_release()
            except Exception:
                pass
            tap.destroy()
            self.tap_window = None
        terms_done_button = Button(
            tap,
            text=self.t("done"),
            command=delete_terms_page,
            font=("Segoe UI", 12, "bold"),
            fg="#FFF68F",
            bg="#104E8B",
            bd=0,
            padx=145
        )
        terms_done_button.place(x=6, y=325)
        tap.protocol("WM_DELETE_WINDOW", delete_terms_page)

    def log_in(self):
        username = self.usr_get.get().strip().lower()
        password = self.pwd_get.get().strip()
        captcha_taken = self.captcha_get.get().strip()
        placeholder = self.t("captcha_placeholder").strip()
        if not self.is_connected():
            msg.showwarning("Network Error", self.t("network_error"))
            return
        if not username:
            msg.showerror("No Data", self.t("username_empty"))
            return
        if username.isdigit():
            msg.showerror("Wrong Data", self.t("username_only_numbers"))
            return
        if not password:
            msg.showerror("No Data", self.t("password_empty"))
            return
        if not captcha_taken or captcha_taken == placeholder:
            msg.showerror("No Data", self.t("captcha_no_data"))
            return
        if not captcha_taken.isdigit():
            msg.showerror("Invalid Data", self.t("captcha_invalid"))
            self.new_captcha()
            return
        if captcha_taken != self.current_captcha_answer:
            msg.showerror("Wrong Data", self.t("captcha_wrong"))
            self.new_captcha()
            return
        password = password.replace(" ", "")
        cipher_usr, cipher_pwd = self.generate_credentials(username, password)
        try:
            self.authenticate_from_json(cipher_usr, cipher_pwd)
        except Exception as error:
            msg.showerror("Login Error", f"Could not authenticate from JSON.\n\n{error}")

    def fetch_users_json(self):
        url = "https://raw.githubusercontent.com/Brav0S1X/Tkinter-Login-Page/main/database.json"
        response = req.get(url, timeout=15)
        if response.status_code != 200:
            raise Exception("Could not fetch users JSON from GitHub.")
        return response.json()

    def authenticate_from_json(self, cipher_usr, cipher_pwd):
        data = self.fetch_users_json()
        users = data.get("users", [])
        matched_user = None
        for user in users:
            if user.get("username") == cipher_usr and user.get("password") == cipher_pwd:
                matched_user = user
                break
        if not matched_user:
            msg.showerror("Wrong Data", self.t("wrong_login"))
            return
        status = str(matched_user.get("status", "")).lower()
        if status != "active":
            msg.showerror("Expired", self.t("expired"))
            return
        expiration = matched_user.get("expiration", "")
        try:
            expiration_date = datetime.strptime(expiration, "%Y-%m-%d").date()
            today = datetime.now().date()
            if expiration_date < today:
                msg.showerror("Expired", self.t("expired"))
                return
        except Exception:
            msg.showerror("Error", "Invalid expiration date in user data.")
            return
        msg.showinfo("Login", self.t("logged_in"))
        self.reset_login_form()

    def encrypt_data(self, data):
        data_bytes = data.encode("utf-8")
        sha_hash = hashlib.sha224(data_bytes)
        return sha_hash.hexdigest()

    def generate_credentials(self, username, password):
        username_chars = list(username)
        password_chars = list(password)
        if len(username_chars) > len(password_chars):
            diff = len(username_chars) - len(password_chars)
            for _ in range(diff):
                password_chars.append("")
        else:
            diff = len(password_chars) - len(username_chars)
            for _ in range(diff):
                username_chars.append("")
        combined_chars = []
        for index in range(len(username_chars)):
            combined_chars.append(username_chars[index] + password_chars[index])
        combined_data = "".join(combined_chars)
        cipher_data = self.encrypt_data(combined_data)
        cipher_size = len(cipher_data)
        half_size = cipher_size / 2
        if cipher_size / 2 == 0:
            half_size = int(half_size)
            cipher_usr = cipher_data[:half_size]
            cipher_pwd = cipher_data[half_size:]
        else:
            half_size = int(half_size)
            name_part_1 = int(half_size - 0.5)
            name_part_2 = int(half_size + 0.5)
            cipher_usr = cipher_data[:name_part_1]
            cipher_pwd = cipher_data[name_part_2:]
        return cipher_usr, cipher_pwd

if __name__ == "__main__":
    clear_terminal()
    os_text = (
        "This program is developed for Windows 8 or newer, 64-bit only;\n"
        "Please contact the program developers for more information."
    )
    try:
        if os.name != "nt":
            with open("Read_ME.txt", "w+", encoding="utf-8") as file:
                file.write(os_text)
            try:
                root = Tk()
                root.withdraw()
                msg.showinfo("Notice", os_text)
                root.destroy()
            except Exception:
                sys.stdout.write("Read This File -> Read_ME.txt")
                slp(5)
            sys.exit(1)
        if sys.maxsize <= 2**32:
            root = Tk()
            root.withdraw()
            msg.showerror(
                "Unsupported Architecture",
                "This program only runs on 64-bit Windows."
            )
            root.destroy()
            sys.exit(1)
        windows_version = sys.getwindowsversion()
        if (windows_version.major, windows_version.minor) < (6, 2):
            root = Tk()
            root.withdraw()
            msg.showerror(
                "Unsupported OS Version",
                "This program requires Windows 8 or newer."
            )
            root.destroy()
            sys.exit(1)
        log_main = Tk()
        LoginPage(log_main)
        log_main.mainloop()
    except SystemExit:
        raise
    except Exception as error:
        try:
            root = Tk()
            root.withdraw()
            msg.showerror("Startup Error", str(error))
            root.destroy()
        except Exception:
            sys.stdout.write(str(error))
        sys.exit(1)
# /// Fin || Developed By: +98911 733 5899 - mrkia.ir \\\
