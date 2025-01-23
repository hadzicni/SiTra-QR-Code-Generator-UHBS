# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Only collect essential babel data
babel_data = collect_data_files('babel', includes=['*.dat'])
tkcalendar_data = collect_data_files('tkcalendar')

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('usblogo.png', '.'),
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
    ],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy', 'notebook', 'test', 'tests',
        'lib2to3', 'pygame', 'PySide2', 'PyQt5', 'PyQt6', 'IPython', 'sphinx',
        'jedi', 'docutils', 'setuptools', 'pydoc'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,  # Changed to True for faster startup
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
    icon='appicon.ico',
    version='file_version_info.txt',
    uac_admin=False,
    uac_uiaccess=False
)
