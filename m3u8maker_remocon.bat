@echo off
set command=$HOME/.local/bin/m3u8maker -r -s N:\Music\test\Playlist -i
setlocal ENABLEDELAYEDEXPANSION
for %%f in (%*) do (
    set command=%command% ^'%%~f%^'
)
ssh nevec !command!

PAUSE