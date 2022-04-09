import sys, os

def get_platform():
    platforms = {
        'linux': 'Linux',
        'linux1': 'Linux',
        'linux2': 'Linux',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]

if get_platform() == 'Windows':
    os.system('python Windows\\main.py')
elif get_platform() == 'Linux':
    os.system('python Linux/main.py')
else:
    print('Unsupported platform')