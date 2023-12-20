# -*- coding: utf-8 -*-
"""
# QUIPPL
Quick User Interface Portable Python Launcher - package a .py launcher
so you don't have to keep repackaging distributed code each update
----------

This tool is part of a complete package for rapid sharing of python
programs.  Many non-programmers would love to run your program but
don't want to worry about installing python and setting up the 
evironment.  QUIPPL helps the user to launch your program.

Step 1: package quippl using pyinstaller or nuitka 
(ideally in the same python environment used for the code you will be sharing)

Step 2: copy the site-packages from your python environment/python 
installation that will run your code into the "dist" folder holding the
QUIPPL executable

Step 3: share the packaged QUIPPL with your user to have them run your 
code as a python file (instead of worrying about re-packaging every update, 
you can just send over the new .py version of your file)

QUIPPL includes a GUI for selecting the py file to be run.  Alternatively
you can provide the location of the file and its needed arguments via 
command line, bypassing the GUI tool.  You can also provide a 
QUIPPL_config.txt file to provide the necessary path to the .py file and it's
arguments to bypass the need for the user to select/do anything

@author: Christopher Scott Ward 2022

"""

__version__ = '2.1.0'

#%% import libraries

import argparse
from PyQt5.QtWidgets import QFileDialog, QApplication
import os
import sys
import importlib



#%% define main
def main():
    print(
        '{}\n{}\nversion : {}'.format(
            'Thank you for using QUIPPL',
            'Quick User Interface Portable Python Launcher',
            __version__)
        )
    
    """
    Collect potential sources of the path to the python file
    """
    #%%
    # default state for availablility of path to python file is False
    command_line_available = False    
    quippl_config_available = False
    gui_selection_available = False
    
    # Collect command line arguments
    parser = argparse.ArgumentParser(description='QUIPPL')
    
    parser.add_argument(
        '--pypath', 
        help='path to the python file to run')
    parser.add_argument(
        '--pyargs', 
        help='a "quoted sting" with the arguments for the python file '
        +'if quotes are needed, use single quotes'
        )
    
    parsed_args = parser.parse_args()
    
    pypath = parsed_args.pypath
    pyargs = parsed_args.pyargs
    
    # Check if command line arguments were provided
    if pypath is not None:
        command_line_available = True
        print(f'pypath: {pypath}\npyargs: {pyargs}')

    # fix pyargs in case quotes are needed - replace with double quotes
    if pyargs is not None and len(pyargs) > 0:
        pyargs = pyargs.replace("'",'"')
        # command_line_selection = ' '.join([pypath, pyargs])
        command_line_selection = pypath
    
    
    # Check if QUIPPL_config.txt is present
    if os.path.isfile('QUIPPL_config.txt'):
        with open('QUIPPL_config.txt','r') as open_file:
            quippl_config_contents = open_file.read().replace('\n','')
            pyargs = {}
            # Check that config contents are not empty
            if len(quippl_config_contents.strip()) > 0:
                quippl_config_available = True
                print(f'QUIPPL_config: {quippl_config_contents}')    

                
    # use gui to get path to py file
    if not any([command_line_available,quippl_config_available]):
        print('No pypath or QUIPPL_config found. Launching GUI tool')
        # Use the pyqt filedialog to select a file 
        # (selected path should be element [0] of the returned list)
        app = QApplication(sys.argv)
        gui_selection_path = QFileDialog.getOpenFileName(
            None,
            'QUIPPL'
            ' - Select you Python File (*.py)',
            '',
            'Python File (*.py)')[0]
        pyargs = {}

        
        
        if gui_selection_path is not None and \
                len(gui_selection_path) > 0:
            gui_selection_available = True
            print(f'GUI selected pypath: {gui_selection_path}')    
            # gui_selection_path = gui_selection_path.join(['"','"'])
    
    
    # decide which path to use
    if quippl_config_available:
        print('...using python file specified in QUIPPL_config')
        path_to_use = quippl_config_contents
    elif command_line_available:
        print('...using pypath specified from command line')
        path_to_use = command_line_selection
    elif gui_selection_available:
        print('...using python file selected from GUI tool')
        path_to_use = gui_selection_path
    else:
        print('...no python file selected...terminating...')
    
    
    
    
    # launch the py file and use the cwd argument to set the working directory
    if any([
            quippl_config_available,
            command_line_available,
            gui_selection_available
            ]):
        if path_to_use[0] == '"' or path_to_use[0] == "'":
            full_path = os.path.realpath(path_to_use[1:-1])
        else:
            full_path = os.path.realpath(path_to_use)
        print(f'running: {full_path}')
        
        os.chdir(os.path.dirname(full_path))
        sys.path.append(os.path.dirname(full_path))
        print(f'using directory: {os.getcwd()}')
        
        launcher = importlib.import_module(
            os.path.splitext(os.path.basename(full_path))[0]
        )
        launcher.main(**pyargs)
    
    print(
        '\nQUIPPL Done\nPress "Enter" to Exit'
        )
    
    
#%% run main
if __name__ == '__main__':
    main()