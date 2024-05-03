from tkinter import *
from tkinter import filedialog, messagebox as msg
from PIL import ImageTk, Image
import random as rn, requests as req
from captcha.image import ImageCaptcha
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from gtts import gTTS
from subprocess import call
from time import sleep as slp
import os, sys, platform, PyPDF2, socket, hashlib, sqlite3, re
class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title('Login Page')
        self.master.geometry("374x648")
        self.master.resizable(0, 0)
        self.currentDir = os.path.dirname(os.path.abspath(__file__))
        FSCP_iconphoto = PhotoImage(file=self.currentDir + "\Login.png")
        self.master.iconphoto(False, FSCP_iconphoto)
        self.default_bg = "#1F1F1F"
        self.dfbg = self.default_bg  # I call Default Background as DFBG(.lower)!
        self.master.config(bg=self.dfbg)
        self.create_widgets()
    def clear_terminal():
        if platform not in ('win32', 'cygwin'):
            command = 'clear'
        else:
            command = 'cls'
        try:
            call(command, shell=True)
        except OSError as e:
            print(type(e).__name__, e)
    try:
        clear_terminal()
    except KeyboardInterrupt:
        pass
    def is_connected(self):
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
            return False
    def captcha(self, capText):
        captcha_img = ImageCaptcha(width = 280, height = 90)
        generate_captcha = captcha_img.generate(capText)
        captcha_img.write(capText, 'captcha.png')
    def rand(self, text):
        global randText
        randStr = list(text)
        rn.shuffle(randStr)
        randText = ("".join(randStr)[0:6])
        return randText
    def new_captcha(self):
        self.rand("0123456789")
        try:
            self.captcha(randText)
        except TypeError:
            self.captcha(str(randText))
        for cap_item in self.cap_list:
            try:
                self.cap_list.remove(cap_item)
            except:
                pass
        self.cap_list.append(randText)
        self.my_captcha = Image.open(os.path.join(self.currentDir, "captcha.png"))
        self.my_captcha = self.my_captcha.resize((self.my_captcha.width // 4, self.my_captcha.height // 3))
        self.my_captcha = ImageTk.PhotoImage(self.my_captcha)
        final_captcha = Label(self.log_main_bot_verification, image = self.my_captcha, bd = 0, bg = self.dfbg)
        final_captcha.place(x = 5, y = 2)
    def listen_captcha(self):
        language = "en"
        Sound_file = "captcha"
        sound_txt = "".join(str(int(randText[i])) + "   " * (4 - i % 4) for i in range(len(randText)))
        sound_txt = "captcha code is: " + sound_txt
        cap_sound = gTTS(text = sound_txt, lang = language)
        cap_sound.save(Sound_file + ".mp3")
        try:
            os.system(f'{Sound_file}.mp3')
        except Exception as e:
            msg.showerror("Error", f"Something went wrong while Trying to Play File {Sound_file}.mp3\n\nError is:\n{e}")
    def clear_all(self):
        for widget in self.master.winfo_children():
            widget.destroy()
    def support(self): # This is problem
        msg.showinfo('Notice', 'This option opening SUPPORT page in full FSCP version! :)')
        None # Go To Support page
    def create_widgets(self):
        self.rand("0123456789")
        self.captcha(randText)
        self.cap_list = []
        self.cap_list.append(randText)
        login_hint_txt_01 = '''Welcome Dear user;
To use the program, just enter your username & password'''
        login_hint_01 = Label(self.master, text=login_hint_txt_01, font=('Ebrima', 10, 'bold'), fg="#ADFF2F",
                              bg=self.dfbg, justify=LEFT)
        login_hint_01.pack()
        login_hint_txt_02 = "or call                        if u need a new one!"
        login_hint_02 = Label(self.master, text=login_hint_txt_02, font=('Ebrima', 9, 'bold'), fg="#ADFF2F",
                              bg=self.dfbg, justify=LEFT)
        login_hint_02.place(x=4, y=36)
        login_support_button = Button(self.master, text="SUPPORT", command=self.support, font=('Ebrima', 9, 'bold', 'underline'),
                                      fg="#FFF68F", bg=self.dfbg, bd=0)
        login_support_button.place(x=46, y=36)
        log_main_login_frame = LabelFrame(self.master, text="Login Informations", font=('Ebrima', 9, 'bold'),
                                          fg="#ADFF2F", bg=self.dfbg, width=358, height=90)
        log_main_login_frame.place(x=7, y=70)
        self.log_main_bot_verification = LabelFrame(self.master, text = "Bot Verification", font=('Ebrima', 9, 'bold'),
                                          fg="#ADFF2F", bg=self.dfbg, width=358, height=58)
        self.log_main_bot_verification.place(x = 7, y = 175)
        log_usr_lbl = Label(log_main_login_frame, text="Username:", font=('Ebrima', 10, 'bold'), fg="#FFF68F",
                            bg=self.dfbg)
        log_usr_lbl.place(x=4, y=4)
        self.usr_get = StringVar()
        self.log_usr_ent = Entry(log_main_login_frame, width=38, textvariable = self.usr_get, font=('Ebrima', 10), fg="#ADFF2F", bg="#3D3D3D",
                                 bd=0)
        self.log_usr_ent.place(x=78, y=7)
        log_pwd_lbl = Label(log_main_login_frame, text="Password:", font=('Ebrima', 10, 'bold'), fg="#FFF68F",
                            bg=self.dfbg)
        log_pwd_lbl.place(x=4, y=34)
        self.pwd_get = StringVar()
        self.log_pwd_ent = Entry(log_main_login_frame, width=34, textvariable = self.pwd_get, show="*", font=('Ebrima', 10), fg="#ADFF2F",
                                 bg="#3D3D3D", bd=0)
        self.log_pwd_ent.place(x=78, y=37)
        self.eyes_on_target = Image.open(os.path.join(self.currentDir, "eyes_on.png"))
        self.eyes_on_target = self.eyes_on_target.resize((self.eyes_on_target.width // 160,
           self.eyes_on_target.height // 160))
        self.on_target_photo = ImageTk.PhotoImage(self.eyes_on_target)
        self.eyes_out_of_target = Image.open(os.path.join(self.currentDir, "eyes_out.png"))
        self.eyes_out_of_target = self.eyes_out_of_target.resize((self.eyes_out_of_target.width // 160,
                   self.eyes_out_of_target.height // 160))
        self.out_of_target_photo = ImageTk.PhotoImage(self.eyes_out_of_target)
        self.show_password = "*"
        self.log_pwd_show = Button(log_main_login_frame, image=self.on_target_photo, command=self.pwd_check,
                                   bg=self.dfbg, bd=0)
        self.log_pwd_show.place(x=322, y=36)
        self.my_captcha = Image.open(os.path.join(self.currentDir, "captcha.png"))
        self.my_captcha = self.my_captcha.resize((self.my_captcha.width // 4, self.my_captcha.height // 3))
        self.my_captcha = ImageTk.PhotoImage(self.my_captcha)
        final_captcha = Label(self.log_main_bot_verification, image = self.my_captcha, bd = 0, bg = self.dfbg)
        final_captcha.place(x = 5, y = 2)
        def on_focus_in(entry, default_text):
            if entry.get() == default_text:
                entry.delete(0, END)
                entry.insert(0, "")
        def on_focus_out(entry, default_text):
            if entry.get() == "":
                entry.delete(0, END)
                entry.insert(0, default_text)
        get_captcha_defaul_txt = "CAPTCHA Here..."
        self.captcha_get = StringVar()
        self.get_captcha = Entry(self.log_main_bot_verification, width = 30, textvariable = self.captcha_get, font=('Ebrima', 10), fg="#ADFF2F",
                                 bg="#3D3D3D", bd=0)
        self.get_captcha.insert(0, get_captcha_defaul_txt)
        self.get_captcha.bind("<FocusIn>", lambda event, entry=self.get_captcha, default_text=get_captcha_defaul_txt: on_focus_in(self.get_captcha, get_captcha_defaul_txt))
        self.get_captcha.bind("<FocusOut>", lambda event, entry=self.get_captcha, default_text=get_captcha_defaul_txt: on_focus_out(self.get_captcha, get_captcha_defaul_txt))
        self.get_captcha.place(x = 78, y = 6)
        self.headphone = Image.open(os.path.join(self.currentDir, "Headphone.png"))
        self.headphone = self.headphone.resize((self.headphone.width // 145, self.headphone.height // 145))
        self.headphone = ImageTk.PhotoImage(self.headphone)
        get_captcha_listen = Button(self.log_main_bot_verification, image = self.headphone, command = self.listen_captcha, bd = 0, bg = self.dfbg)
        get_captcha_listen.place(x = 321, y = 3)
        self.refresh = Image.open(os.path.join(self.currentDir, "Refresh.png"))
        self.refresh = self.refresh.resize((self.refresh.width // 145, self.refresh.height // 145))
        self.refresh = ImageTk.PhotoImage(self.refresh)
        get_new_captcha = Button(self.log_main_bot_verification, image = self.refresh, command = self.new_captcha, bd = 0, bg = self.dfbg)
        get_new_captcha.place(x = 294, y = 3)
        self.defualt_logo = Image.open(os.path.join(self.currentDir, "default_bg.png"))
        self.defualt_logo = self.defualt_logo.resize((self.defualt_logo.width // 10, self.defualt_logo.height // 11))
        self.defualt_logo = ImageTk.PhotoImage(self.defualt_logo)
        bs_main_pic = Label(self.master, image = self.defualt_logo, bg = self.dfbg, bd = 0)
        bs_main_pic.place(x = 14, y = 350)
        agreement_txt =  "By click on this, you agreed to our                          &"
        def agreement():
            agrmnt = self.get_agreement_accepted.get()
            def log_in():
                username = str(self.usr_get.get().strip())
                password = str(self.pwd_get.get().strip())
                self.captcha = self.captcha_get.get().strip()
                if self.is_connected():
                    if username:
                        if "@" in username:
                            msg.showerror('Invalid Data', 'You cant use "@" in your Username at all!')
                        else:
                            try:
                                username = int(username)
                                usr_int = True
                            except:
                                usr_int = False
                            if usr_int:
                                msg.showerror('Wrong Data', 'Username cant be only numbers!')
                            else:
                                if password:
                                    def check_captcha():
                                        if self.captcha:
                                            try:
                                                self.captcha = int(self.captcha)
                                                capt_int = True
                                            except:
                                                capt_int = False
                                                if self.captcha == get_captcha_defaul_txt:
                                                    msg.showerror('No Data', 'Please enter the numbers which you see in image, at captcha section\n\nCant See Numbers?\n    [1] Use listener\n    [2] Refresh CAPTCHA')
                                                else:
                                                    msg.showerror('Invalid Data', 'You cant enter anything except numbers in CAPTCHA Field!')
                                            if capt_int:
                                                self.captcha = str(self.captcha)
                                                if self.captcha == self.cap_list[0]:
                                                    try:
                                                        def delete_database():
                                                            if os.path.exists("FSCP_database.db"):
                                                                try:
                                                                    os.system('del FSCP_database.db')
                                                                except FileNotFoundError:
                                                                    current_directory = os.getcwd()
                                                                    for file in os.listdir(current_directory):
                                                                        if file.endswith('.db'):
                                                                            file_path = os.path.join(current_directory, file)
                                                                            try:
                                                                                os.remove(file_path)
                                                                            except Exception as e:
                                                                                msg.showerror('System Permission', f'Failed to delete FSCP_database.db\n Error -> {e}')
                                                                except PermissionError:
                                                                    msg.showinfo('Notice', 'Your system couldn\'t allow us to remove FSCP_database.db automatically!\nif u dont need it, delete it by your own.')
                                                                except Exception:
                                                                    pass # به درک که حذف نمیشه
                                                            else:
                                                                msg.showerror('Missing Data', 'FSCP_database.db NOT FOUNDED!')
                                                        def try_del_db():
                                                            try:
                                                                login_cur.close()
                                                                login_conn.close()
                                                            except:
                                                                pass
                                                            try:
                                                                delete_database()
                                                            except:
                                                                pass
                                                        url = "https://s31.picofile.com/d/8474621368/00bcda0c-ad06-48ab-8376-322f5872dbc0/FSCP_database.db"
                                                        try:
                                                            response = req.get(url, stream = True)
                                                        except req.HTTPError as http_err:
                                                            response = req.get(url, stream = True)
                                                            if response.status_code == 400:
                                                                msg.showerror('Network Error', 'Poor Connection')
                                                            elif response.status_code == 404:
                                                                msg.showerror('Invalid URL', f'This url is not active anymore!\nupdate your app or call support.\n\nLast Database URL ->  {url}')
                                                            else:
                                                                msg.showerror('Invalid Error', 'Something went wrong, contact support')
                                                                raise http_err
                                                        if response.status_code == 200:
                                                            with open("FSCP_database.db", "wb") as file:
                                                                for chunk in response.iter_content(chunk_size=8192):
                                                                    file.write(chunk)
                                                        else:
                                                            msg.showerror('Network Error', 'Poor Connection')
                                                    except Exception as e:
                                                        msg.showerror('Error', 'System Crashed while tried to download Database')
                                                    def encrypt_data(data):
                                                        data_bytes = data.encode('utf-8')
                                                        sha_hash = hashlib.sha224(data_bytes)
                                                        hashed_data = sha_hash.hexdigest()
                                                        return hashed_data
                                                    userName = list(username)
                                                    passWord = list(password)
                                                    if len(userName) > len(passWord):
                                                        diff = len(userName) - len(passWord)
                                                        for i in range(diff):
                                                            passWord.append('')
                                                    else:
                                                        diff = len(passWord) - len(userName)
                                                        for i in range(diff):
                                                            userName.append('')
                                                    new_full_name = []
                                                    for i in range(len(userName)):
                                                        new_full_name.append(userName[i] + passWord[i])
                                                    full_name = "".join(new_full_name)
                                                    data = full_name
                                                    cipher_data = encrypt_data(data)
                                                    full_name_size = len(cipher_data)
                                                    new_size = full_name_size / 2
                                                    if full_name_size / 2 == 0:
                                                        new_size = int(new_size)
                                                        cipher_usr = cipher_data[:new_size]
                                                        cipher_pwd = cipher_data[new_size:]
                                                    else:
                                                        new_size = int(new_size)
                                                        name_part_1 = new_size - 0.5
                                                        name_part_2 = new_size + 0.5
                                                        name_part_1 = int(name_part_1)
                                                        name_part_2 = int(name_part_2)
                                                        cipher_usr = cipher_data[:name_part_1]
                                                        cipher_pwd = cipher_data[name_part_2:]
                                                    if os.path.exists("FSCP_database.db"):
                                                        def start_mission():
                                                            try:
                                                                login_cur.close()
                                                                login_conn.close()
                                                            except Exception as e:
                                                                msg.showerror('Notice', f'Something went wrong while trying to close FSCP_database.db\n\nError -> {e}')
                                                            self.clear_all()
                                                            try_del_db()
                                                            Label(self.master, text = "Now! You logged in :) do something.." ,fg = "Yellow", bg = self.dfbg).pack()
                                                        login_conn = sqlite3.connect('FSCP_database.db')
                                                        login_cur = login_conn.cursor()
                                                        login_cur.execute(f"SELECT role FROM USERs WHERE username = '{cipher_usr}' AND password = '{cipher_pwd}'")
                                                        login_conn.commit()
                                                        login_data = login_cur.fetchall()
                                                        if login_data:
                                                            for item in login_data:
                                                                if 'admin' in item:
                                                                    start_mission()
                                                                elif 'user' in item:
                                                                    login_cur.execute(f"SELECT status FROM USERs WHERE username = '{cipher_usr}' AND password = '{cipher_pwd}'")
                                                                    login_conn.commit()
                                                                    status_data = login_cur.fetchall()
                                                                    for theme in status_data:
                                                                        if 'active' in theme:
                                                                            start_mission()
                                                                        else:
                                                                            login_cur.execute(f"SELECT expiration FROM USERs WHERE username = '{cipher_usr}' AND password = '{cipher_pwd}'")
                                                                            login_conn.commit()
                                                                            expiration_data = login_cur.fetchall()
                                                                            current_datetime = datetime.now()
                                                                            formatted_date = str(current_datetime.strftime("%m%Y"))
                                                                            for way in expiration_data:
                                                                                expiration_way = re.findall(r'\d+', way[0])  # extract the first element of the tuple
                                                                                expiration_date = ''.join(expiration_way) if expiration_way else None
                                                                                current_date_month = formatted_date[:2]
                                                                                current_date_year = formatted_date.replace(current_date_month, '')
                                                                                expiration_date_month = expiration_date[:2]
                                                                                expiration_date_year = expiration_date.replace(expiration_date_month, '')
                                                                                if expiration_date_year > current_date_year:
                                                                                    start_mission()
                                                                                else:
                                                                                    if expiration_date_year == current_date_year:
                                                                                        if expiration_date_month >= current_date_month:
                                                                                            start_mission()
                                                                                        else:
                                                                                            try_del_db()
                                                                                            msg.showerror('Expirad Data', 'Your Login Data had been Expirad\nContact support to get a new one!')
                                                                                    else:
                                                                                        try_del_db()
                                                                                        msg.showerror('Expirad Data', 'Your Login Data had been Expirad\nContact support to get a new one!')
                                                                else:
                                                                    try_del_db()
                                                                    msg.showerror('Wrong Data', f'Please Download FSCP_database.db in original version:\n{url}')
                                                        else:
                                                            try_del_db()
                                                            msg.showerror('Wrong Data', 'Username or Password isn\'t correct!')
                                                    else:
                                                        msg.showerror('Missing Data', 'FSCP_database.db not founded!\n\ncheck your internet to download it again\nor\ncontact support')
                                                else:
                                                    msg.showerror('Wrong Data', 'Captcha code does not match!')
                                            else:
                                                pass
                                        else:
                                            msg.showerror('No Data', 'Please enter the numbers which you see in image, at captcha section\n\nCant See Numbers?\n    [1] Use listener\n    [2] Refresh CAPTCHA')
                                    if " " in password:
                                        password = password.replace(" ", "")
                                        check_captcha()
                                    else:
                                        check_captcha()
                                else:
                                    msg.showerror('No Data', 'Password field cant be empty!')
                    else:
                        msg.showerror('No Data', 'Please Enter something in  the Username field as your username!\nEx: John1234')
                else:
                    msg.showwarning('Network Error', 'Make Sure that your connected to an internet server!')
            if agrmnt:
                try:
                    self.get_logging_in.place(x = 5, y = 330)
                except:
                    self.get_logging_in = Button(self.master, text = "LOGIN",command = log_in, font = ("Copperplate Gothic Bold", 12, 'bold'), 
                                            fg = "Green", bg = "#FFF68F", bd = 0, padx = 138)
                    self.get_logging_in.place(x = 10, y = 320)
            else:
                try:
                    self.get_logging_in.destroy()
                except:
                    self.get_logging_in.place(x = 10, y = 1000) # to be not able to access
        self.get_agreement_accepted = BooleanVar()
        self.get_agreement = Checkbutton(self.master, text = "", variable = self.get_agreement_accepted, command = agreement, fg = "Red", bg = self.dfbg, bd = 0)
        self.get_agreement.place(x = 6, y = 255)
        self.agreement_txt = Label(self.master, text = agreement_txt, font=('Ebrima', 10, 'bold'), fg = "#ADFF2F", bg = self.dfbg)
        self.agreement_txt.place(x = 25, y = 253)
        self.tap_page_num = 0
        self.tap_page_status = None
        def terms_n_privacy():
            def close_tap_window():
                self.tap_page_num = 0
                self.tap_page_status = None
                tap.destroy()
            tap = Tk() # TAP is Terms And Privacy
            tap.title("Terms and privacy policy")
            tap.geometry("374x393")
            tap.resizable(0, 0)
            if self.tap_page_num == 0: # self.tap_page_num is 0 -> OSerror
                self.tap_page_num += 1
            else:
                with open(os.devnull, "w") as devnull:
                    with redirect_stdout(devnull):
                        with redirect_stderr(devnull):
                            try:
                                if self.tap_page_num == 1:
                                    if self.tap_page_status == True:
                                        tap.destroy()
                                    elif self.tap_page_status == False:
                                        pass
                                    else:
                                        pass
                                else:
                                    pass
                            except TclError:
                                pass
            self.tap_page_status = True
            tap.config(bg = self.dfbg)
            tap_msg = Label(tap, text = "Read this to avail our services:", font = ('Ebrima', 10, 'bold'),
                            bg = self.dfbg, fg = "#1E90FF")
            tap_msg.place(x = 2, y = 2)
            tap_terms_text = Text(tap, width = 49, height = 17, wrap = WORD,
                               font = ('Ebrima', 10, 'bold'),bg = "#3D3D3D", fg = "#FFF68F", bd = 0)
            tap_terms_text.place(x = 6, y = 30)
            tap_scrollbar = Scrollbar(tap, orient = VERTICAL, command = tap_terms_text.yview)
            tap_scrollbar.pack(side = RIGHT, fill = Y)
            tap_terms_text.config(yscrollcommand = tap_scrollbar.set)
            tap_scrollbar.config(command = tap_terms_text.yview)
            def read_pdf(filename):
                with open(filename, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    text = ""
                    for page_num in range(num_pages):
                        page = reader.pages[page_num]
                        text += page.extract_text()
                    new_text = ""
                    for t in text:
                        new_text += t
                    return new_text
            terms_pdf_file = self.currentDir + "\Terms.pdf"
            if os.path.exists("Terms.pdf"):
                pdf_text = read_pdf(terms_pdf_file)
                terms = ""
                for char in pdf_text:
                    terms += char
                    tap_terms_text.insert(INSERT, terms)
                    terms = ""
                tap_terms_text.config(state = 'disabled')
            else:
                msg.showerror('Missing Data', 'Terms.pdf NOT FOUNDED')
            def delete_terms_page():
                tap.destroy()
                self.tap_page_num -= 1
                self.tap_page_status = False
            def show_terms_pdf():
                os.startfile(terms_pdf_file)
                tap.destroy()
                self.tap_page_num -= 1
                self.tap_page_status = False
            terms_done_button = Button(tap, text = "DONE",command = delete_terms_page, font = ("Copperplate Gothic Bold", 12, 'bold'), 
                                            fg = "#FFF68F", bg = "#104E8B", bd = 0, padx = 137)
            terms_done_button.place(x = 6, y = 325)
            terms_pdf_button = Button(tap, text = "SHOW IN PDF",command = show_terms_pdf, font = ("Copperplate Gothic Bold", 12, 'bold'), 
                                            fg = "#FFF68F", bg = "#104E8B", bd = 0, padx = 99)
            terms_pdf_button.place(x = 6, y = 357)
            tap.protocol("WM_DELETE_WINDOW", close_tap_window)
            tap.mainloop()
        self.privacy = Button(self.master, text="PRIVACY POLICY", command=terms_n_privacy, font=('Ebrima', 9, 'bold', 'underline'),
                                      fg="#FFF68F", bg=self.dfbg, bd=0)
        self.privacy.place(x = 243, y = 255)
        self.terms = Button(self.master, text="TERMS of USE", command=terms_n_privacy, font=('Ebrima', 9, 'bold', 'underline'),
                                      fg="#FFF68F", bg=self.dfbg, bd=0)
        self.terms.place(x = 26, y = 275)
        self.agreement_txt_done = Label(self.master, text = ".", font=('Ebrima', 10, 'bold'), fg = "#ADFF2F", bg = self.dfbg)
        self.agreement_txt_done.place(x = 108, y = 275)
    def pwd_check(self):
        if self.show_password == "*":
            self.log_pwd_show.config(image = self.out_of_target_photo)
            self.show_password = ""
            self.log_pwd_ent.config(show = self.show_password)
        else:
            self.log_pwd_show.config(image = self.on_target_photo)
            self.show_password = "*"
            self.log_pwd_ent.config(show = self.show_password)
if __name__ == "__main__":
    osname = platform.uname()[0]
    if osname == "Windows":
        try:
            clear_terminal() # It not working in "self.clear_terminal" mode too ! Cuze clear_terminal function should be writed after this code part..
        except KeyboardInterrupt:
            pass
        except NameError:
            os.system('cls')
        log_main = Tk()
        login_page = LoginPage(log_main)
        log_main.mainloop()
    else:
        OS_txt = "This program is developed for the Windows operating system;\nPlease contact the program developers for more information."
        with open("Read_ME.txt", W) as file:
            file.write(OS_txt)
        try:
            root = Tk()
            root.title('Message')
            msg.showinfo("Notice", OS_txt)
        except:
            os.system('cmd')
            sys.stdout.write('Read This File -> Read_Me.txt')
            slp(5)
            root.destroy()
            root.mainloop()
            sys.exit()
# /// Fin || Developed By: +98911 733 5899 - Ali Rahimi Kia. \\\