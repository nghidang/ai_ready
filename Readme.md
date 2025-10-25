python3 -m venv venv
source venv/bin/activate
cd week_2
pip freeze > requirements.txt
streamlit run week_1.py
python3 main.py
python3 -m unittest test_office_assistant.py -v