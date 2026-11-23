import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '_common'))
import study
study.run_experiment(os.path.dirname(HERE), 'E4')
