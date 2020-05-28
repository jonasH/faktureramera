# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ["src/pyside2_app.py"],
    pathex=["/home/jonas/Kod/faktureramera"],
    binaries=[],
    datas=[
        ("src/ui/faktureramera.ui", "ui"),
        ("src/ui/jobform.ui", "ui"),
        ("src/ui/newcustomerform.ui", "ui"),
        ("src/ext/fm.sql", "ext"),
    ],
    hiddenimports=["PySide2.QtXml"],
    hookspath=[],
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
    [],
    exclude_binaries=True,
    name="FaktureraMera",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="FaktureraMera",
)
