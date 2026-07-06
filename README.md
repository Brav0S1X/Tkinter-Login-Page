<p align="center">
    <br>
    <b>Graphical User Interface by Python</b>
    <br>
</p>
<img width="900" alt="Tkinter app authentication screen" src="https://github.com/user-attachments/assets/2770b612-6d63-4700-aec1-ee88ab7b629e" />

### root != Tk;)

> a Quick Modern Graphical User Interface to Get Logged into Your Accounts!

**Tkinter Login Project** is a lightweight Python application packaged as a single executable. It uses embedded resources, including inline SVG assets, to reduce external dependencies and keep the project self-contained. This is the second working version of the project, built as a learning-oriented example of graphical user interface development.<br><br>

### Packaging & Deployment
For the final packaged executable, setting the icon at runtime with self.set_icon is not recommended.
Use the `--icon` argument when building the application with **PyInstaller** to permanently embed your desired `.ico` file into the executable.

> **Troubleshooting:**

> If you encounter the following error while packaging:
>
> `randrange(0, 0, 0)`
>
> make sure all required dependencies are collected correctly. For example:

```bash
pyinstaller --onefile --windowed --collect-all multicolorcaptcha --collect-all PIL --icon ICON.ico login.py
```

---
<br><br>
### Testing
Use the following credentials for testing:

```text
Username: Test
Password: 1234
```

> **Security Notice:**  
> This project is intended only as a demonstration of how to connect a graphical interface to a database. Before using it in a real-world application, you should replace the encryption algorithm with a secure one and protect the communication channel between the application and the database.



### Key Features
- **Modern UI**: A clean and lightweight Tkinter interface
- **Database-backed Login**: Authentication connected to a database
- **Bot Protection**: Basic captcha verification
- **Single Executable**: Packed into one standalone file
- **Embedded Assets**: Uses internal resources to minimize external dependencies


### Run

```text
>_ git clone https://github.com/Brav0S1X/Tkinter-Login-Page.git
>_ cd Tkinter-Login-Page
>_ pip install -r requirements.txt
>_ python login.py
```
