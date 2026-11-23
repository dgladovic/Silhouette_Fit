import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
# M04: always start E0 from the 11 historical keys (ignore an existing keys.json); refine() writes the new keys.json
os.environ['M04_BASE_KEYS'] = '1'
sys.path.insert(0, os.path.join(HERE, '..', '..', '_common'))
import study
study.run_experiment(os.path.dirname(HERE), 'E0')
