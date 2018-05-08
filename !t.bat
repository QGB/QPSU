:cyg usage
: { qgb } master » ./\!t.bat


@echo off
set py=G:\python27\python.exe
set py=G:\QGB\Anaconda2\python.exe

: echo import U,T,N,F
: echo U.test()

%py% -c "import U;U.test()"
: echo import Win
: echo import Clipboard


pause
