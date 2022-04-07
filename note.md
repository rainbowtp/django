# notes

```bash
django-admin startproject project
python .\manage.py startapp app01

drop database django;
create database django DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'django',  # 数据库名字
          'USER': 'root',
          'PASSWORD': '',
          'HOST': '127.0.0.1',  # 那台机器安装了MySQL
          'PORT': 3306,
      }
  }


python manage.py makemigrations
python manage.py migrate

```
