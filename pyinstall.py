# -*- mode: python -*-

# if you use pyqt5, this patch must be adjusted
# https://github.com/bjones1/pyinstaller/tree/pyqt5_fix

block_cipher = None

a = Analysis(['ui.py'],
             pathex=['C:\\Users\\user\\Desktop\\JP (2)\\JP'],
             binaries=[],
             datas=[],
             hiddenimports=["./crawling",

                            ],
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
          exclude_binaries=True,
          name='run',
          debug=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='run')