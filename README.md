FashionHub 👗✨

FashionHub is an AI-powered fashion e-commerce website designed to provide users with a personalized and convenient online shopping experience.

The platform combines fashion e-commerce functionality with an AI Fashion Assistant that helps users discover suitable products based on their preferences such as category, subcategory, color, budget, and occasion.

💻 Technologies Used
Python
Django
HTML5
CSS3
JavaScript
Bootstrap
SQLite
Font Awesome
📂 Project Structure
FashionHub/
├── accounts/
├── adminpanel/
├── ai_assistant/
├── cart/
├── checkout/
├── config/
├── contact/
├── home/
├── products/
├── static/
├── templates/
├── manage.py
└── README.md
🤖 AI Fashion Assistant

The AI Fashion Assistant uses rule-based recommendation logic to understand user preferences and provide relevant fashion products and outfit combinations.

Users can select or provide preferences such as:

Category → Subcategory → Color → Budget → Occasion → Recommendations

⚙️ Installation

Clone the repository:

git clone https://github.com/vidhi0721/FashionHub.git

Open the project folder:

cd FashionHub

Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Start the development server:

python manage.py runserver

Open the website at:

http://127.0.0.1:8000/
