# Stock_Price_Scraping 

## Project Definitions...


### Virtual Environment with Project Requirements
> ``Python 3.9.0`` was used to develop for the homework assignments.\
> You can find the required python packages and their versions in ``requirements.txt`` file.\
> Thanks to ``Makefile``, you can create a virtual environment, install required packages and delete virtual environment.
> If you do not want to use virtual environment, then you need to install required packages in your base python interpreter.
> * make ``venv`` creates python virtual environment.
> * make ``require`` install required packages.
> * make ``clean`` delete venv file.

You can simply run the code like as follows from command line:
```console
**LINUX**
## For linux, you need to update the makefile commands compatible for linux environment.
...@...:project_root$ make venv
...@...:project_root$ make require
...@...:project_root$ python3 some_file_1.py
...@...:project_root$ python3 some_file_2.py

**WINDOWS**
project_root> make venv
project_root> make require
project_root> python some_file_1.py
project_root> python some_file_2.py
```
If you face problem about creating virtual environment from makefile, you can create virtual environment manually and
install packages from ``requirements.txt`` file.
