@echo off
:inicio
title Mi Asistente del Clima
color 0F
cls

echo =========================================
echo       ELIJA UNA OPCION DE CLIMA
echo =========================================
echo [1] Ver Clima Actual
echo [2] Ver Pronostico Extendido (5 dias)
echo [3] Salir
echo =========================================
echo.

choice /c 123 /n /m "Seleccione una opcion (1, 2 o 3): "

if errorlevel 3 goto salir
if errorlevel 2 goto pronostico
if errorlevel 1 goto actual

:actual
echo.
echo --- Iniciando Clima Actual ---
call .\env\Scripts\activate.bat
python clima.py
echo.
echo -----------------------------------------
echo Consulta finalizada.
pause
goto inicio

:pronostico
echo.
echo --- Iniciando Pronostico Extendido ---
call .\env\Scripts\activate.bat
python pronostico.py
echo.
echo -----------------------------------------
echo Consulta finalizada.
pause
goto inicio

:salir
echo.
echo ¡Gracias por usar el Asistente del Clima!
timeout /t 2 >nul
exit