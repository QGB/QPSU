:usage ./t.bat|python

@echo off
set py=C:\python27\python.exe
: echo import U,T,N,F
: echo U.test()

%py% -c "import U;U.test()"
: echo import Win
: echo import Clipboard



