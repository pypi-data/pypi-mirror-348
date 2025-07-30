from .pm import run

import os

submodule = os.environ.get('submodule', '')

if submodule == 'bio_pm':
    run()
