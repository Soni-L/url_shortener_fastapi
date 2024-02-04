## Live site preview :rocket:
https://url-shortener-sl-1dd71db24af7.herokuapp.com/docs

#### Example: resolving a shortened url :gift:
https://url-shortener-sl-1dd71db24af7.herokuapp.com/qmzLhp

## Local Installation 🛠
1. Make sure you have python version 3.10 or up installed

2. Clone the git repository to your machine

```
git clone https://github.com/Soni-L/url_shortener_fastapi.git
```

3. Run the following command for local installation

```
pip install -r requirements.txt
```

## Running the application &#9654;
After install run the following to start the app on http://localhost (http://127.0.0.1) port 80

```
python -m uvicorn main:app --host 0.0.0.0 --port 80
```

## Running the tests ✔️
Install `pytest`:

```
python -m pip install pytest
```

Execute the tests:

```
python -m pytest
```