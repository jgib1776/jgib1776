cd C:\Users\jgibf\Documents\Python
py -m venv gibbous
C:\Users\jgibf\Documents\Python\gibbous\Scripts\activate.bat
py -m pip install --upgrade pip
py -m pip install Django
py -m pip install psycopg2
py -m pip install djangorestframework

# Setup sublimetext: https://www.youtube.com/watch?v=xFciV6Ew5r4
# Install packages in sublime with Tools-->Command Pallete, 'Package Control: Install Package'
# Install 'Babel Snippets' for better java script syntax

# Django setup
django-admin startproject gibbous_dj
cd C:\Users\jgibf\Documents\Python\gibbous_dj
django-admin startapp api
# settings.py api.apps.ApiConfig
python manage.py makemigrations
python manage.py migrate

# Setup github  jgib1776
# Installed github-cli from https://github.com/cli/cli/releases/tag/v2.5.0
# https://cli.github.com/
# Login: github.com:https:No Github Creds:Auth Token Past  --> in keepass
gh auth login
# Install git https://gitforwindows.org/
git config --global user.name "Joe Gibfried"
git config --global user.email "jbgib1776@gmail.com"

# Git initial setup
cd C:\Users\jgibf\Documents\Python\gibbous_dj
git init
gh repo create gibbous_jd --private --source=. --remote=upstream
#gh repo delete gibbous
git status
# Add existing to git: git add <file>
git add api gibbous_dj db.sqllite3 manage.py
git status
git commit -m "initial"
git branch -M main
git remote add origin https://github.com/jgib1776/jgib1776.git
git push -u origin main


# git management.  After a local change...
git status
git diff
git add .
git commit -m "message"
git push




# Normal operations
cd C:\Users\jgibf\Documents\Python
C:\Users\jgibf\Documents\Python\gibbous\Scripts\activate.bat
cd C:\Users\jgibf\Documents\Python\gibbous_dj
python manage.py runserver


