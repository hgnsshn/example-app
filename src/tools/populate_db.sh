#!/usr/bin/env sh

cd $(git rev-parse --show-toplevel)/src/user
. venv/bin/activate
python populate_fake_users.py
cd $(git rev-parse --show-toplevel)/src/product
. venv/bin/activate
python populate_fake_products.py
cd $(git rev-parse --show-toplevel)/src/order
. venv/bin/activate
python populate_fake_orders.py

