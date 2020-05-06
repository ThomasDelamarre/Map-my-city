import os
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=%s' % "Map my city",
    '--onefile',
    '--console',
    os.path.join('main_all.py'),
])