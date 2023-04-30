from command import mssk8svm as mk8
import os

stdlib_dir = '{0}/k8s-install.log'.format(os.path.dirname(__file__))
print('LOG FILE : ', stdlib_dir)
mk8.__main__()