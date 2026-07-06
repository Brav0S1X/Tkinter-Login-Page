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
<img width="3146" height="1769" alt="78451" src="https://github.com/user-attachments/assets/cddea596-1f5e-475f-a4c2-6dfa997c2288" />
## root != Tk;)

> a Quick Modern Graphical User Interface to Get Logged into Your Accounts!

### Notices

**One**  
For the final packaged executable, setting the icon at runtime with self.set_icon is not recommended.
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
