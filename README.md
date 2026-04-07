# GymMonk - Integrated Gym Management System

GymMonk is a full-stack gym management solution featuring a Flask-based REST API, a secure MySQL database backend, and a dynamic, role-based dashboard frontend.

## 🚀 Key Features

* **Role-Based Access Control:** Distinct interfaces and permissions for Admins, Employees, and Members.
* **Member Management:** Full CRUD operations for tracking memberships, contact info, and status.
* **Inventory Tracking:** Manage gym equipment, quantities, and unit pricing.
* **Security:** Password hashing using Bcrypt and stateless authentication via JWT (JSON Web Tokens).
* **Automated Database Setup:** Self-initializing MySQL schema on first run.

## 🛠️ Technology Stack

### Backend
* **Python 3.x**: Core programming language.
* **Flask**: Micro web framework for the REST API.
* **mysql-connector-python**: Database driver for MySQL connectivity.
* **bcrypt**: Library for secure password hashing.
* **PyJWT**: Implementation of JSON Web Tokens for authentication.
* **python-dotenv**: For managing environment variables securely.
* **Flask-Cors**: Handling Cross-Origin Resource Sharing.

### Database
* **MySQL**: Relational database management system.

### Frontend
* **HTML5 / CSS3**: Styled using **Tailwind CSS**.
* **JavaScript (Vanilla JS)**: ES6+ for interactivity and API integration.

## 📁 Project Structure

```text
gym_monk_project/
├── Backend/
│   ├── api/                    # API Blueprints & Data Models
│   │   ├── __init__.py
│   │   ├── admin.py            # Admin logic & authentication
│   │   ├── auth_routes.py      # Registration & Login endpoints
│   │   ├── employee.py         # Employee class logic
│   │   ├── employee_routes.py  # Employee management endpoints
│   │   ├── equipment.py        # Equipment class logic
│   │   ├── equipment_routes.py # Equipment management endpoints
│   │   ├── member_routes.py    # Member management endpoints
│   │   └── user.py             # Member class logic
│   ├── core/
│   │   └── security.py         # Password hashing & JWT helper functions
│   ├── database/
│   │   └── connection.py       # MySQL connection & Schema initialization
│   ├── .env                    # Secret keys and DB credentials
│   ├── create_admin.py         # Script to generate initial admin account
│   ├── main.py                 # Application entry point
│   └── requirements.txt        # Project dependencies
└── Frontend/
    ├── dashboard.html          # Dynamic user dashboard
    ├── index.html              # Main login page
    └── register.html           # Public member signup page
```
## ⚙️ Installation & Setup
**1. Database Configuration**

Ensure MySQL is running and create a `.env` file in the `Backend/` directory:

``` bash
MYSQL_PASSWORD=your_password
SECRET_KEY=your_jwt_secret_key
```

**2. Running the Backend**
You must navigate into the `Backend` folder to run the server:

```bash 
# Move into the directory
cd Backend

# Activate virtual environment (Windows PowerShell)
& ./.venv/Scripts/Activate.ps1

# Start the application
python main.py
```

**3. Frontend Access**
Once the backend logs `Successfully connected to the GymDB database`, open `Frontend/index.html` in your browser.

Developed as a comprehensive management solution for modern fitness centers.

```bash
You can copy and paste this directly into your `README.md` file in your root directory. This version matches the exact project structure and tech stack we have been working on together.
```