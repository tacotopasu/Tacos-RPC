@ECHO OFF
ECHO Welcome to Taco's RPC!
ECHO Let's go through the instalation of Python, since it's needed for Taco's RPC to run.
ECHO Press Enter when you're ready.
PAUSE
ECHO Downloading Python 3.10.5... && curl -L -O https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe
ECHO Running Installer... && python-3.10.5-amd64.exe /quiet PrependPath=1 Include_test=0
pip install -r requirements.txt 
ECHO Clearing up unnecessary files... && DEL python-3.10.5-amd64.exe && DEL README.md && DEL LICENSE && DEL requirements.txt
ECHO Done. && ECHO Python (3.10.5) Installed!
ECHO setup.bat is going to delete itself on exit. Have fun using Taco's RPC!
PAUSE
DEL setup.bat
EXIT