@ECHO OFF
IF EXIST .\.venv\ GOTO NOVENV
ECHO. & ECHO. & ECHO.
ECHO "*************** Criando um Ambiente Virtual (VirtualEnv) ***************" & ECHO.
python -m venv .venv
ECHO. & ECHO. & ECHO.
ECHO "*************** Instalando Flask e Dependencias ***************" & ECHO.
TIMEOUT 5
.venv\Scripts\pip.exe install -e .
run.bat


:NOVENV
run.bat
pause
