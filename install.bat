@ECHO OFF
IF EXIST .\.venv\ GOTO NOVENV
ECHO "*************** Criando um Ambiente Virtual ***************"
python -m venv .venv
ECHO "*************** Criando o Projeto Flask ***************"
.venv\Scripts\pip.exe install -e .
ECHO "*************** Executando o Projeto Flask ***************"
run.bat
pause


:NOVENV
ECHO "*************** Executando o Projeto Flask ***************"
run.bat
pause
