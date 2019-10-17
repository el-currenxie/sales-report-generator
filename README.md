OSX only

python3

pip3 install virtualenv==16.1
virtualenv venv --no-site-pasckage

archive HEAD -o ${PWD##*/}.zip

pyinstaller sales_generator.spec