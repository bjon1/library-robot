@echo off 
cd surface_pro_web_interface\
start /B npm run start
timeout /t 5 /nobreak
"C:\Program Files\Google\Chrome\Application\chrome.exe" --start-fullscreen http://localhost:5000

