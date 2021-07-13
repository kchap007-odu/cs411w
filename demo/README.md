# Setting up Flask

- Windows
  python -m venv venv
  venv\Scripts\activate
  pip3 install --trusted-host pypi.org flask

- Linux

# Setting up server

- Powershell
  $env:FLASK_APP = "hello"
  flask run

- Bash
  export FLASK_APP=hello
  flask run

# Retrieving the data

Go to <a href="http://127.0.0.1:5000/">loopback</a>
