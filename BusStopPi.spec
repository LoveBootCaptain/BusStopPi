#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

PATH = os.path.realpath('src/')
print(PATH)

block_cipher = None

added_files = [
    (PATH + '/font', 'src/font'),
    (PATH + '/icons', 'src/icons')
]

a = Analysis([PATH + '/BusStopPi.py'],
             pathex=[PATH],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='BusStopPi',
          debug=True,
          strip=False,
          upx=False,
          console=False, icon=PATH + '/icons/BusStopPi.icns')
app = BUNDLE(exe,
             name='BusStopPi.app',
             icon=PATH + '/icons/BusStopPi.icns',
             bundle_identifier=None)
