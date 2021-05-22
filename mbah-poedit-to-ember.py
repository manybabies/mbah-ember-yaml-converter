
import yaml
import polib
from os import path

# Location of yaml files on filesystem
git_mbah_elf_path='/home/cusackrh/repos/mbah-ember-lookit-frameplayer/translations'
poeditor_path='export_from_poeditor'

dest_lang=['pt']

for lang in dest_lang:
    with open(path.join(poeditor_path,f'{lang}.yml')) as f:
        yml = yaml.load(f)
        
        ymlout = {}

        for key, val in yml.items():
            fields = key.split('.')
            el = ymlout
            for field in fields[:-1]:
                if not field in el:
                    el[field] = {}
                el=el[field]
            el[fields[-1]] = val
        
    with open(path.join(git_mbah_elf_path,f'{lang}.yaml'),'w') as f:
        yaml.dump(ymlout, f, allow_unicode=True)


