pyinstaller.exe ^
    --clean ^
    --hidden-import=PySide2 ^
    --hidden-import=PySide2.QtXml ^
    --hidden-import=scipy ^
    --hidden-import=matplotlib ^
    --hidden-import=marshmallow ^
    --hidden-import=peakutils ^
    --hidden-import=pandas ^
    --onefile ^
    --specpath=specs ^
    --distpath=distributables ^
    --workpath=temp ^
    --name=App ^
    --noconfirm ^
    ..\mainapplication.py