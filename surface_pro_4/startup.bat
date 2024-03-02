@echo off 
cd surface_pro_web_interface\client
start /B npm run dev
timeout /t 5 /nobreak
"C:\Program Files\Google\Chrome\Application\chrome.exe" --start-fullscreen http://localhost:5173

