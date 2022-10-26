# API for website Hype and Play

- Download and installing python from this website [link](https://www.python.org/downloads/)

- Create virtual environtment
    ```
    python -m venv env
    ```
    After create virtual environtment activate it in the directory of it with

    for Windows :
        ```
        env\Script\activate
        ```

    for Linux :
        ```
        source env/bin/activate
        ```

- Install dependencies that needed

    ```
    pip install -r requirement.txt
    ```

- Migration for database that needed for API

    ```
    manage.py makemigrations
    manage.py migrate
    ```

- Create Super Admin

    ```
    manage.py createsuperuser
    ```


- Activate Server

    ```
    manage.py runserver
    ```