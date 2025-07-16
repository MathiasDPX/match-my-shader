echo Installing Python dependencies...
pip install -r requirements.txt
pip install PyInstaller

cd game

echo Building...
pyinstaller \
	-D main.py \
	-n match_my_shader \
	--add-data "challenges:challenges" \
	--add-data "docs:docs" \
	--add-data "icon.ico:." \
	--icon "icon.ico" \
	--noconsole \
	--clean
