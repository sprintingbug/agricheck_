@echo off
echo This script will add a Windows Firewall rule to allow port 8000
echo You need to run this as Administrator!
echo.
echo Right-click this file and select "Run as administrator"
echo.
pause
netsh advfirewall firewall add rule name="Agricheck Backend Port 8000" dir=in action=allow protocol=TCP localport=8000
echo.
echo Firewall rule added!
echo You can now access the backend from your phone.
pause

