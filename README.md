# blackjack-cbm-study
CBM study using the card game Blackjack


```sh
conda create -n blackjack-cbm-study python=3.10
conda activate blackjack-cbm-study
pip install -r requirements.txt
```


```sh
export FLASK_APP=study.py
export FLASK_ENV=development
```


```sh
flask --app app --debug run
```


```sh
flask db init
flask db migrate -m "message here"
flask db upgrade
```
