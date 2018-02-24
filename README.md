# Vue 2.0 MeuBolsoWeb

software architecture:
* Client side: VUE (https://vuejs.org/v2/guide/) + JavaScript
* Server side: Python + Flask (http://flask.pocoo.org/)
* Database: SQLite (https://www.sqlite.org/)


preparing the environment:
* for coding: https://code.visualstudio.com/
* for database administration: SQLiteStudio (https://sqlitestudio.pl/index.rvt)
* to interact with code repository: any GitHub client like https://desktop.github.com/

Getting the source code and dependencies:
1) download the source code (https://github.com/giselermf/MeuBolsoWeb) to a folder in your computer
2) install python 3 https://www.python.org/
3) study and install npm (https://docs.npmjs.com/getting-started/what-is-npm)
4) go to the source code folder in your computer (where the file package.json is) and run "npm install".
5) a lot of libraries will be downloaded to folder node_modules/

to start the application:
1) in server/flask:
  export FLASK_APP=flask.py
  flask run
  
2) in src:
  npm run dev
