# -*- mode: python -*-

block_cipher = None

a = Analysis(['slouchy.py'],
             pathex=['/home/me/PROJECTS/slouchy'],
             binaries=None,
             datas=[('README.md', ''),
                    ('LICENSE', ''),
                    ('slouchy.ini', ''),
                    ('slouchy_icon.png', ''),],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='slouchy',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='slouchy_icon.png')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='slouchy')
