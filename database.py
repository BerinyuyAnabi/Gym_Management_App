import sqlite3
def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Drop existing tables if they exist

    # Create tables
    c.execute('''
    DROP DATABASE IF EXISTS gym_database;
    CREATE DATABASE gym_database;

        -- Use the new database
        USE gym_database;

        CREATE TABLE staff (
            staffID TEXT PRIMARY KEY,
            income REAL NOT NULL CHECK (income >= 0),
            position TEXT NOT NULL,
            hire_date TEXT NOT NULL,
            workers_name TEXT NOT NULL,
            contact_information TEXT NOT NULL UNIQUE,
            employment TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE inventory_table (
            inventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            status TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            purchase_date TEXT NOT NULL,
            UNIQUE (item_name, purchase_date)
        )
    ''')

    c.execute('''
        CREATE TABLE gym_equipment_table (
            inventoryID INTEGER,
            status TEXT NOT NULL,
            last_maintenance_date TEXT NOT NULL,
            FOREIGN KEY (inventoryID) REFERENCES inventory_table(inventoryID) ON DELETE CASCADE ON UPDATE CASCADE,
            CHECK (last_maintenance_date >= '2024-01-01')
        )
    ''')

    c.execute('''
        CREATE TABLE class_schedules (
            classID TEXT PRIMARY KEY,
            staffID TEXT,
            programID INTEGER,
            class_name TEXT NOT NULL,
            day_of_week TEXT NOT NULL CHECK (day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (staffID) REFERENCES staff(staffID) ON DELETE SET NULL ON UPDATE CASCADE
        )
    ''')

    c.execute('''
        CREATE TABLE training_programs (
            programID INTEGER PRIMARY KEY AUTOINCREMENT,
            classID TEXT,
            program_name TEXT NOT NULL,
            duration TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (classID) REFERENCES class_schedules(classID) ON DELETE SET NULL ON UPDATE CASCADE
        )
    ''')

    c.execute('''
        CREATE TABLE members (
            memberID TEXT PRIMARY KEY,
            programID INTEGER,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            mtype_price REAL NOT NULL CHECK (mtype_price >= 0),
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            contact_information TEXT NOT NULL UNIQUE,
            membership_type TEXT NOT NULL,
            FOREIGN KEY (programID) REFERENCES training_programs(programID) ON DELETE SET NULL ON UPDATE CASCADE
        )
    ''')

    c.execute('''
        CREATE TABLE visitor_table (
            visitorID TEXT PRIMARY KEY,
            visitor_name TEXT NOT NULL,
            purpose_of_visit TEXT NOT NULL,
            contact_information TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE attendance (
            attendanceID INTEGER PRIMARY KEY AUTOINCREMENT,
            personID TEXT NOT NULL,
            person_type TEXT NOT NULL CHECK (person_type IN ('member', 'staff', 'visitor')),
            arrival_time TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE damage (
            damageID INTEGER PRIMARY KEY AUTOINCREMENT,
            personID TEXT NOT NULL,
            person_type TEXT NOT NULL CHECK (person_type IN ('member', 'staff', 'visitor')),
            inventoryID INTEGER,
            damage_type TEXT NOT NULL,
            cost REAL NOT NULL CHECK (cost >= 0),
            damage_date TEXT NOT NULL,
            FOREIGN KEY (inventoryID) REFERENCES inventory_table(inventoryID) ON DELETE SET NULL ON UPDATE CASCADE
        )
    ''')

    c.execute('''
        CREATE TABLE feedback (
            feedbackID INTEGER PRIMARY KEY AUTOINCREMENT,
            personID TEXT NOT NULL,
            person_type TEXT NOT NULL CHECK (person_type IN ('member', 'staff', 'visitor')),
            feedback TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE booking (
            bookingID INTEGER PRIMARY KEY AUTOINCREMENT,
            memberID TEXT NOT NULL,
            staffID TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            duration TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            FOREIGN KEY (memberID) REFERENCES members(memberID) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (staffID) REFERENCES staff(staffID) ON DELETE CASCADE ON UPDATE CASCADE,
            UNIQUE (memberID, staffID, booking_date, booking_time)
        )
    ''')

    c.execute('''
        CREATE TABLE payment (
            paymentID INTEGER PRIMARY KEY AUTOINCREMENT,
            person_ID TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount >= 0),
            payment_date TEXT NOT NULL,
            reason_for_payment TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE class_attendance (
            class_attendanceID INTEGER PRIMARY KEY AUTOINCREMENT,
            memberID TEXT,
            classID TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            FOREIGN KEY (memberID) REFERENCES members(memberID) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (classID) REFERENCES class_schedules(classID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    # Insert sample data into the tables
    c.execute('''
        INSERT INTO staff (staffID, income, position, hire_date, workers_name, contact_information, employment) VALUES
        ('ST001', 1500.00, 'Fitness Trainer', '2023-01-15', 'Kwame Mensah', 'kwame.mensah@example.com', 'Full-Time'),
        ('ST002', 1200.00, 'Receptionist', '2023-03-10', 'Akosua Aidoo', 'akosua.aidoo@example.com', 'Part-Time'),
        ('ST003', 1700.00, 'Gym Manager', '2022-06-05', 'Abena Owusu', 'abena.owusu@example.com', 'Full-Time'),
        ('ST004', 1300.00, 'Personal Trainer', '2024-04-20', 'Kofi Boateng', 'kofi.boateng@example.com', 'Full-Time'),
        ('ST005', 1100.00, 'Cleaner', '2024-05-15', 'Gifty Asante', 'gifty.asante@example.com', 'Part-Time'),
        ('ST006', 500.00, 'Maintainer', '2024-06-15', 'Precious Asante', 'precious.asante@example.com', 'Full-Time'),
        ('ST007', 800.00, 'Cook', '2024-05-15', 'Mary Yeboah', 'mary.yeboah@example.com', 'Part-Time'),
        ('ST008', 500.00, 'Maintainer', '2024-07-15', 'Fabiola Akwelle', 'fabiola.akwelle@example.com', 'Full-Time')
    ''')

    c.execute('''
        INSERT INTO inventory_table (item_name, status, quantity, purchase_date) VALUES
        ('Treadmill', 'Good', 5, '2024-02-10'),
        ('Dumbbells', 'Need Repair', 20, '2024-01-20'),
        ('Yoga Mats', 'Need Repair', 15, '2024-03-12'),
        ('Resistance Bands', 'Good', 30, '2024-04-01'),
        ('Exercise Bikes', 'Good', 10, '2024-05-20')
    ''')

    c.execute('''
        INSERT INTO gym_equipment_table (inventoryID, status, last_maintenance_date) VALUES
        (1, 'Good', '2024-06-15'),
        (2, 'Good', '2024-07-20'),
        (3, 'Need Repair', '2024-04-01'),
        (4, 'Good', '2024-05-01'),
        (5, 'Good', '2024-06-01')
    ''')

    c.execute('''
        INSERT INTO class_schedules (classID, staffID, programID, class_name, day_of_week, start_time, end_time) VALUES
        ('CL001', 'ST001', 1, 'Morning Yoga', 'Monday', '07:00:00', '08:00:00'),
        ('CL002', 'ST002', 2, 'Advanced Weight Training', 'Wednesday', '17:00:00', '18:30:00'),
        ('CL003', 'ST003', 3, 'Evening Cardio', 'Friday', '18:00:00', '19:00:00'),
        ('CL004', 'ST001', 4, 'Aerobics', 'Tuesday', '08:00:00', '09:00:00'),
        ('CL005', 'ST002', 5, 'HIIT', 'Thursday', '06:00:00', '07:00:00')
    ''')

    c.execute('''
        INSERT INTO training_programs (classID, program_name, duration, description) VALUES
        ('CL001', 'Morning Yoga', '1 hour', 'A relaxing start to your day with morning yoga.'),
        ('CL002', 'Advanced Weight Training', '1.5 hours', 'Push your limits with advanced weight training.'),
        ('CL003', 'Evening Cardio', '1 hour', 'Get your heart pumping with evening cardio.'),
        ('CL004', 'Aerobics', '1 hour', 'High-energy aerobics session to keep you fit.'),
        ('CL005', 'HIIT', '1 hour', 'High-intensity interval training for quick results.')
    ''')

    c.execute('''
        INSERT INTO members (memberID, programID, last_name, first_name, mtype_price, start_date, end_date, contact_information, membership_type) VALUES
        ('MB001', 1, 'Doe', 'John', 100.00, '2024-01-01', '2024-12-31', 'john.doe@example.com', 'Annual'),
        ('MB002', 2, 'Smith', 'Jane', 50.00, '2024-02-01', '2024-07-31', 'jane.smith@example.com', 'Semi-Annual'),
        ('MB003', 3, 'Brown', 'Charlie', 30.00, '2024-03-01', '2024-05-31', 'charlie.brown@example.com', 'Quarterly'),
        ('MB004', 4, 'Wilson', 'Anna', 10.00, '2024-04-01', '2024-04-30', 'anna.wilson@example.com', 'Monthly')
    ''')

    c.execute('''
        INSERT INTO visitor_table (visitorID, visitor_name, purpose_of_visit, contact_information) VALUES
        ('VS001', 'Mark Thompson', 'Tour', 'mark.thompson@example.com'),
        ('VS002', 'Emily Clark', 'Workshop', 'emily.clark@example.com')
    ''')

    c.execute('''
        INSERT INTO attendance (personID, person_type, arrival_time, departure_time, date) VALUES
        ('MB001', 'member', '07:00:00', '08:00:00', '2024-01-15'),
        ('ST001', 'staff', '08:00:00', '17:00:00', '2024-01-15'),
        ('VS001', 'visitor', '09:00:00', '10:00:00', '2024-01-15')
    ''')

    c.execute('''
        INSERT INTO damage (personID, person_type, inventoryID, damage_type, cost, damage_date) VALUES
        ('MB002', 'member', 2, 'Broken', 20.00, '2024-02-15')
    ''')

    c.execute('''
        INSERT INTO feedback (personID, person_type, feedback, date) VALUES
        ('MB001', 'member', 'Great facility!', '2024-01-16'),
        ('ST001', 'staff', 'Need more equipment.', '2024-01-17'),
        ('VS001', 'visitor', 'Enjoyed the tour.', '2024-01-18')
    ''')

    c.execute('''
        INSERT INTO booking (memberID, staffID, booking_date, duration, booking_time) VALUES
        ('MB001', 'ST001', '2024-01-20', '1 hour', '10:00:00'),
        ('MB002', 'ST002', '2024-01-21', '1.5 hours', '11:00:00')
    ''')

    c.execute('''
        INSERT INTO payment (person_ID, amount, payment_date, reason_for_payment) VALUES
        ('MB001', 100.00, '2024-01-01', 'Membership Fee'),
        ('MB002', 50.00, '2024-02-01', 'Membership Fee')
    ''')

    c.execute('''
        INSERT INTO class_attendance (memberID, classID, attendance_date) VALUES
        ('MB001', 'CL001', '2024-01-15'),
        ('MB002', 'CL002', '2024-02-15')
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
