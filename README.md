# NotesApp

A simple note-taking application built to practice frontend design and working with SQLAlchemy models and Flask routing.

### Features

- User authentication (signup, login)
- Note creation and management
- LLM integration via Ollama
- Responsive frontend with HTML/CSS/JS

## Requirements
Apart from the requirements that will be listed in the requirements.txt, there are a couple of things to install before launching the app:
One major requirement is `Ollama` installed and launched on your device, as we're also using a local LLM in the application.

Install and run Ollama from [ollama.com](https://ollama.com)

After having installed Ollama, the model that the application uses is `'smollm2:1.7b'`, you can install it by doing:
```
ollama pull smollm2:1.7b
```
It's a lightweight model by `HuggingFace`, so it should work on almost any device.
If, in any case, you would like to use a different model instead, you can find it in `src/app/website/routes/agent.py` and just change the `Jarvis` model.

## Installation
Before getting started, make sure to have an active `virtualenv`:
```
python3 -m venv env
source env/bin/activate
```

The installation process is quite easy:

1. Clone the repository and cd into it:
```
git clone https://github.com/marcoslashpro/notes-app && cd notes-app
```
2. Install the local package:
```
pip install -e .
```
3. Install the requirements:
```
pip install -r requirements.txt
```
Then simply launch the app by doing:
```
launch
```
If that, for any reason, failes, then try:
```
python3 -m src.app.run
```
