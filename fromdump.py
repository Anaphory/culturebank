
import os
from shutil import copytree


if __name__ == '__main__':
    src = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(os.path.split(src)[0], 'grambank')
    if src != dest:
        copytree(src, dest)
    os.chdir(dest)
    print("""\
#---------------------------------------------------------#

Run
    cd grambank
    pip install -r requirements.txt
    python setup.py develop
    python grambank/scripts/unfreeze.py sqlite.ini
    pserve sqlite.ini

or equivalent to start the grambank web app accessible at

    http://localhost:6543

#---------------------------------------------------------#
""")
