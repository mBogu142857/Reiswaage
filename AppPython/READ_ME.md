# App

## Version Python and PyCharm
For developing this tool, we used :
* Python: v3.9
* PyCharm: 2020.2.5

## Content of the project folder
 - **mainapplication.py**: main file running the app (script + GUI visualization)
 
 - **model (folder)**: reference to all classes for the application
 
 - **views (folder)**: gui related files
    - **main_view.py**: GUI definition and properties

     
 - **controllers (folder)**: 
    - **main_controller.py**: interactivity of the GUI and launch of the script for the app
 
 - **READ_ME.md**
 
 - **build (folder)**: all files to compile the app into an exe file via pyinstaller. 
     To launch the export, in the terminal type: 
        ```
        cd build
        build_standalone_exe.bat
        ```
 
 - **requirement.txt**: dependencies file information 

## Dependencies

To install all the dependencies, open the terminal inside the EDI PyCharm, make sure that you have create and Virtual 
Environment. The virtual environment is made with Virtualvenv. It is possible to confirm that you are actually inside 
a virtual environment by looking the prompter of the terminal, it should have "(venv)" at the beginning of the line.

There is several ways of installing dependencies:
1) open the file requirements.txt which are at the root of the project folder. Then PyCharm will ask you for install the
 dependencies.
    Note: Sometimes the network has restriction about downloading some dependencies.
2) If the first solution does not work, open the terminal inside the IDE and write this followed commands and enter:
```
pip install -r requirements.txt
```
3) Manually via the settings of the current project (File --> Settings --> Python Project --> Python Intepreter). 
Click on the plus sign on the side of the window, and select the package to install
 ## Versions 
 v0
 
 ## How to run/debug the App with the GUI
In the terminal:
 ```
mainapplication.py 
```
In Pycharm: 
Run (or debug) the mainapplication.py file (green triangle or green spider, top-right corner of the pycharm window)
Note: the first you launch an application, the triangle might not be there. Right click with the mouse on the window 
with the code of main_application.py and click on run/debug.   

