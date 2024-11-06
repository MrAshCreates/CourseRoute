# CourseRoute
CourseRoute is cross-platform desktop app built with Python and PyQt, automating high school scheduling using Smart algorithms. It integrates with PowerSchool and Schoology, leveraging PostgreSQL and SQLAlchemy for data management, ensuring seamless data handling.

## Features

- **Automated Scheduling**: Generates optimal schedules using Integer Linear Programming and Genetic Algorithms.
- **Cross-Platform**: Runs on Windows, macOS, and Linux.
- **User-Friendly Interface**: Built with Qt and PyQt for a responsive GUI.
- **Database Integration**: Utilizes PostgreSQL with SQLAlchemy for data persistence.
- **Educational Platform Support**: Integrates with PowerSchool and Schoology for data import/export.
- **Customizable Requirements**: Allows selection of state and county-specific graduation requirements.

## Requirements

- **Python 3.8 or higher**
- **PostgreSQL 12 or higher**
- **Qt 5 or higher**
- **Required Python Packages** (see `requirements.txt`):
  - PyQt5
  - SQLAlchemy
  - Psycopg2
  - PuLP
  - numpy
  - pandas
  - requests (for API calls)
  - PowerSchool and Schoology API clients (if available)

## Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/MrAshCreates/EduScheduler.git
cd EduScheduler

2. Set Up a Virtual Environment

python3 -m venv venv
source venv/bin/activate

3. Install Python Dependencies

pip install -r requirements.txt

4. Set Up PostgreSQL Database

	•	Install PostgreSQL if not already installed:

brew install postgresql


	•	Start PostgreSQL service:

brew services start postgresql


	•	Create a new database user and database:

createuser eduscheduler_user --pwprompt
createdb eduscheduler_db -O eduscheduler_user


	•	Update config.ini with your database credentials.

5. Configure the Application

	•	Rename config.example.ini to config.ini:

cp config.example.ini config.ini


	•	Edit config.ini to add your database credentials and API keys for PowerSchool and Schoology.

6. Run the Application

python main.py

Usage

	1.	Launch the Application:

python main.py


	2.	Set Up Graduation Requirements:
	•	Select your state and county to load local graduation requirements.
	3.	Import or Enter Data:
	•	Students: Import from PowerSchool/Schoology or enter manually.
	•	Courses: Define available courses and their details.
	•	Teachers: Input teacher information and availability.
	4.	Generate Schedules:
	•	Run the scheduling algorithm to generate student schedules.
	•	Review and adjust as necessary.
	5.	Export Schedules:
	•	Export finalized schedules back to PowerSchool/Schoology or as reports.

Contributing

Contributions are welcome! Please follow these steps:

	1.	Fork the repository.
	2.	Create a new branch: git checkout -b feature/your-feature-name.
	3.	Commit your changes: git commit -m 'Add some feature'.
	4.	Push to the branch: git push origin feature/your-feature-name.
	5.	Open a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

	•	Qt and PyQt for the GUI framework.
	•	PuLP and NumPy for optimization and mathematical computations.
	•	SQLAlchemy for ORM and database management.
	•	PowerSchool and Schoology for providing APIs to integrate educational data.

Contact

For any inquiries or support, please contact professional@asherwinstead.dev
