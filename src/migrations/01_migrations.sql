\c exampleapp;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL
);
GRANT ALL ON users TO exampleuser;
GRANT USAGE, SELECT ON users_id_seq TO exampleuser;

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
);
GRANT ALL ON products TO exampleuser;
GRANT USAGE, SELECT ON products_id_seq TO exampleuser;

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
GRANT ALL ON orders TO exampleuser;
GRANT USAGE, SELECT ON orders_id_seq TO exampleuser;
