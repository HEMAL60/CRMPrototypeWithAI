-- Drop everything for a clean reset, handling dependencies with CASCADE
DROP TABLE IF EXISTS Quotation_Items CASCADE;
DROP TABLE IF EXISTS Quotations CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TYPE IF EXISTS product_type CASCADE;
DROP TYPE IF EXISTS material CASCADE;
DROP TYPE IF EXISTS user_role CASCADE;

-- Recreate custom ENUM types with expanded roles
CREATE TYPE product_type AS ENUM ('Window', 'Door');
CREATE TYPE material AS ENUM ('uPVC', 'Aluminium', 'Timber');
CREATE TYPE user_role AS ENUM ('Manager', 'Regional Manager', 'Sales', 'Construction Worker', 'Human Resources Head', 'Human Resources Associate');

-- Recreate tables
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
    total_price NUMERIC(10, 2), -- Will be updated after items are added
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

-- Seed the Users table (10 users)
INSERT INTO Users (id, username, hashed_password, role) VALUES
(1, 'manager_jane', '$2b$12$D6U/SE8jA.R.M9x21pBdee5ddVnUBC.5eSoA3i8lQHFtC3BE2qNma', 'Manager'),
(2, 'sales_john', '$2b$12$u/v.f2A4Y4gX0.d/u.i/h.OCZ.Q9B.T8c.Z/W.E/S.T/U.V/W', 'Sales'),
(3, 'hr_head_sandra', '$2b$12$UE6K2e.wdywgotOdR2raHO23FSpOdim994qHYRpopJyi4KPbgNJV2', 'Human Resources Head'), -- pw: 'hr_password'
(4, 'reg_man_mike', '$2b$12$a1B2c3D4e5F6g7H8i9J0k.O/P/Q/R/S/T/U/V/W/X/Y/Z', 'Regional Manager'),
(5, 'sales_sue', '$2b$12$b1C2d3E4f5G6h7I8j9K0l.P/Q/R/S/T/U/V/W/X/Y/Z/a', 'Sales'),
(6, 'worker_will', '$2b$12$c1D2e3F4g5H6i7J8k9L0m.Q/R/S/T/U/V/W/X/Y/Z/a/b', 'Construction Worker'),
(7, 'hr_assoc_harry', '$2b$12$d1E2f3G4h5I6j7K8l9M0n.R/S/T/U/V/W/X/Y/Z/a/b/c', 'Human Resources Associate'),
(8, 'worker_wendy', '$2b$12$e1F2g3H4i5J6k7L8m9N0o.S/T/U/V/W/X/Y/Z/a/b/c/d', 'Construction Worker'),
(9, 'sales_sam', '$2b$12$f1G2h3I4j5K6l7M8n9O0p.T/U/V/W/X/Y/Z/a/b/c/d/e', 'Sales'),
(10, 'manager_mark', '$2b$12$g1H2i3J4k5L6m7N8o9P0q.U/V/W/X/Y/Z/a/b/c/d/e/f', 'Manager')
ON CONFLICT (id) DO NOTHING;

-- Seed the Customers table (10 customers)
INSERT INTO Customers (id, full_name, email, phone_number, address) VALUES
(1, 'Alice Johnson', 'alice.j@example.com', '07123456789', '123 Oak Street, Birmingham'),
(2, 'Bob Williams', 'bob.w@example.com', '07987654321', '456 Maple Avenue, Birmingham'),
(3, 'Charlie Brown', 'charlie.b@example.com', '07555123456', '789 Pine Lane, Solihull'),
(4, 'Diana Prince', 'diana.p@example.com', '07777888999', '101 Birch Close, Coventry'),
(5, 'Edward Scissorhands', 'edward.s@example.com', '07111222333', '202 Elm Drive, Wolverhampton'),
(6, 'Fiona Glenanne', 'fiona.g@example.com', '07333444555', '303 Cedar Road, Dudley'),
(7, 'George Costanza', 'george.c@example.com', '07999888777', '404 Sycamore Place, Walsall'),
(8, 'Harleen Quinzel', 'harley.q@example.com', '07888777666', '505 Willow Way, Sutton Coldfield'),
(9, 'Indiana Jones', 'indy.j@example.com', '07666555444', '606 Redwood Grove, Tamworth'),
(10, 'Jack Sparrow', 'jack.s@example.com', '07444333222', '707 Aspen Court, Redditch')
ON CONFLICT (id) DO NOTHING;

