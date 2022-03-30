# Travel In Good Health Management System

## Installation 

```bash
pip install -r requirements.txt
```

## Usage

```bash
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

## Testing

```bash 
python3 manage.py test -v 3 --testrunner auto_test.HtmlTestReporter
```

#### The report gets saved in a folder named reports