. venv/bin/activate.fish
cd bot
pip install -r requirements.txt
cd ..
cd backend
pip install -r requirements.txt

# dev stuff
pip install bake-cli
pip install black