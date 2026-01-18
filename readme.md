# Smile Score & Demo Wallet Project

A **Django-based project** that allows users to upload a face image, predicts a **smile score** (0-100) using a CNN model, and shows a **demo Ethereum wallet** using Ganache test network.

This project is meant as a **demo to showcase skills** in Python, Django, ML, and blockchain integration. No real money is used.

---

## Features

1. **Face Smile Score**
   - Users can upload an image.
   - The model predicts a score from 0 to 100.
   - If the score >= 80, a demo ETH reward is sent to the user’s demo wallet.

2. **Demo Ethereum Wallet**
   - Wallet created for each user.
   - Shows balance and reward transaction history.
   - Uses **Ganache local blockchain** (fake ETH).
   - Demo purposes only; not for real transactions.

3. **Email OTP Login**
   - Users log in via email OTP (no password required).
   - Realistic OTP email sent via console (for development).

4. **Leaderboard**
   - Shows top scores.
   - Users can compete in score ranking.

---

## Requirements

- Python 3.13+
- Django 6.0
- TensorFlow / Keras
- Web3.py
- Ganache (for local blockchain demo)

---

## Setup Instructions

1. **Clone the repo**
```bash
git clone <repo-url>
cd project-folder

 **Install dependencies**
```bash
pip install -r requirements.txt

python -m venv env
env\Scripts\activate   # Windows
source env/bin/activate # Mac/Linux

DJANGO_SECRET_KEY=your_django_secret_key
GANACHE_URL=http://127.0.0.1:7545
Migrate database

python manage.py migrate
Run server

python manage.py runserver
![Alt text for the GIF]PROJECT.gif)
