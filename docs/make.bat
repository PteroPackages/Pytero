@ECHO OFF

PUSHD %~dp0

:: Command file for Sphinx documentation

IF "%SPHINXBUILD%" == "" (
	SET SPHINXBUILD=sphinx-build
)
SET SOURCEDIR=.
SET BUILDDIR=_build

%SPHINXBUILD% >NUL 2>NUL
IF ERRORLEVEL 9009 (
	ECHO.
	ECHO.The 'sphinx-build' command was not found. Make sure you have Sphinx
	ECHO.installed, then set the SPHINXBUILD environment variable to point
	ECHO.to the full path of the 'sphinx-build' executable. Alternatively you
	ECHO.may add the Sphinx directory to PATH.
	ECHO.
	ECHO.If you don't have Sphinx installed, grab it from
	ECHO.https://www.sphinx-doc.org/
	EXIT /b 1
)

IF "%1" == "" GOTO help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
GOTO end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
POPD