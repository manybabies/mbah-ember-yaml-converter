'''
PURPOSE
MBAH wish to provide translations for the files used by ember, like this one:
https://github.com/manybabies/mbah-ember-lookit-frameplayer/blob/master/translations/en-us.yaml
These files can be imported into our default translation tool, poeditor. But hierarchical structures get collapsed. So for example:
    exp-lookit-exit-survey:
        confirm-birthdate: Please confirm your child's birthdate
        why-birthdate: We ask again just to check for typos during registration or accidental selection of a different child at the start of the study.
becomes
    exp-lookit-exit-survey.confirm-birthdate: Please confirm your child's birthdate
    exp-lookit-exit-survey.why-birthdate: We ask again just to check for typos during registration or accidental selection of a different child at the start of the study.

This code converts the latter format back into the former. It requires that there are not "." in the original yaml keys.

Rhodri Cusack Trinity College Dublin 2021-05-22
'''
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


