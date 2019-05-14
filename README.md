# How to use the Virtual Environment

Use all those commands in CMD **NOT** Powershell
1. Install virtualenvwrapper for windows `pip install virtualenvwrapper-win`
2. `mkvirtualenv -a path/to/project/ blog` Create new virtual environment called 'blog' and associated to the project path.
3. `workon blog` Select the virtual environment.
4. `pip install -r requirements.txt` Install all needed packages into the virtual environment.
5. `flask run` Run the server.