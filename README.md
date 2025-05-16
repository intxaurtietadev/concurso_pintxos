# Bilbao Pintxos Contest 2025

Web application to manage a pintxos contest in Bilbao, allowing users to view participating bars, pintxo categories, and vote for their favorites.

## Description

This project is a web application developed with Flask that simulates the organization of a pintxos contest. Users can browse contest information, learn about participating bars, different pintxo categories, and cast their votes. The application uses a MySQL database to store information about bars, categories, pintxos, users, and votes.

## Main Features

* Display of contest rules.
* List of participating bars with their logos and images.
* Display of awarded pintxo categories.
* Voting system for users to choose their favorite pintxos by category.
    * A user can only vote once per category.
* Simplified voter registration.
* Database management using SQLAlchemy and migrations with Flask-Migrate.
* Secure forms with Flask-WTF.
* Modular project structure using Flask Blueprints.

## Technologies Used

* **Backend**:
    * Python 3.12+
    * Flask: Web microframework.
    * SQLAlchemy: ORM for database interaction.
    * Flask-SQLAlchemy: SQLAlchemy integration with Flask.
    * Flask-WTF: WTForms integration with Flask for form management.
    * Flask-Migrate: Database migration handling with Alembic.
    * mysql-connector-python: Python driver for MySQL.
* **Database**:
    * MariaDB
* **Frontend**:
    * HTML5
    * CSS3
    * JavaScript (for basic interactivity like the image modal)
* **Web Server (for development)**:
    * Flask development server
* **Version Control**:
    * Git

## Setup and Getting Started

Follow these steps to set up and run the project in your local environment.

### Prerequisites

* Python 3.12 or higher.
* `pip` (Python package manager).
* Git.
* A MySQL database server installed and running.

### 1. Clone the Repository

```
git clone <GIT_REPOSITORY_URL>
cd concurso_pintxos
```
### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to isolate project dependencies.
```
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure the MySQL Database
Create the Database:
Make sure you have a running MySQL server. Create a database for the project (e.g., named concurso_pintxos). You can use tools like phpMyAdmin, MySQL Workbench, or the MySQL command line.

```
CREATE DATABASE concurso_pintxos CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
```
Configure the Connection:
Edit the config.py file. Modify the SQLALCHEMY_DATABASE_URI variable to point to your MySQL database.

# config.py
import os
```
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secure-and-hard-to-guess-secret-key' # CHANGE THIS!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://your_mysql_user:your_mysql_password@localhost:3306/concurso_pintxos' # ADJUST THIS
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ...
```
Important: Replace your_mysql_user and your_mysql_password with your MySQL credentials. Also, adjust localhost:3306 if your MySQL server runs on a different host or port.
For security, consider using environment variables for credentials in a production environment.

### Running the Application

Once the setup is complete and dependencies are installed:
```
flask run
```
By default, the application will run at http://127.0.0.1:5000/. Open this URL in your web browser.

If you need the application to be accessible from other devices on your local network (for testing, for example):
```
flask run --host=0.0.0.0
```

### Usage
```
Main Page (/): Displays contest information, rules, participating bars, voting form, and awards.

Voting: Users can enter their name, email, select a category, and a bar to vote.

View Votes (Debugging): Access /ver-votos to see a list of registered votes in the database (this route is primarily for debugging purposes and should be protected in a production environment).
```

### Database Structure (Main Models)

  - Rol: Defines user roles (e.g., 'Lector', 'Admin').

  - Usuario: Stores voter information (name, email, role).

  - Bar: Information about participating bars (name, address).

  - Categoria: Pintxo categories (e.g., 'Tortilla', 'Vegano').

  - Pintxo: Represents a specific pintxo offered by a bar in a category.

  - Voto: Records a vote cast by a user for a pintxo in a specific category. The main constraint is that a user can only vote once per category.

### Contributions

Contributions are welcome. Please open an issue to discuss significant changes or report bugs. If you wish to contribute code, please fork the repository and submit a pull request. Ensure your code follows the project's coding style and includes tests for new features.


### License

This project is distributed under the MIT License. See the LICENSE file for more details (if a LICENSE file is not present, assume it is a proprietary project unless otherwise stated).





