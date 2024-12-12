# bastion character generator

a python script for generating careers and character stats from roll playing game Electric Bastionland

## Description

The script rolls character stats, and uses the data file to generate other characteristics

## Using the script

* example usage:
```
python -i bastion_generator.py
jason = fail('jason')
```

```
{'career': 'LOST EXPEDITIONEER',
 'desc': 'You’ve been on a treasure hunting expedition before. You were the '
         'only survivor',
 'stats': [10, 10, 9],
 'hp': [6],
 'pocket money': [1],
 'get': 'YOU GET - Pair of pistols (d6 each).',
 'debt1': 'IF YOU ARE THE YOUNGEST PLAYER, THE WHOLE GROUP IS £10K IN DEBT '
          'TO...',
 'debt2': 'The Elephant Reimbursement House: Reclaimed ivory goods pay double '
          'their value against your debt.',
 'prompt1': 'WHAT WAS YOUR POSITION ON THE CREW?',
 'answer1': 'Counsellor:Take an aromatherapy kit.',
 'prompt2': 'WHAT DID YOU BRING BACK FROM THE EXPEDITION?',
 'answer2': 'Ambrosia Seed – A bag of golden seed that no animal can resist if '
            'thrown.'}
```
### Dependencies

* python

## Authors

Andrew Russell

## Version History

* 0.1
    * Initial Release
