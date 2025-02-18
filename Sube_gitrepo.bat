@echo off
cd /d "%~dp0"
echo Introduce el mensaje de commit:
set /p commitMsg=

git add .
git commit -m "%commitMsg%"
git push origin main

echo.
echo ¡Codigo subido con exito!
pause
