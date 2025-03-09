# Cafe Reviews Web Application

## Overview
This is a **Flask-based web application** that allows users to browse, review, and request the addition of cafes in the city. Admins can add, edit, or delete cafes. Users can submit requests to add cafes, which will be emailed to the admin for approval.

### 🌐 Live Demo
The application is deployed and available at: **[Cafe Club](https://cafeclub.onrender.com)**

## Features
- **User Authentication:** Users can register, log in, and log out.
- **Browse Cafes:** View a list of cafes with details such as name, location, coffee price, and rating.
- **Review Cafes:** Users can leave a review and the system will calculate the average rating.
- **Admin Controls:** Admins can add, edit, or delete cafes.
- **User Cafe Requests:** Normal users can request to add a cafe, which is sent to the admin via email.
- **Search Functionality:** Users can search for cafes by name.
- **Deployment Ready:** Works on platforms like **Render** with Gunicorn support.

## Technologies Used
- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS (Bootstrap 5)
- **Email Integration:** SMTP (for cafe addition requests)
- **Deployment:** Gunicorn, Render

## Installation & Setup
### **1. Clone the Repository:**

   git clone https://github.com/vihansr/Cafe-Club.git
   cd cafe-reviews

### **2. Create a Virtual Environment (Optional but Recommended):**

   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

### **3. Install Dependencies:**

   pip install -r requirements.txt

### **4. Set Up the Database:**

   python -c 'from main import db; db.create_all()'

### **5. Run the Application Locally:**

   python main.py
   

## Environment Variables
Create a `.env` file (or `data.env` if specified) and add:
```
SECRET_KEY=your_secret_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

## Routes
| Route | Method | Description |
|--------|--------|-----------------|
| `/` | GET | Homepage listing all cafes |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/add` | GET, POST | Admin adds a cafe |
| `/edit/<cafe_id>` | GET, POST | Admin edits a cafe |
| `/delete/<cafe_id>` | POST | Admin deletes a cafe |
| `/review/<cafe_id>` | GET, POST | User reviews a cafe |
| `/user_add` | GET, POST | User requests to add a cafe (emails admin) |

## Contribution
If you’d like to contribute, feel free to fork the repo and submit a pull request!

Developed with ❤️ using Flask & Bootstrap 🚀

