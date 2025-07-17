# HOW to RUN

## Linux

- Open the shell on repo
- execute `<source | .> create_venv.sh` for create/activate python virtual environment
- execute `install_requirements.sh` for install dependencies
- finally, run with cmd `python3 app.py`
- (optional) if you want to stop application: `ctrl+c`

### TODO

- Save the DONE_URL_LIST content in a JSON file, when stop the app on `ctrl-c`
- Load the URLs downloaded in the file created by the function trigged on `ctrl-c` (stop)