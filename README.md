# GymMonk - Gym Management System

GymMonk is a web-based application designed to help gym owners and staff manage members, employees, and equipment efficiently. It provides role-based access control, secure authentication, and a clean user interface.

## Features

Role-Based Access Control: Distinct interfaces and permissions for Admins, Employees (IT, Trainer), and Members.

Secure Authentication: Uses bcrypt for password hashing and JWT (JSON Web Tokens) for session management.

Member Management: Admins and IT staff can add, view, update, and delete member information (including membership plan, join date, status). Trainers can view member details.

Employee Management: Admins can add, view, update, and delete employee records (Trainers, IT Staff).

Equipment Management: Admins and Employees can add, view, update, and delete gym equipment inventory.

Dynamic Dashboard: Frontend dashboard adapts based on the logged-in user's role.

Database Integration: Uses MySQL for persistent data storage.

Technology Stack

Backend:

Python 3.x

Flask (Web Framework)

mysql-connector-python (Database Driver)

bcrypt (Password Hashing)

PyJWT (JSON Web Tokens)

python-dotenv (Environment Variables)

Flask-Cors (Cross-Origin Resource Sharing)

Database:

MySQL

Frontend:

HTML5

CSS3 (with Tailwind CSS for styling)

JavaScript (Vanilla JS for interactivity and API calls)

Environment:

Python Virtual Environment (venv)

Project Structure

gym_monk_project/
│
├── Backend/
│   ├── main.py             # Main application entry point
│   ├── .env                # Environment variables (DB password, JWT secret)
│   ├── requirements.txt    # Python dependencies
│   ├── create_admin.py     # Script to create the first admin user
│   │
│   ├── api/                # Contains API blueprints and data models
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── member_routes.py
│   │   ├── employee_routes.py
│   │   ├── equipment_routes.py
│   │   ├── user.py         # Member class
│   │   ├── admin.py        # Admin class
│   │   ├── employee.py     # Employee class
│   │   └── equipment.py    # Equipment class
│   │
│   ├── core/
│   │   └── security.py     # Password hashing logic
│   │
│   └── database/
│       └── connection.py   # Database connection and schema setup
│
└── Frontend/
    ├── index.html          # Login page
    ├── register.html       # Member registration page
    └── dashboard.html      # Main application dashboard


Setup and Installation

Follow these steps to get GymMonk running locally:

Clone the Repository:

git clone [https://github.com/your-username/GymMonk.git](https://github.com/your-username/GymMonk.git)
cd GymMonk


Database Setup:

Ensure you have MySQL server installed and running.

Create a .env file inside the Backend directory with your MySQL password and a secret key for JWT:

MYSQL_PASSWORD=your_mysql_password
SECRET_KEY=your_strong_secret_key_here


The application will automatically create the GymDB database and tables on first run.

Backend Setup:

Navigate to the Backend directory:

cd Backend


Create and activate a Python virtual environment:

# Use 'py' on Windows if 'python' is not found
python -m venv .venv
# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1
# Activate (macOS/Linux/Git Bash)
# source .venv/bin/activate


Install the required dependencies:

pip install -r requirements.txt


Create Initial Admin User:

Run the create_admin.py script once to create your first administrator account (configure details inside the script first):

python create_admin.py


Run the Backend Server:

Start the Flask development server:

flask --app main run


The backend will be running at http://127.0.0.1:5000.

Access the Frontend:

Open the Frontend/index.html file directly in your web browser.

Log in using the admin credentials you created.

Usage

Access the application by opening Frontend/index.html.

Register as a new member using the "Sign Up" link.

Log in using the appropriate user type (Member, Employee, Admin).

Navigate the dashboard using the sidebar links based on your role.

Future Enhancements

Implement password reset functionality.

Add detailed member profile pages.

Develop workout plan features.

Implement reporting and analytics.

Add editing and deletion functionality to the dashboard views.

Containerize the application using Docker.

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
