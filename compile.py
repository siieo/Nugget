from sys import platform, argv
import os
import PyInstaller.__main__

target_arch = None
for n in argv:
    if n.startswith("--target-arch="):
        print(f"Target arch: {n}")
        target_arch = n

args = [
    'main_app.py',
    '--hidden-import=zeroconf',
    '--hidden-import=pyimg4',
    '--hidden-import=zeroconf._utils.ipaddress',
    '--hidden-import=zeroconf._handlers.answers',
    '--collect-all=devicemanagement',
    '--add-data=files/:./files',
    '--copy-metadata=pyimg4',
    '--onedir',
    '--noconfirm',
    '--name=Nugget',
    '--icon=nugget.ico',
    '--strip',  # remove debug symbols
    '--exclude-module=tkinter',
    '--exclude-module=unittest',
    '--exclude-module=pydoc',
    '--exclude-module=tests',
    '--exclude-module=numpy.random._examples',
]

if target_arch is None:
    args.append('--optimize=2')

if platform == "darwin":
    args.append('--windowed')
    args.append('--osx-bundle-identifier=com.leemin.Nugget')
    if target_arch is not None:
        args.append(target_arch)

    # Optional: macOS code signing if present
    try:
        import secrets.compile_config as compile_config
        args.append('--osx-entitlements-file=entitlements.plist')
        args.append(f"--codesign-identity={compile_config.CODESIGN_HASH}")
    except ImportError:
        print("No compile_config found, skipping codesign...")

elif os.name == 'nt':
    args.append('--version-file=version.txt')
    args.append('--add-binary=.\\status_setter_windows.exe;.')
    if os.path.exists("ffmpeg/bin"):
        args.append('--add-data=ffmpeg/bin:ffmpeg/bin')
    else:
        print("ffmpeg not found!")

# Run PyInstaller with args
PyInstaller.__main__.run(args)