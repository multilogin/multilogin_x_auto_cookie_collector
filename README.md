# CookieRobot for Multilogin X

This is a tool for automatically visiting determined websites in order to collect cookies for your browser profiles.

## Instructions

### Start your Multilogin X agent

#### Linux:
```bash
/opt/mlx/agent.bin
```
Or simply:
```bash
mlx
```

#### Windows:

```bash
Start-Process -FilePath "~/AppData/Local/Multilogin X/agent.exe"
```
### Edit the .env file

```env
MLX_EMAIL=yourmultiloginaccount@domain.com
MLX_PASSWORD=SuperSecretPassword
PROFILE_ID=
FOLDER_ID=
BROWSER_TYPE=
```
### Edit the websites list

You need to tell the script where it needs to collect cookies from. Simply edit the "websites" array in the main.py file.

```python
# This is an example. Add as many as you want. If you want to, you can even remove this array here and add another
# method of reading the list of websites, such as by using a spreadsheet, for example.

websites = ["https://wikipedia.org/",
            "https://multilogin.com/"
            "https://dell.com/",
            "https://reddit.com/",
            "https://youtube.com/"]
```
## Install the browser extension

We use Superagent browser extension to accept cookie policy automatically. Before starting the script, make sure the extension has been installed. "[Folder](https://help.multilogin.com/en_US/profile-management/installing-browser-extensions)" method is recommended for extension installation.

### Run the script

On your terminal, run the script with python.
```bash
python cookie_robot.py
```
Or, if you're using the python3 interpreter:
```bash
python3 cookie_robot.py
```
