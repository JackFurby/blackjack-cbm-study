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

```sh
flask --app app --debug run
```


Deploying the application

It is assumed you have a server setup. We used Ubuntu 22.04

connect to server: `ssh -i ./blackjack-study.key ubuntu@131.251.172.55`

1. Update server and install software

  ```sh
  suso apt-get update
  sudo apt-get upgrade
  sudo apt install gunicorn libsm6 libxext6 libgl1 ffmpeg libxrender-dev python3-pymysql python3-pip
  ```

2. Clone repository to your server

  ```sh
  git clone https://github.com/JackFurby/blackjack-cbm-study.git
  cd blackjack-cbm-study
  ```

3. Install pip packages

  ```sh
  pip3 install -r requirements.txt
  pip3 install pymysql
  ```
4. Set environmental variables

  ```sh
  nano ~/.bashrc
  ```

  add `export DATABASE_URL='mysql+pymysql://<USER_NAME>:<PASSWORD>@<DB_URL>:3306/<DB_NAME>'` to the end of the file.

  ```sh
  source ~/.bash_profile
  ```

5. Start app

  *Note: this should be started such that it will run when you exit the terminal e.g. with tmux*

  gunicorn -b 0.0.0.0:8080 study:app
