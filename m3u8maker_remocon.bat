@echo off

for %%f in (%*) do (
    ssh nevec echo ^'%%~f%^'
)