-- Seed the Products table (10 products)
INSERT INTO Products (id, name, product_type, material, base_price) VALUES
(1, 'Classic French Door', 'Door', 'uPVC', 250.00),
(2, 'Modern Sliding Patio Door', 'Door', 'Aluminium', 450.00),
(3, 'Traditional Casement Window', 'Window', 'Timber', 150.00),
(4, 'Victorian Bay Window', 'Window', 'uPVC', 220.00),
(5, 'Stable Door', 'Door', 'Timber', 350.00),
(6, 'Aluminium Bi-Fold Door', 'Door', 'Aluminium', 650.00),
(7, 'Sash Window', 'Window', 'Timber', 180.00),
(8, 'Tilt and Turn Window', 'Window', 'uPVC', 160.00),
(9, 'Composite Front Door', 'Door', 'uPVC', 400.00),
(10, 'Minimalist Aluminium Window', 'Window', 'Aluminium', 300.00)
ON CONFLICT (id) DO NOTHING;

-- Seed the Quotations table (10 quotations), ensuring customer 1 has 5 entries
INSERT INTO Quotations (id, customer_id, user_id, status) VALUES
(1, 1, 2, 'Sent'), (2, 1, 5, 'Accepted'), (3, 1, 9, 'Draft'), (4, 1, 1, 'Sent'), (5, 1, 2, 'Accepted'),
(6, 2, 2, 'Accepted'), (7, 3, 1, 'Draft'), (8, 4, 5, 'Sent'), (9, 5, 9, 'Draft'), (10, 7, 5, 'Draft')
ON CONFLICT (id) DO NOTHING;

-- Seed the Quotation_Items table (15 items, ensuring all quotations have at least one)
-- price = base_price * width * height
INSERT INTO Quotation_Items (quotation_id, product_id, width, height, quantity, price) VALUES
-- Items for Quotation 1 (Customer 1)
(1, 3, 1.2, 1.5, 2, 540.00), -- 2x Casement Window (150 * 1.2 * 1.5 * 2)
(1, 1, 0.9, 2.1, 1, 472.50), -- 1x French Door (250 * 0.9 * 2.1)
-- Items for Quotation 2 (Customer 1)
(2, 6, 3.0, 2.2, 1, 4290.00), -- 1x Bi-Fold Door (650 * 3.0 * 2.2)
-- Items for Quotation 3 (Customer 1)
(3, 8, 0.6, 0.9, 3, 259.20), -- 3x Tilt and Turn (160 * 0.6 * 0.9 * 3)
-- Items for Quotation 4 (Customer 1)
(4, 4, 2.5, 1.6, 1, 880.00), -- 1x Bay Window (220 * 2.5 * 1.6)
(4, 7, 0.8, 1.4, 2, 403.20), -- 2x Sash Window (180 * 0.8 * 1.4 * 2)
-- Items for Quotation 5 (Customer 1)
(5, 10, 1.8, 1.0, 4, 2160.00), -- 4x Aluminium Window (300 * 1.8 * 1.0 * 4)
-- Items for Quotation 6
(6, 2, 2.5, 2.1, 1, 2362.50), -- 1x Sliding Door (450 * 2.5 * 2.1)
-- Items for Quotation 7
(7, 5, 1.0, 2.0, 1, 700.00), -- 1x Stable Door (350 * 1.0 * 2.0)
-- Items for Quotation 8
(8, 9, 0.9, 2.0, 1, 720.00), -- 1x Composite Door (400 * 0.9 * 2.0)
(8, 3, 1.0, 1.2, 2, 360.00), -- 2x Casement Window (150 * 1.0 * 1.2 * 2)
-- Items for Quotation 9
(9, 7, 0.7, 1.3, 5, 819.00), -- 5x Sash Window (180 * 0.7 * 1.3 * 5)
-- Items for Quotation 10
(10, 1, 0.8, 2.0, 1, 400.00); -- 1x French Door (250 * 0.8 * 2.0)

-- UPDATE the total_price in the Quotations table based on the sum of its items
UPDATE Quotations q SET total_price = (SELECT SUM(price) FROM Quotation_Items qi WHERE qi.quotation_id = q.id);

