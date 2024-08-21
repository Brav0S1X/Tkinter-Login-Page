<p align="center">
    <a href="github.address">
        <img src="https://github.com/BlackSourceTM/Tkinter-Login-Page/blob/main/default_bg.png" alt="Brav0S1X" width="128">
    </a>
    <br>
    <b>Graphical User Interface by Python</b>
    <br>
    <a href="https://github.com/BlackSourceTM/Tkinter-Login-Page">
        Homepage    
    </a>
    •
    <a href="https://bit.ly/Mr_kia">
            About
    </a>
</p>

## Python Tk()

> a quick modern Graphical User Interface to get logged into your accounts!

### Notices
**One**
Sometimes you may encounter this error:
```text
Exception in Tkinter callback
Traceback (most recent call last):
  File "Login_page.py", line 306, in check_captcha
    login_cur.execute(f"SELECT role FROM USERs WHERE username = '{cipher_usr}' AND password = '{cipher_pwd}'")
sqlite3.DatabaseError: file is not a database
```
To fix this error, you must refer to the site's Internet address manually with the IP address of Iran; URL available in line 239 of the source! something like:
```Python
url = "https://domain.com/path/Login_Database.ibd"
```
Submit a request to get a new download link and replace it with the previous URL in the source code.(or u can put your own URL in the same place)
**Two**
To get logged in, use this informations:
```bash
username: Brav0S1X
password: Ali@1382
```

### Key Features

- **Simple**: With an easy UI
![Login_github_vector](https://github.com/BlackSourceTM/Tkinter-Login-Page/assets/97563457/c220ea64-b4bf-4fe6-956d-6d2337531047)
- **Safe**: Using DataBases for getting better experience & prevent of BOT Activities.

### Run

``` bash
>_ git clone https://github.com/BlackSourceTM/Tkinter-Login-Page.git
>_ cd Tkinter-Login-Page
>_ pip install -r requirements.txt
>_ python main.py
```
