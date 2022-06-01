

## setup

- install virtual environment and python dependencies

```bash
git clone
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

- install node modules for the json-server (backend for cli app)
```bash
npm install
```


## initialize storage

```bash
pcmd utils data-init
```

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


## LOGGER

- example config: https://stackoverflow.com/q/49012123
- log handlers: https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers

## tests

> ?? How to parallelize the tests ??

- basic command `pytest --tb=no --lf`
  - `--lf` is the flag you use to run only the last failed,test suite fails often because server has issues keeping up with requests
- change the verbosity of traceback when error happens `--tb=no` and `-tb=short` are common
- to run a test or group of tests that match a name patter use `-k` followed by name pattern
- to see each test result detail increase verbosity with `-v`
- to only run tests that last failed add `--lf`
- to see logging output add `-s`