# Sales Report Generator

## OS

OSX only

## Environment

python3

## To develop

```bash
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python sales_generator.py
```

## To generator one executable binary

executable will go to `./dist`

```bash
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ ./package.sh
```

### other

```
pip3 install virtualenv==16.1
virtualenv venv --no-site-pasckage
archive HEAD -o \${PWD##\*/}.zip
pyinstaller sales_generator.spec
```

### test

import folder which contains the sale file
click fuiou
