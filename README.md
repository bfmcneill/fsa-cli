

## setup

- install virtual environment and python dependencies

```bash
git clone
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

- install node modules for the json-server (backend for cli app)
````bash
npm install

```


## reseed database

```json
{
  "customers": [],
  "accounts": []
}
```

## create customer profile

```bash
pcmd customer create-profile \
--email jim@bo.com \
--first-name jim \
--last-name bo
```

## find customer by email

```bash
pcmd customer find-by-email --email jim@bo.com
```

## create customer account

```bash
pcmd customer create-account --account-type CHECKING
```