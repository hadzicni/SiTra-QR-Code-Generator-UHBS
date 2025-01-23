# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect babel data files
babel_data = collect_data_files('babel')
tkcalendar_data = collect_data_files('tkcalendar')

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/usblogo.png', '.'),
        *babel_data,
        *tkcalendar_data,
        ('main.py', '.'),
    ],
    hiddenimports=[
        'babel.numbers',
        'babel.dates',
        'tkcalendar',
        'reportlab.graphics.barcode.qr',
        'reportlab.graphics.barcode.common',
        'PIL._tkinter_finder',
        'main'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add version info
a.datas += [('file_version_info.txt', 'file_version_info.txt', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SiTra-QR-Generator',
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
    icon='assets/appicon.ico',
    version='file_version_info.txt',
    uac_admin=False,
    uac_uiaccess=False
)
