@echo off
set command=$HOME/.local/bin/m3u8maker -sl -r -s 'N:\Music\test\Playlist' -i

for %%f in (%*) do (
    echo ^'%%~f%^'
    call:append-args "^'%%~f%^'"
)
echo %command%
ssh nevec %command%
PAUSE

:append-args
set command=%command% %~1
exit /b