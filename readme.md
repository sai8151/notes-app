## a full stack application pages(login, register, user profile, delete profile, add notes, view notes, delete notes, update notes)

```
python3 -m pip install --upgrade pip
pip install Flask
pip install mysqlclient
pip install flask_sqlalchemy

pip show werkzeug
pip install --upgrade werkzeug
pip install werkzeug==0.15.5

```

## SQL

```
CREATE TABLE note (
         id INT AUTO_INCREMENT PRIMARY KEY,
         user_id INT NOT NULL,
         content VARCHAR(200) NOT NULL,
         FOREIGN KEY (user_id) REFERENCES user(id)
     );

mysql> CREATE TABLE user (
         id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(80) UNIQUE NOT NULL,
         password VARCHAR(200) NOT NULL
     );
```