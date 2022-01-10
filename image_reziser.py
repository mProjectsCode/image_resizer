import json
from pathlib import Path
from PIL import Image

DEFAULT_CONFIG = """{
    "sizes": [
        "1080",
        "720",
        "480",
        "360",
        "240"
    ],
    "folderAddon": "_resized"
}"""
CONFIG_NAME = '.resizeConfig'


def enterFolderPath():
    folderPathString = input('Enter Folder Path String: ')
    confirmation = input('Is this the correct Location? \"' +
                         folderPathString + '\" (y/n) ')
    print('')
    if confirmation.lower() == 'y':
        return folderPathString
    else:
        return enterFolderPath()


def scanFolder(p: Path):
    if not (newFolderPath / p).exists():
        (newFolderPath / p).mkdir()
    for e in (folderPath / p).iterdir():
        if e.is_file():
            if str(e).lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                resizeImage(e)
        else:
            e = e.relative_to(folderPath)
            scanFolder(e)


def resizeImage(p: Path):
    f = newFolderPath / p.relative_to(folderPath).with_suffix('')
    if not f.exists():
        f.mkdir()
    i = Image.open(p)
    for s in imageSizes:
        s = int(s)
        heightPercent = float(s) / float(i.size[1])
        widthSize = int(float(i.size[0]) * float(heightPercent))
        j = i.resize((widthSize, s))
        j.save(f / modifyName(p.name, widthSize, s))


def modifyName(s: str, x: int, y: int):
    foundSuffix = False
    suffix = ''
    name = ''

    for i in range(len(s), 0, -1):
        if s[i-1] == '.':
            foundSuffix = True
        else:
            if foundSuffix:
                name += s[i-1]
            else:
                suffix += s[i-1]

    return ''.join([name[::-1], '_', str(x), 'x', str(y), '.', suffix[::-1]])


folderPathString = enterFolderPath()

folderPath = Path(folderPathString)

if not (folderPath / CONFIG_NAME).exists():
    with (folderPath / CONFIG_NAME).open("w", encoding="utf-8") as f:
        f.writelines(DEFAULT_CONFIG)
    print('No config file found so I created one for you named \"' +
          CONFIG_NAME + '\". ')
    input('After you finsished editing it hit enter... ')
else:
    print('Config file found! \"' + CONFIG_NAME + '\". ')
    input('Enter to proceed... ')

configFile = (folderPath / CONFIG_NAME).read_text()
config = json.loads(configFile)
newFolderPath = Path(folderPathString + config["folderAddon"])
imageSizes = config["sizes"]

scanFolder(Path(''))
