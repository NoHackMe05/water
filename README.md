# Water

Recover GPS coordinates of drinking water points in France

## Install

### Installing Python packages :

```
python3 -m venv mon_env
source mon_env/bin/activate
pip install -r requirements.txt
deactivate
```

### Creating the configuration file

```
cp .env.example .env
```

## Setting

The following variables must be configured in the .env file:

- STORE_ENDPOINT : url of the api that will store the information
- API_KEY : api key for STORE_ENDPOINT

## Usage

```
python get_water.py
```
