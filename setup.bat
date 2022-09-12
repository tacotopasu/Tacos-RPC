@ECHO OFF
ECHO Welcome to Taco's RPC!
ECHO Let's go through the instalation of Python, since it's needed for Taco's RPC to run.
ECHO Downloading Python 3.10.5... && curl -L -O https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe
ECHO Running Installer... && python-3.10.5-amd64.exe /quiet PrependPath=1 Include_test=0
ECHO Clearing up... && del python-3.10.5-amd64.exe && del README.md && del LICENSE && del requirements.txt
ECHO Done. && ECHO Python (3.10.5) Installed!
python -m pip install pyautogui
PAUSE && EXIT