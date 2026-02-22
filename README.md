# EMart - My Django E-Commerce Project 🛒

Hey there! 👋 Welcome to **EMart**. 

I built this full-stack e-commerce website from scratch using Python and Django. This project was a massive learning experience for me, especially figuring out how to handle real-world shopping cart logic, database relationships, and connecting the backend to the frontend!

## ✨ What I Built (Features)

* **Secure User Accounts:** Customers can sign up, log in, and securely manage their sessions.
* **Live Shopping Cart:** I used JavaScript and AJAX here! When you add an item or change the quantity, the math updates instantly on the screen without having to refresh the page.
* **Checkout System:** Users can enter their shipping address, review their grand total, and successfully place an order.
* **Order Tracking:** I built a "My Orders" page where users can see their past purchases and check if their item is *Pending*, *Packed*, or *Delivered*.
* **Admin Dashboard:** Using Django's built-in admin panel, the store owner can easily add new products, update stock, and change the shipping status of customer orders.

## 🛠️ The Tech Stack

* **Backend:** Python & Django
* **Frontend:** HTML5, CSS3, and Bootstrap 5 (for a clean, responsive design)
* **Dynamic UI:** JavaScript, jQuery, and AJAX
* **Database:** SQLite

## 💻 Want to run it locally?

If you want to download my code and run the store on your own computer, just follow these steps:
**0. Install Python**
If you don't have Python installed yet, download it from [python.org](https://www.python.org/downloads/). 
*(⚠️ **Windows Users:** Make sure to check the box that says "Add Python to PATH" during the installation process!)*

**1. Clone this repository**

git clone [https://github.com/Shoye12/E-Commerce-Django-Project.git](https://github.com/Shoye12/E-Commerce-Django-Project.git)
cd E-Commerce-Django-Project
**2. Set up a virtual environment**
    
    python -m venv venv
    # Activate it:
    # Windows: venv\Scripts\activate
    # Mac/Linux: source venv/bin/activate

**3. Install Django and Pillow (Required for images)**
    
    pip install django pillow

**4. Set up the database**
    
    python manage.py makemigrations
    python manage.py migrate

**5. Create an Admin account for yourself**
    
    python manage.py createsuperuser

**6. Start the server!**
    
    python manage.py runserver
