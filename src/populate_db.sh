#!/usr/bin/env sh

cd user
. venv/bin/activate
python populate_fake_users.py
cd ../product
. venv/bin/activate
python populate_fake_products.py
cd ../order
. venv/bin/activate
python populate_fake_orders.py

