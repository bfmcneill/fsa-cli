## CLI Actions

## create customer

```bash
pcmd customer create \
--email jim@bo.com \
--first-name jim \
--last-name bo
```

## create customer address

```bash
pcmd customer update-address \
--email "jim@bo.com" \
--line1 "8000 broadway street" \
--city Phoenix \
--state-code AZ \
--zip-code 85331
```

## create customer checking account

```bash
pcmd account create-checking --email jim@bo.com 
```

## create checking account transactions

```bash
pcmd account deposit --account-id 1 --amount 100 --memo "birthday gift"
pcmd account withdraw --account-id 1 --amount 100 --memo "birthday suit"
```

## features to be implimented

- view balance
- view accounts
- export transactions to csv

----

## How to setup your environment

- clone project to your computer
- create a python virtual environment
- activate virtual environment and install project dependencies
- install nodejs dependencies (this is required for the python CLI app to hit REST API endpoints)
- initialize json-sever `db.json file`
- rename logger config template
- start json-server
- run all tests

### clone project to your computer

```bash
git clone git@github.com:bfmcneill/fsa-cli.git
```

### create virtual environment

```bash
python -m venv venv
```

### activate virtual environment and install python dependencies

#### bash / zsh

```bash
source venv/bin/activate
pip install -e ".[dev]"
```

#### powershell

```powershell
.venv\scripts\activate
pip install -e .[dev]
```

- ### install node modules for the json-server (backend for cli app)

```bash
npm install
```

### initialize `db.json` storage

```bash
pcmd utils reset-db-json
```

### rename logger config template

- review the settings to make increase / decrease logging verbosity
- by default logger will display DEBUG to console

#### bash / zsh

```bash
mv ./config/logging.yml.temlpate ./config/logging.yml
```

#### powershell

```
Rename-Item -Path ".\configlogging.yml.temlpate" -NewName ".\config\logging.yml"
```

#### Additional information on python logger

- example config: https://stackoverflow.com/q/49012123
- log handlers: https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers

### start json-server

- note, this step requires `db.json` to be initialized with collections.  make sure you have completed the previous step titled `initialize db.json storage`
- in a separate terminal run the following command

```bash
npm run start:api
```

you should see the following output

```bash
> fsav@1.0.0 start:api
> json-server --watch ./data/db.json


  \{^_^}/ hi!

  Loading ./data/db.json
  Done

  Resources
  http://localhost:3000/accounts
  http://localhost:3000/customers
  http://localhost:3000/ledger
  http://localhost:3000/addresses
```

### run tests

- ensure the virtual environment is activated before running tests.  see previous step titled `create virtual environment`
```cmd
pytest --tb=no
```

#### Additional remarks about tests

- to see logging output add `-s`
- `--lf` is the flag you use to run only the last failed, test suite will sometimes fail if api server can't handle barrage of requests
- change the verbosity of traceback when error happens `--tb=no` and `-tb=short` are common
- to run a test or group of tests that match a name pattern use `-k` followed by name pattern
  - for example `-k cli` or `-k term_loan`
- to see each test result detail increase verbosity with `-v`