for %%i in (%~dp0) do @set wsDriver=%%~di
set QGB=%wsDriver%\QGB\
if not defined wspath (set wsPath=%wsDriver%\QGB\babun\cygwin\home\qgb\wshell\)

call %wsPath%up %*