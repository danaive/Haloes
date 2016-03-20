mysql -u root -e "drop database haloes;"
mysql -u root -e "create database haloes;"
find . -name "00*.py" | xargs rm
python manage.py makemigrations
python manage.py migrate