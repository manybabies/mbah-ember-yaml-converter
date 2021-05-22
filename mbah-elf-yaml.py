
import yaml
import polib
from os import path

# Location of yaml files on filesystem
git_mbah_elf_path='/home/cusackrh/repos/mbah-ember-lookit-frameplayer/translations'
po_path='/home/cusackrh/repos/mbah-ember-lookit-frameplayer/translations/po'

dest_lang=['pt_BR']

for lang in dest_lang:
    pofn = path.join(po_path,lang + '.po')
    if not path.exists(pofn):
        print(f'No po for {lang}, creating')
        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'cusackrh@tcd.ie',
            'Language-Team': 'Many Babies at Home',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }
    else:
        po = polib.pofile(pofn)

    with open(path.join(po_path))
        with open(path.join(git_mbah_elf_path,'en-us.yaml')) as f:
            en = yaml.load(f)

            decipher(po, )

        for entry in po:

        print(en)

