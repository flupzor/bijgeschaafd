git config --global user.email "travis@travis"
git config --global user.name "Travis"
cd website
python ./manage.py test --settings=settings_dev
