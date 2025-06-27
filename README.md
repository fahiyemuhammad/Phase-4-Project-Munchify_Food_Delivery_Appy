# 🍔 Munchify - Food Delivery App

**Munchify** is a full-stack food delivery web application built with **React** (frontend) and **Flask + PostgreSQL** (backend). It allows users to sign up, browse food items, add to cart, place orders, and track their order history. Admin users can manage menu items as well.

---

## Features

### 👨‍🍳 For Users

- Sign up and log in with JWT authentication
- Browse available food items with images and descriptions
- Add items to cart and calculate totals
- Place orders with full delivery info
- Receive order confirmation email via Flask-Mail
- View order history (with order totals and delivery info)

### 🔐 For Admin (Optional Future Feature)

- Add, update, or delete menu items
- View all orders from all users

---

## 🛠️ Tech Stack

### Frontend

- React (with React Router & Context API)
- SweetAlert2 for alerts
- CSS for styling

### Backend

- Flask
- Flask SQLAlchemy (ORM)
- Flask-JWT-Extended (authentication)
- PostgreSQL (database)
- Flask-Mail (email confirmations)
- Marshmallow (optional for validation/serialization)

---

## 📁 Project Structure

project-root/
│
├── frontend/
│ └── src/
│ ├── components/
│ ├── context/StoreContext.js
│ ├── pages/PlaceOrder.js
│ └── ...
│
├── server/
│ ├── models/
│ ├── routes/orders.py
│ ├── routes/auth.py
│ ├── extensions.py
│ ├── app.py
│ └── config.py
│
└── README.md

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 📌 Requirements

- Node.js (v16+)
- Python 3.10+
- PostgreSQL
- Pipenv or virtualenv

---

### 🔧 Backend Setup (Flask + PostgreSQL)

1. **Clone the repo** and navigate to the backend folder:

   ```bash
   git clone https://github.com/your-username/munchify.git
   cd munchify/server
   Create a virtual environment and install dependencies:
   ```

bash
Copy
Edit
pipenv install
pipenv shell
Set environment variables (or create a .env file):

ini
Copy
Edit
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/munchify_db
SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True
Initialize the database:

bash
Copy
Edit
flask db init
flask db migrate
flask db upgrade
Seed sample menu items (optional)

bash
Copy
Edit
flask seed
Run the server:

bash
Copy
Edit
flask run
🌐 Frontend Setup (React)
In another terminal, navigate to the frontend/ folder:

bash
Copy
Edit
cd munchify/frontend
Install dependencies:

bash
Copy
Edit
npm install
Start the React app:

bash
Copy
Edit
npm start
The app will open at http://localhost:3000

🔐 Authentication Flow
JWT tokens are stored in localStorage.

Protected routes require a valid token (e.g., placing orders, viewing history).

Token is attached in headers via:

js
Copy
Edit
Authorization: `Bearer ${token}`
📦 API Endpoints (Sample)
POST /auth/register
Registers a new user

POST /auth/login
Logs in and returns JWT

POST /orders
Creates an order (token required)

GET /orders
Returns user's order history (token required)

📧 Email Confirmation
When an order is placed, the user receives an email like:

vbnet
Copy
Edit
Subject: Your Order Confirmation

Hi Fahiye,

Your order was successfully placed!
You'll pay $32.00 on delivery.

Thanks for shopping with us!
💡 Future Improvements
Admin dashboard for managing items

Mobile responsive design

Real-time order tracking

Stripe or M-Pesa integration

Order status updates (preparing, out for delivery, delivered)

📷 Demo
Include screenshots or GIFs showing:

Landing page

Cart and checkout

Order success

Order history page

🙌 Author
Fahiye Muhammad
Front-End & Back-End Developer
LinkedIn | GitHub
