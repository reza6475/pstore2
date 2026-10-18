# PStore2 — Django Online Shop
# PStore2 — Django Online Shop

A Django-based online shopping application built with JavaScript, HTML, CSS, and SQLite.

The project implements a complete shopping workflow, including product browsing, a browser-based shopping cart, user authentication, order creation, inventory validation, payment status management, and Django Admin customization.

## Features

- **Product management:** Store product information, prices, stock quantities, descriptions, and images.
- **Shopping cart:** Manage cart data in the browser using `localStorage`.
- **Checkout:** Submit cart contents to Django for server-side validation and order creation.
- **Inventory validation:** Validate product availability and stock quantities before creating an order.
- **Order management:** Store orders and their associated order items in the database.
- **User accounts:** Support user registration, login, and logout.
- **Payment workflow:** Create payment records and manage payment statuses. Payment processing is simulated; no real payment gateway is integrated.
- **Django Admin:** Manage application data through the administrative interface, including order-related customizations.
- **User feedback:** Display application messages and relevant validation errors.
- **Environment configuration:** Load sensitive settings and environment-specific values from a `.env` file.
- **Static and media files:** Separate application static assets from uploaded product images.

## Technology Stack

- Python
- Django
- JavaScript
- HTML5
- CSS3
- SQLite
- Pillow
- python-dotenv
- django-jalali-suite

Exact dependency versions are listed in `requirements.txt`.

## Project Structure

```text
pstore2/
├── config/
│   └── settings.py
├── store/
│   ├── tests.py
│   └── ...
├── media/
│   └── products/
├── static/
├── templates/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

The structure above is a high-level overview. Some application files and directories may differ in the current repository.

## Requirements

- Python compatible with the versions specified by the project's dependencies
- pip
- Git (optional, for cloning the repository)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/reza6475/pstore2.git
cd pstore2
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root, next to `manage.py`, using `.env.example` as a reference.

Set the following variables:

```dotenv
DJANGO_SECRET_KEY=your-own-random-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate a unique secret key for your environment. Do not use the example placeholder as the actual secret key, and never commit the real `.env` file.

### 5. Apply database migrations

```powershell
python manage.py migrate
```

### 6. Create an administrator account

```powershell
python manage.py createsuperuser
```

Follow the prompts to create the account.

### 7. Start the development server

```powershell
python manage.py runserver
```

Open the local development address shown in the terminal, usually:

http://127.0.0.1:8000/

## Environment Variables

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | Enables or disables debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of allowed host names |

These values are loaded from the local `.env` file by Django settings.

## Database

The project currently uses SQLite. Database migrations are managed through Django's migration system.

To apply migrations:

```powershell
python manage.py migrate
```

## Running Tests

Run the project's automated tests with:

```powershell
python manage.py test
```

The test suite includes checkout and cart API scenarios, such as successful order creation, stock validation, invalid input, and unsupported HTTP methods.

## Static and Media Files

- `static/` contains application static assets, such as CSS and JavaScript.
- `media/products/` contains uploaded product images.
- `STATIC_ROOT` defines the destination for collected static files when preparing for deployment.
- `MEDIA_ROOT` defines the location of uploaded media files.

For deployment preparation, Django provides the following command:

```powershell
python manage.py collectstatic
```

This command is not required for ordinary local development.

## Security Notes

- Keep `.env` and other secret-bearing files out of version control.
- Use a unique, randomly generated `DJANGO_SECRET_KEY` for each environment.
- Set `DJANGO_DEBUG=False` and configure appropriate allowed hosts before production deployment.
- Configure HTTPS, secure cookies, and a production email backend before deployment.
- Validate important checkout data on the server rather than trusting browser-submitted values.

## Project Status

This project is being developed as a portfolio-quality Django online shop.

The core shopping workflow, account functionality, order management, simulated payment workflow, and administrative features have been implemented. Testing and deployment preparation are ongoing.

A real payment gateway and production deployment are not currently included.

## License

No license has been specified yet. All rights reserved unless a license is added to the repository.
