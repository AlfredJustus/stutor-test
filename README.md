# Stutor Platform Test

Stutor is a platform that connects tutors and students from the same school. 

This repository features a primitive version of stutor.de, 
designed to help you understand the workings of
Django and the basic structure of the project.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.12.6** - If not installed:
   - Visit [Python's official website](https://www.python.org/downloads/)
   - Download Python 3.12.6 for macOS
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening Terminal and typing: `python3 --version`

2. **MySQL** - If not installed:
   - Visit [MySQL's official website](https://dev.mysql.com/downloads/mysql/)
   - Download MySQL Community Server for macOS
   - Follow the installation wizard
   - Remember the root password you set during installation

## Getting the Project

### Option 1: Download ZIP (Easiest)
1. Go to the GitHub repository in your web browser (also possible in terminal though)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your computer
5. Open Terminal and navigate to the extracted folder

### Option 2: Using Git (For developers)
You won't need to edit anything in this file so let's not overcomplicate for now.

## Project Setup Instructions

### 1. Set Up Python Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Verify you're in the virtual environment (you should see (venv) in your terminal)
# Install required packages
pip install -r requirements.txt
```

### 2. Configure Secret Key
The project comes with a development secret key. For security reasons, you should generate your own secret key:

1. Open a Python shell:
```bash
python manage.py shell
```

2. Generate a new secret key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

3. Copy the generated key and replace the `SECRET_KEY` value in `project/project/settings.py`

### 3. Database Setup
1. Start MySQL if it's not running:
   ```bash
   # On macOS, you can start MySQL from System Preferences
   # Or use the command line:
   mysql.server start
   ```

2. Create the database and user:
   ```bash
   # Log into MySQL
   mysql -u root -p
   
   # In MySQL prompt, run:
   CREATE DATABASE primitive;
   CREATE USER 'stutor'@'localhost' IDENTIFIED BY '1234';
   GRANT ALL PRIVILEGES ON primitive.* TO 'stutor'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. Create and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
# Follow the prompts to create your admin account
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

The application should now be running at `http://127.0.0.1:8000/`. To add tutors to the database and make them visible, head to `http://127.0.0.1:8000/admin` and log in with your superuser details. Once you filled out a tutor profile, click 'verified' to make them appear on the website. 


## Important Notes
- Make sure you're using Python 3.12.6
- Keep your secret key secure and never commit it to version control
- The project uses MySQL as the database backend
- Email functionality requires proper SMTP configuration in settings.py

## Need Help?
Ask chatgpt or claude
