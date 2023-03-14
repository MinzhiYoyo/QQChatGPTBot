@echo off
setlocal
set JAVA_BINARY=java
%JAVA_BINARY% -Dmirai.slider.captcha.supported -jar mcl.jar %* 

set EL=%ERRORLEVEL%
if %EL% NEQ 0 (
    echo Process exited with %EL%
    pause
)
