@echo off

set my_dir=%~dp0
Echo.%my_dir% | Find "~" && ( echo '---------------------------------' ) || ( goto Write )

:Write
    echo %my_dir% > install_log.txt

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%my_dir%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%my_dir%\getadmin.vbs"


    "%my_dir%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%my_dir%\getadmin.vbs" ( del "%my_dir%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------

FOR /F "tokens=* delims=" %%x in (install_log.txt) DO set logPath=%%x

Echo.%PYTHONPATH% | Find /I /C "%logPath%" && ( goto doNotSetPath ) || ( goto setPythonPath )

:setPythonPath
    echo setting path
    echo %logPath%
    setx PYTHONPATH %PYTHONPATH%;%logPath%
    if exist "install_log.txt" ( del "install_log.txt" )

:doNotSetPath
    echo Project path already exists in PYTHONPATH, skipping.
    if exist "install_log.txt" ( del "install_log.txt" )

echo Project is successfully installed.
pause



