@echo off
REM no password questions

sc stop wuauserv
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" ^
 /v NoLocalPasswordResetQuestions ^
 /t REG_DWORD ^
 /d 1 ^
 /f
title SetupComplete - Windows Update Control

REM ===============================
REM Disable automatic Windows Update
REM ===============================

REM Policy: Disable automatic updates
reg add HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU ^
 /v NoAutoUpdate /t REG_DWORD /d 1 /f

REM Prevent auto-restart for updates
reg add HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU ^
 /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f

REM Set updates to "Notify only" if user enables them later
reg add HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU ^
 /v AUOptions /t REG_DWORD /d 2 /f

REM Disable Update Orchestrator (Windows 10/11)
sc config UsoSvc start= disabled
sc stop UsoSvc

REM Disable Windows Update service
sc config wuauserv start= disabled


exit /b 0


