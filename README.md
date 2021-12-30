# Documentator backend

# Installation

```
python -m venv venv
venv/Scripts/activate
pip install -r requirements_fixed.txt
```

# Run test server

```
uvicorn main:app --reload
```

# Run unit tests

```
pytest . -v
```

# Deploy

- Setup account on Deta
- Install tools: `iwr https://get.deta.dev/cli.ps1 -useb | iex`
- Run `deta deploy`
