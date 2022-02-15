pyinstaller.exe ^
    --windowed ^
    --hidden-import=PySide2.QtXml ^
    --onedir ^
    --specpath=specs ^
    --distpath=distributables ^
    --workpath=temp ^
    --name=Merging_tool_v2 ^
    --noconfirm ^
    ..\mainapplication.py