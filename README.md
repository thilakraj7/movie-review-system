# DataVista - DBMS project

![DBMS Project](https://img.shields.io/badge/DBMS-Streamlit%20App-blue.svg)

## 📌 Overview
This project is a **Database Management System (DBMS) application** built using **Streamlit** for an interactive web-based interface. It provides a user-friendly platform for managing, querying, and visualizing data stored in a relational database.

## 🚀 Features
- **CRUD Operations**: Perform Create, Read, Update, and Delete operations.
- **User Authentication**: Secure login and access control.
- **Data Visualization**: Interactive charts and graphs.
- **SQL Query Execution**: Run custom SQL queries.
- **Streamlit-Based UI**: Lightweight and easy-to-use web app.
- **Scalability**: Supports multiple database backends (MySQL, PostgreSQL, SQLite).

## 🏗️ Project Structure
```
DBMS_project--streamlit/
│── app/                    # Streamlit application files
│── database/               # Database connection and queries
│── static/                 # CSS and JavaScript files
│── templates/              # HTML templates
│── main.py                 # Entry point for the Streamlit app
│── requirements.txt        # Dependencies list
│── README.md               # Project documentation
```

## 🔧 Requirements
- **Python 3.x**
- **Streamlit**
- **MySQL/PostgreSQL/SQLite**
- **SQLAlchemy**
- **Pandas & Matplotlib**

## 📖 Installation & Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/adityagirishh/DBMS_project--streamlit.git
   cd DBMS_project--streamlit
   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Database**
   - Update `database/config.py` with your database credentials.
   - Run migrations (if applicable).
5. **Run the Application**
   ```bash
   streamlit run main.py
   ```

## 📊 Usage
- Navigate to the web UI.
- Use the interactive dashboard to manage and query the database.
- Visualize data through graphs and tables.
- Perform CRUD operations via the app interface.

## 🚀 Future Enhancements
- Implement Role-Based Access Control (RBAC).
- Support NoSQL databases (MongoDB, Firebase).
- Add API endpoints for integration with other apps.

## 📝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments
- Open-source contributors
- Streamlit & SQLAlchemy communities
- Database design best practices

---
📧 For queries, contact: thilakraj67411@gmail.com

