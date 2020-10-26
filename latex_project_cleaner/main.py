#!/usr/bin/env python3
__author__ = "Thomas Eiband"

""" This tool cleans a LaTeX project to make it ready for submission.
It does the following steps:
- delete all figure sourcefiles
- delete all figures, which are not used in the document
- delete all auxiliary files
- delete compiled main document pdf: root.pdf

This actions cannot be undone! Make sure to create a backup before you run this tool.
Images that are mentioned in comments will NOT be removed.
"""

import os
import pathlib
import glob
import shutil
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-V', '--verbose', action='store_true')
    args = parser.parse_args()
    verbose = args.verbose

    clean_tasks = ['images', 'comments', 'auxiliary', 'main_pdf']

    def new_task():
        print('------------------------')

    ret = input(
        "Don't blame me, if this tool destroys "
        "something you created with hard work.\nType 'yes' to continue:\n")
    if ret != 'yes':
        exit(0)

    project_dir = os.getcwd()

    if not glob.glob(os.path.join(project_dir, '*.tex')):
        print("I did not find any *.tex files here, this seems not to be a latex project directory. Exiting.")
        exit(-1)

    if 'images' in clean_tasks:
        new_task()
        figure_source_dirs = ["figures/src", "images-src"]
        figure_dirs = ["figures", "images"]
        print("removing figure source files...")
        for d in figure_source_dirs:
            cur_dir = os.path.join(project_dir, d)
            if pathlib.Path.exists(pathlib.Path(cur_dir)):
                print(f"\tremoving directory {cur_dir}...")
                shutil.rmtree(cur_dir)
            else:
                print(f"\tdid not find figure source files in {d}. skipping.")
        # In case source files are within normal figure folder, remove them by extension
        print("\tremoving figure source files in figure folders...")
        for d in figure_dirs:
            cur_dir = os.path.join(project_dir, d)
            cur_src_figures = glob.glob(os.path.join(d, '*.svg'))
            for f in cur_src_figures:
                if os.path.isfile(f):
                    if verbose:
                        print('\t\t' + f)
                    os.remove(f)

        print("searching included figures in documents...")
        all_figures = []
        for d in figure_dirs:
            #cur_dir = os.path.join(project_dir, dir)
            all_figures += glob.glob(os.path.join(d, '*.pdf'))
        tex_files =[]
        included_figures = []
        for path in pathlib.Path(project_dir).rglob('*.tex'):
            tex_files.append(path)
            with open(path,'r') as texf:
                tex_str = texf.read()
                i = 0
                while i < len(tex_str):
                    ret = tex_str[i:].find('\includegraphics')
                    if ret < 0:
                        break
                    i = i + ret
                    ret = tex_str[i:].find('}')
                    if ret < 0:
                        break
                    i2 = i + ret
                    include_str = tex_str[i : i2+1]
                    i = i2
                    filename = include_str[include_str.rfind('{')+1 : -1]
                    if not filename.endswith('.pdf'):
                        filename += '.pdf'
                    #print(filename)
                    included_figures.append(filename)
        print(f"\tfound {len(included_figures)} figures")
        if verbose:
            print('', *included_figures, sep='\n\t')

        #print("find intersection...")
        #keep_figures = list(set(all_figures) & set(included_figures))
        print("check for difference in included and available figures...")
        delete_figures = list(set(all_figures) - set(included_figures))
        if delete_figures:
            print(f"I will remove {len(delete_figures)} unused figures.")
            print('', *delete_figures, sep='\n\t')
            ret = input("Type 'yes' to continue.\n")
            if ret == 'yes':
                print("removing figures...")
                for fig in delete_figures:
                    os.remove(fig)
        else:
            print("\tnothing to do.")
    if 'comments' in clean_tasks:
        new_task()
        print("removing all comments from tex-files")
        for path in pathlib.Path(project_dir).rglob('*.tex'):
            tex_files.append(path)
            new_str = ""
            with open(path, 'r') as texf:
                tex_str = texf.read()
                i = 0
                while i < len(tex_str):
                    ret = tex_str[i:].find('%')
                    if ret < 0:
                        break
                    i = i + ret
                    ret = tex_str[i:].find('\n')
                    if ret < 0:
                        break
                    tex_str = tex_str[:i] + tex_str[i2:]
                    #i2 = i + ret
                    #remove_str = tex_str[i: i2 + 1]
                    #i = i2
                # write back document without comments
                with open(path, 'w') as texf:
                    texf.write(tex_str)

    if 'aux' in clean_tasks:
        new_task()
        print("delete auxiliary files")
        file_patterns = '*.gz,root.pdf,*.aux,*.out,*.bbl,*.blg,*.log,*.idea,__pycache__'.split(',')
        for pattern in file_patterns:
            cur_dir = os.path.join(project_dir, pattern)
            for f in glob.glob(cur_dir):
                if os.path.isfile(f):
                    print('\t', f)
                    os.remove(f)
    if 'main_pdf' in clean_tasks:
        new_task()
        for f in glob.glob(os.path.join(project_dir, '*.pdf')):
            os.remove(f)

    print("\nSuccess")


