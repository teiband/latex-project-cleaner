#import pytest
import os
import shutil
import latex_project_cleaner.main
import runpy
import subprocess

if __name__ == '__main__':
    test_data_src_dir = 'test_latex_project'
    test_data_dir = 'test_latex_project2'
    main_path = '../../latex_project_cleaner/main.py'

    # recreate test latex project
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
    shutil.copytree(test_data_src_dir, test_data_dir,)

    os.chdir(test_data_dir)
    subprocess.run(main_path)
