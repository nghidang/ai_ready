python3 -m venv venv
source venv/bin/activate
cd week_1
pip freeze > requirements.txt
pip install -r requirements.txt
streamlit run week_1.py
python3 main.py
python3 -m unittest test_office_assistant.py -v