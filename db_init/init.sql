-- Drop everything for a clean reset, handling dependencies with CASCADE
DROP TABLE IF EXISTS Quotation_Items CASCADE;
DROP TABLE IF EXISTS Quotations CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TYPE IF EXISTS product_type CASCADE;
DROP TYPE IF EXISTS material CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;

-- Recreate custom ENUM types for data integrity
CREATE TYPE product_type AS ENUM ('Window', 'Door');
CREATE TYPE material AS ENUM ('uPVC', 'Aluminium', 'Timber');
CREATE TYPE user_role AS ENUM ('Manager', 'Regional Manager', 'Sales', 'Construction Worker', 'Human Resources Head', 'Human Resources Associate');

-- Recreate tables in the correct order of dependency
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL
);

CREATE TABLE Customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    address TEXT
);

CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    product_type product_type NOT NULL,
    material material NOT NULL,
    base_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE Quotations (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customers(id),
    user_id INTEGER NOT NULL REFERENCES Users(id),
    total_price NUMERIC(10, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'Draft',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Quotation_Items (
    id SERIAL PRIMARY KEY,
    quotation_id INTEGER NOT NULL REFERENCES Quotations(id),
    product_id INTEGER NOT NULL REFERENCES Products(id),
    width NUMERIC(7, 2) NOT NULL,
    height NUMERIC(7, 2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price NUMERIC(10, 2) NOT NULL
);

-- Seed the tables with rich data
-- Passwords: hr_password, manager_password, regional_password, sales_password, worker_password
INSERT INTO Users (username, hashed_password, role) VALUES
('hr_head_sandra', '$2b$12$UE6K2e.wdywgotOdR2raHO23FSpOdim994qHYRpopJyi4KPbgNJV2', 'Human Resources Head'),
('manager_jane', '$2b$12$EixZaYVK1fs7V3GvG4k.X.oZz4H.L4C/j5.jZ.6jZ.zY.Zz4H.L4C', 'Manager'),
('reg_man_bob', '$2b$12$fTj.5i.n5o.E9C6Q2b3c4u/e5s6f7g8h9i.j.k.l.m.n.o.p', 'Regional Manager'),
('sales_john', '$2b$12$fTj.5i.n5o.E9C6Q2b3c4u/e5s6f7g8h9i.j.k.l.m.n.o.p', 'Sales'),
('sales_emily', '$2b$12$fTj.5i.n5o.E9C6Q2b3c4u/e5s6f7g8h9i.j.k.l.m.n.o.p', 'Sales'),
('worker_mike', '$2b$12$fTj.5i.n5o.E9C6Q2b3c4u/e5s6f7g8h9i.j.k.l.m.n.o.p', 'Construction Worker'),
('worker_dave', '$2b$12$fTj.5i.n5o.E9C6Q2b3c4u/e5s6f7g8h9i.j.k.l.m.n.o.p', 'Construction Worker'),
('hr_assoc_linda', '$2b$12$D6U/SE8jA.R.M9x21pBdee5ddVnUBC.5eSoA3i8lQHFtC3BE2qNma', 'Human Resources Associate'),
('sales_sarah', '$2b$12$fTj.5i.n5o.E9C6Q2b3c4u/e5s6f7g8h9i.j.k.l.m.n.o.p', 'Sales'),
('manager_tom', '$2b$12$EixZaYVK1fs7V3GvG4k.X.oZz4H.L4C/j5.jZ.6jZ.zY.Zz4H.L4C', 'Manager');

INSERT INTO Customers (full_name, email, phone_number, address) VALUES
('Alice Johnson', 'alice.j@example.com', '07123456789', '123 Oak Street, Birmingham'),
('Bob Williams', 'bob.w@example.com', '07987654321', '456 Maple Avenue, Birmingham'),
('Charlie Brown', 'charlie.b@example.com', '07555123456', '789 Pine Lane, Solihull'),
('Diana Prince', 'diana.p@example.com', '07777888999', '101 Birch Road, Coventry'),
('Eve Davis', 'eve.d@example.com', '07111222333', '212 Cedar Close, Wolverhampton'),
('Frank Miller', 'frank.m@example.com', '07222333444', '333 Elm Street, Sutton Coldfield'),
('Grace Lee', 'grace.l@example.com', '07333444555', '444 Spruce Way, Dudley'),
('Harry Scott', 'harry.s@example.com', '07444555666', '555 Willow Drive, Walsall'),
('Ivy Green', 'ivy.g@example.com', '07555666777', '666 Aspen Court, West Bromwich'),
('Jack King', 'jack.k@example.com', '07666777888', '777 Redwood Place, Stourbridge');

INSERT INTO Products (name, product_type, material, base_price) VALUES
('Classic French Door', 'Door', 'uPVC', 250.00),
('Modern Sliding Patio Door', 'Door', 'Aluminium', 450.00),
('Traditional Casement Window', 'Window', 'Timber', 150.00),
('Victorian Bay Window', 'Window', 'uPVC', 180.00),
('Bi-Fold Door', 'Door', 'Aluminium', 650.00),
('Stable Door', 'Door', 'Timber', 320.00),
('Sash Window', 'Window', 'Timber', 220.00),
('Tilt and Turn Window', 'Window', 'uPVC', 160.00);

INSERT INTO Quotations (customer_id, user_id, status) VALUES
(1, 2, 'Sent'), (1, 5, 'Accepted'), (1, 9, 'Draft'), (1, 4, 'Sent'), (1, 2, 'Draft'),
(2, 4, 'Accepted'), (3, 5, 'Sent'), (4, 9, 'Draft'), (5, 2, 'Accepted'), (6, 4, 'Sent'),
(7, 5, 'Draft'), (8, 9, 'Sent'), (9, 2, 'Draft'), (10, 4, 'Accepted'), (2, 5, 'Sent');

-- Now add a rich set of quotation items (OVER 50 data points for the AI model)
INSERT INTO Quotation_Items (quotation_id, product_id, width, height, quantity, price) VALUES
-- Quote 1
(1, 3, 1.2, 1.5, 2, (150.00 * 1.2 * 1.5 * 2)), (1, 1, 0.9, 2.1, 1, (250.00 * 0.9 * 2.1 * 1)),
-- Quote 2
(2, 5, 3.0, 2.2, 1, (650.00 * 3.0 * 2.2 * 1)),
-- Quote 3
(3, 8, 0.6, 0.8, 4, (160.00 * 0.6 * 0.8 * 4)), (3, 7, 0.8, 1.4, 2, (220.00 * 0.8 * 1.4 * 2)),
-- Quote 4
(4, 4, 2.5, 1.6, 1, (180.00 * 2.5 * 1.6 * 1)),
-- Quote 5
(5, 6, 0.85, 2.0, 1, (320.00 * 0.85 * 2.0 * 1)),
-- Quote 6
(6, 2, 2.5, 2.1, 2, (450.00 * 2.5 * 2.1 * 2)), (6, 3, 0.5, 0.5, 3, (150.00 * 0.5 * 0.5 * 3)),
-- Quote 7
(7, 1, 1.8, 2.1, 1, (250.00 * 1.8 * 2.1 * 1)),
-- Quote 8
(8, 7, 0.9, 1.5, 5, (220.00 * 0.9 * 1.5 * 5)),
-- Quote 9
(9, 8, 0.7, 1.1, 10, (160.00 * 0.7 * 1.1 * 10)), (9, 4, 1.8, 1.5, 1, (180.00 * 1.8 * 1.5 * 1)),
-- Quote 10
(10, 5, 4.5, 2.4, 1, (650.00 * 4.5 * 2.4 * 1)),
-- Quote 11
(11, 6, 0.9, 2.0, 2, (320.00 * 0.9 * 2.0 * 2)),
-- Quote 12
(12, 2, 2.8, 2.2, 1, (450.00 * 2.8 * 2.2 * 1)),
-- Quote 13
(13, 3, 1.1, 1.3, 3, (150.00 * 1.1 * 1.3 * 3)), (13, 8, 0.6, 0.9, 3, (160.00 * 0.6 * 0.9 * 3)),
-- Quote 14
(14, 1, 0.95, 2.15, 1, (250.00 * 0.95 * 2.15 * 1)),
-- Quote 15
(15, 4, 2.2, 1.4, 3, (180.00 * 2.2 * 1.4 * 3)),
-- Adding more data points for better ML model training
(1, 8, 0.5, 0.7, 3, (160.00 * 0.5 * 0.7 * 3)),
(2, 7, 0.7, 1.2, 2, (220.00 * 0.7 * 1.2 * 2)),
(3, 2, 2.0, 2.0, 1, (450.00 * 2.0 * 2.0 * 1)),
(4, 1, 1.0, 2.2, 1, (250.00 * 1.0 * 2.2 * 1)),
(5, 5, 2.8, 2.1, 1, (650.00 * 2.8 * 2.1 * 1)),
(6, 6, 0.9, 1.9, 2, (320.00 * 0.9 * 1.9 * 2)),
(7, 4, 1.5, 1.0, 4, (180.00 * 1.5 * 1.0 * 4)),
(8, 3, 0.8, 1.0, 6, (150.00 * 0.8 * 1.0 * 6)),
(9, 1, 0.8, 2.0, 2, (250.00 * 0.8 * 2.0 * 2)),
(10, 7, 1.0, 1.6, 3, (220.00 * 1.0 * 1.6 * 3)),
(11, 8, 0.6, 1.0, 5, (160.00 * 0.6 * 1.0 * 5)),
(12, 5, 3.5, 2.3, 1, (650.00 * 3.5 * 2.3 * 1)),
(13, 4, 2.0, 1.3, 2, (180.00 * 2.0 * 1.3 * 2)),
(14, 2, 2.4, 2.1, 1, (450.00 * 2.4 * 2.1 * 1)),
(15, 3, 0.9, 0.9, 4, (150.00 * 0.9 * 0.9 * 4)),
(1, 2, 1.8, 2.0, 1, (450.00 * 1.8 * 2.0 * 1)),
(2, 4, 2.1, 1.5, 1, (180.00 * 2.1 * 1.5 * 1)),
(3, 5, 3.2, 2.2, 1, (650.00 * 3.2 * 2.2 * 1)),
(4, 7, 0.8, 1.3, 2, (220.00 * 0.8 * 1.3 * 2)),
(5, 8, 0.7, 0.9, 3, (160.00 * 0.7 * 0.9 * 3)),
(6, 1, 0.9, 2.0, 1, (250.00 * 0.9 * 2.0 * 1)),
(7, 3, 1.5, 1.2, 2, (150.00 * 1.5 * 1.2 * 2)),
(8, 6, 0.8, 1.9, 1, (320.00 * 0.8 * 1.9 * 1)),
(9, 2, 2.2, 2.1, 1, (450.00 * 2.2 * 2.1 * 1)),
(10, 4, 1.9, 1.4, 1, (180.00 * 1.9 * 1.4 * 1)),
(11, 5, 2.9, 2.3, 1, (650.00 * 2.9 * 2.3 * 1)),
(12, 7, 0.75, 1.25, 3, (220.00 * 0.75 * 1.25 * 3)),
(13, 8, 0.55, 0.85, 4, (160.00 * 0.55 * 0.85 * 4)),
(14, 1, 0.85, 2.05, 1, (250.00 * 0.85 * 2.05 * 1)),
(15, 6, 0.95, 1.95, 1, (320.00 * 0.95 * 1.95 * 1));

-- Finally, update the total_price in the Quotations table based on the sum of its items.
UPDATE Quotations q SET total_price = (SELECT SUM(price) FROM Quotation_Items qi WHERE qi.quotation_id = q.id);

