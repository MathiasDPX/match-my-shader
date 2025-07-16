cd game
pyinstaller \
	-D main.py \
	-n match_my_shader \
	--add-data "challenges:challenges" \
	--add-data "docs:docs" \
	--add-data "icon.ico:." \
	--icon "icon.ico" \
	--clean
