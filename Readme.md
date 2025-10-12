python3 -m venv venv
source venv/bin/activate
cd week_1
pip freeze > requirements.txt
python3 week_1.py
streamlit run week_1.py