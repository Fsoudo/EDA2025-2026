@echo off
setlocal
set SRC=src
set OUT=out

echo [1/2] Compiling...
if not exist %OUT% mkdir %OUT%
javac -encoding UTF-8 -d %OUT% %SRC%\*.java
if %errorlevel% neq 0 ( echo COMPILE ERROR & pause & exit /b 1 )

echo [2/2] Running...
echo.
java -cp %OUT% src.Main
pause
