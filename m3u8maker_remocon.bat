@echo off
set command=m3u8maker -s N:\Music\test\Playlist -i
setlocal ENABLEDELAYEDEXPANSION
for %%f in (%*) do (
    set command=%command% ^'%%~f%^'
)
ssh nevec !command!