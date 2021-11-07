@echo off
set command=~/work/src/pj/m3u8maker/m3u8maker.py -r -s N:\Music\test\Playlist -i
setlocal ENABLEDELAYEDEXPANSION
for %%f in (%*) do (
    set command=%command% ^'%%~f%^'
)
ssh nevec !command!

PAUSE