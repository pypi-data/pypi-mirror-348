pip install %RECIPE_DIR%\dist\ep_bolfi-${VERSION}-py3-none-any.whl
rd -r %RECIPE_DIR%\dist
rd -r %PREFIX%\dist
if errorlevel 1 exit 1