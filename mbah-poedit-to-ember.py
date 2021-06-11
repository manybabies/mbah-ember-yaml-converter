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

def get_curly_fields(val, curlyfields=[], unmatched = False):
    if type(val) == dict:
        # A spot of recursion for nested dicts
        for key0, val0 in val.items():
            curlyfields, unmatched = get_curly_fields(val0, curlyfields= curlyfields, unmatched = unmatched)  
    elif type(val) == str:
        pos=0
        while True:
            posstart = val.find('{', pos)
            if posstart ==-1:
                break

            # Create list of all the nested curly braces
            innerbraces=[]
            posstart_inner = val.find('{', posstart+1)
            posend = val.find('}', posstart)
            if posend==-1:
                unmatched = True          
                break
            while posstart_inner>0 and posstart_inner<posend:
                # Inner curly braces
                posend_inner= posend
                posend = val.find('}', posend_inner+1)
                if posend==-1:
                    unmatched = True          
                    break
                innerbraces.append([posstart_inner, posend_inner])
                posstart_inner = val.find('{', posend_inner+1)


            # Piece together all of the parts around the inner braces
            curly = ''
            pos = posstart + 1
            for innerbrace in innerbraces:
                curly += val[pos:innerbrace[0]] + '{###}'
                pos = innerbrace[1] + 1
            curly += val[pos:posend]
            
            if curly not in curlyfields:
                curlyfields.append(curly)
            
            pos=posend+1
    
    return curlyfields, unmatched

# Location of yaml files exported from poedit
poeditor_path='export_from_poeditor'
# Location of ember framekit translations folder
git_mbah_elf_path='/home/cusackrh/repos/mbah-ember-lookit-frameplayer/translations'

# Scan the original en-us file for its curly fields
with open(path.join(git_mbah_elf_path,f'en-us.yaml')) as f:
    ymlin = yaml.load(f, Loader=yaml.BaseLoader)
    en_curlyfields, unmatched = get_curly_fields(ymlin)
    if unmatched:
        raise(Exception('Original en-us.yaml has unmatched curly braces'))
   


# List of languages
dest_lang=['pt']

for lang in dest_lang:
    with open(path.join(poeditor_path,f'{lang}.yaml')) as f:
        ymlin = yaml.load(f, Loader=yaml.BaseLoader)
        ymlout = {}

        # Build a list of fields in curly brackets
        curlyfields, unmatched = get_curly_fields(ymlin, curlyfields=[])
        
        waserror = False
        for curlyfield in curlyfields:
            if not curlyfield in en_curlyfields:
                waserror = True
                print(f'Curly field "{curlyfield}" not in original US version')
        if waserror:
            raise(Exception('One or more unknown curly fields'))

        for key, val in ymlin.items():
            fields = key.split('.') # assumes no '.' within original yaml keys
            # create/navigate into hierarchical dict where multiple fields
            el = ymlout
            for field in fields[:-1]:
                if not field in el:
                    el[field] = {}
                el=el[field]
            # set destination key at leaf node of hierarchy
            el[fields[-1]] = val
            

        print(curlyfields)

    # Write out
    with open(path.join(git_mbah_elf_path,f'{lang}.yaml'),'w') as f:
        yaml.dump(ymlout, f, allow_unicode=True)


