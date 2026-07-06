<p align="center">
    <br>
    <b>Graphical User Interface by Python</b>
    <br>
    <a href="https://github.com/Brav0S1X/Tkinter-Login-Page">
        Homepage    
    </a>
    •
    <a href="https://mrkia.ir">
            About
    </a>
</p>

## root != Tk;)

> a Quick Modern Graphical User Interface to Get Logged into Your Accounts!

### Notices

**One**  
You can set a custom application icon using one of the following methods:

**1. Per-window icon (Development method)**  
Call the following method (e.g. `self.set_icon()`) for each window individually:

```python
def set_icon(self):
    icon_path = os.path.join(self.currentDir, "ICON.png")
    if os.path.exists(icon_path):
        try:
            icon_photo = PhotoImage(file=icon_path)
            self.master.iconphoto(False, icon_photo)
            self.icon_photo = icon_photo
        except Exception:
            pass
```

**2. Permanent executable icon (Recommended)**  
Use the `--icon` argument when building the application with **PyInstaller** to permanently embed your desired `.ico` file into the executable.

> **Note:**  
> If you encounter the following error while packaging:
>
> `randrange(0, 0, 0)`
>
> make sure all required dependencies are collected correctly. For example:

```bash
pyinstaller --onefile --windowed --collect-all multicolorcaptcha --collect-all PIL --icon ICON.ico login.py
```

---

**Two**  
Use the following credentials for testing:

```text
Username: Test
Password: 1234
```

> **Security Notice:**  
> This project is intended only as a demonstration of how to connect a graphical interface to a database. Before using it in a real-world application, you should replace the encryption algorithm with a secure one and protect the communication channel between the application and the database.

### Run

```text
>_ git clone https://github.com/Brav0S1X/Tkinter-Login-Page.git
>_ cd Tkinter-Login-Page
>_ pip install -r requirements.txt
>_ python login.py
```
