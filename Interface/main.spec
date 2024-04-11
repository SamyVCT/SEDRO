# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\cocol\\Documents\\Cours\\2A\\PIE SEDRO\\SEDRO\\Interface'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('loading.png','C:\\Users\\cocol\\Documents\\Cours\\2A\\PIE SEDRO\\SEDRO\\Interface\\Images\\loading.png', "DATA")]
a.datas += [('basedrone2.png','C:\\Users\\cocol\\Documents\\Cours\\2A\\PIE SEDRO\\SEDRO\\Interface\\Images\\basedrone2.png', "DATA")]
a.datas += [('basedrone.png','C:\\Users\\cocol\\Documents\\Cours\\2A\\PIE SEDRO\\SEDRO\\Interface\\Images\\basedrone.png', "DATA")]
a.datas += [('drone.png','C:\\Users\\cocol\\Documents\\Cours\\2A\\PIE SEDRO\\SEDRO\\Interface\\Images\\drone.png', "DATA")]
a.datas += [('drawn_grid.png','C:\\Users\\cocol\\Documents\\Cours\\2A\\PIE SEDRO\\SEDRO\\Interface\\Images\\drawn_grid.png', "DATA")]
a.datas += [('ultralytics','C:\\Users\\cocol\\AppData\\Roaming\\Python\\Python38\\site-packages\\', "DATA")]



pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SEDRO',
          debug=False,
          strip=False,
          upx=True,
          console=False)