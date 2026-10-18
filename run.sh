python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
python -m pip install -r requirements-dev.txt
python scripts/live_book.py --open-browser
