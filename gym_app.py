import streamlit as st
import mysql.connector
import pandas as pd
import sqlite3


# Function to connect to the SQLite database
def get_sqlite_connection():
    conn = sqlite3.connect('database.db')
    return conn


# Function to connect to the MySQL database
def get_mysql_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        port = '3307',
        password='Minushbest#0',
        database='gym_database'
    )
    return conn


# Function to execute a query and return a DataFrame
def run_query(conn, query, params=()):
    df = pd.read_sql_query(query, conn, params=params)
    return df


def main():
    st.title('Gym Management System')

    menu = [
        "Home",
        "View Data",
        "Add Member",
        "Update Member",
        "Book a Session",
        "View Popular Class",
        "View Receptionist Added Members",
        "Bookings and Program Details",
        "Training Programs Analysis",
        "Equipment Damage Analysis",
        "Member Payment and Damage Balances",
        "View Feedback"  # New option to view feedback
    ]
    choice = st.sidebar.selectbox("Select Option", menu)

    db_choice = st.sidebar.radio("Choose Database", ["SQLite", "MySQL"])

    if db_choice == "SQLite":
        conn = get_sqlite_connection()
    else:
        conn = get_mysql_connection()

    if choice == "Home":
        st.subheader("Welcome to the Gym Management System")

    elif choice == "View Data":
        st.subheader("View Data")
        table = st.selectbox("Select Table", ["staff", "inventory_table", "gym_equipment_table",
                                              "class_schedules", "training_programs", "members",
                                              "visitor_table", "attendance", "damage", "feedback",
                                              "booking", "payment", "class_attendance"])

        query = f"SELECT * FROM {table};"
        df = run_query(conn, query)
        st.write(df)

    elif choice == "Add Member":
        st.subheader("Add New Member")

        current_user_id = st.text_input("Enter Your ID")
        current_user_role = None

        if st.button("Check Role"):
            cursor = conn.cursor()
            query = "SELECT position FROM staff WHERE staffID = %s;"
            cursor.execute(query, (current_user_id,))
            result = cursor.fetchone()
            if result:
                current_user_role = result[0]
                st.write(f"Valid ID with role of: {current_user_role}, you can add a member!")
            else:
                st.error("User not found.")
            cursor.close()

        if current_user_role == 'Receptionist':
            memberID = st.text_input("Member ID")
            programID = st.selectbox("Select Program ID", [1, 2, 3, 4, 5])  # Ensure these are available
            last_name = st.text_input("Last Name")
            first_name = st.text_input("First Name")
            mtype_price = st.number_input("Membership Price", min_value=0.00)
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            contact_information = st.text_input("Contact Information")
            membership_type = st.text_input("Membership Type")

            if st.button("Add Member"):
                cursor = conn.cursor()
                query = """
                CALL insert_member(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                try:
                    cursor.execute(query, (
                        memberID, programID, last_name, first_name, mtype_price, start_date, end_date,
                        contact_information, membership_type, current_user_id))
                    conn.commit()
                    st.success("Member added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
                cursor.close()
        else:
            st.error("Only receptionists can add new members.")

    elif choice == "Update Member":
        st.subheader("Update Member Details")

        memberID = st.text_input("Member ID to Update")

        if memberID:
            query = f"SELECT * FROM members WHERE memberID = '{memberID}';"
            df = run_query(conn, query)
            st.write(df)

            if not df.empty:
                new_last_name = st.text_input("New Last Name", value=df.loc[0, 'last_name'])
                new_first_name = st.text_input("New First Name", value=df.loc[0, 'first_name'])
                new_mtype_price = st.number_input("New Membership Price", min_value=0.00,
                                                  value=df.loc[0, 'mtype_price'])
                new_start_date = st.date_input("New Start Date", value=pd.to_datetime(df.loc[0, 'start_date']).date())
                new_end_date = st.date_input("New End Date", value=pd.to_datetime(df.loc[0, 'end_date']).date())
                new_contact_information = st.text_input("New Contact Information",
                                                        value=df.loc[0, 'contact_information'])
                new_membership_type = st.text_input("New Membership Type", value=df.loc[0, 'membership_type'])

                if st.button("Update Member"):
                    cursor = conn.cursor()
                    query = """
                    UPDATE members
                    SET last_name = %s, first_name = %s, mtype_price = %s, start_date = %s, end_date = %s, contact_information = %s, membership_type = %s
                    WHERE memberID = %s;
                    """
                    try:
                        cursor.execute(query, (
                            new_last_name, new_first_name, new_mtype_price, new_start_date, new_end_date,
                            new_contact_information, new_membership_type, memberID))
                        conn.commit()
                        st.success("Member updated successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    cursor.close()

    elif choice == "Book a Session":
        st.subheader("Book a Session")

        memberID = st.text_input("Member ID")
        staffID = st.text_input("Staff ID")
        classID = st.text_input("Class ID")
        booking_date = st.date_input("Booking Date")
        duration = st.text_input("Duration (e.g., '1 Hour')")
        booking_time = st.time_input("Booking Time")
        booking_datetime = pd.to_datetime(f"{booking_date} {booking_time}")

        if st.button("Book Session"):
            cursor = conn.cursor()
            query = """
            INSERT INTO booking (memberID, staffID, booking_date, duration, booking_time)
            VALUES (%s, %s, %s, %s, %s);
            """
            try:
                cursor.execute(query, (memberID, staffID, booking_date, duration, booking_time))
                conn.commit()
                st.success("Session booked successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
            cursor.close()

    elif choice == "View Popular Class":
        st.subheader("Most Popular Class")

        query = """
        SELECT 
            cs.classID,
            cs.class_name,
            COUNT(ca.memberID) as total_members,
            tp.program_name,
            s.workers_name as tutor
        FROM 
            class_schedules cs
        JOIN 
            training_programs tp on cs.programID = tp.programID
        LEFT JOIN 
            class_attendance ca on cs.classID = ca.classID
        LEFT JOIN 
            staff s on cs.staffID = s.staffID
        WHERE 
            cs.classID = (
                SELECT 
                    classID
                FROM 
                    class_attendance
                GROUP BY 
                    classID
                ORDER BY 
                    COUNT(memberID) DESC
                LIMIT 1
            )
        GROUP BY 
            cs.classID, cs.class_name, tp.program_name, s.workers_name;
        """
        df = run_query(conn, query)
        st.write(df)

    elif choice == "View Receptionist Added Members":
        st.subheader("Receptionist Added Members")

        query = """
        SELECT 
            memberID,
            programID,
            last_name,
            first_name,
            mtype_price,
            start_date,
            end_date,
            contact_information,
            membership_type
        FROM members;
        """
        df = run_query(conn, query)
        st.write(df)

    elif choice == "Bookings and Program Details":
        st.subheader("Bookings and Program Details")

        query = """
        SELECT
            booking.booking_time,
            members.memberID,
            CONCAT(members.first_name, ' ', members.last_name) as Full_name,
            staff.staffID as tutorID,
            staff.workers_name as tutor_name,
            class_schedules.class_name,
            training_programs.program_name
        FROM booking
        JOIN members on booking.memberID = members.memberID
        JOIN class_schedules on booking.staffID = class_schedules.staffID
        JOIN staff on class_schedules.staffID = staff.staffID
        JOIN training_programs on class_schedules.programID = training_programs.programID;
        """
        df = run_query(conn, query)
        st.write(df)

    elif choice == "Training Programs Analysis":
        st.subheader("Training Programs Analysis")

        query = """
        SELECT 
            tp.programID,
            tp.program_name,
            COUNT(m.memberID) as total_members,
            AVG(m.mtype_price) as avg_membership_price
        FROM 
            training_programs tp
        LEFT JOIN 
            members m on tp.programID = m.programID
        GROUP BY 
            tp.programID, tp.program_name;
        """
        df = run_query(conn, query)
        st.write(df)

    elif choice == "Equipment Damage Analysis":
        st.subheader("Equipment Damage Analysis")

        query = """
        SELECT 
            ge.equipmentID,
            ge.equipment_name,
            COUNT(d.damageID) as total_damages,
            AVG(d.cost_to_repair) as avg_repair_cost
        FROM 
            gym_equipment_table ge
        LEFT JOIN 
            damage d on ge.equipmentID = d.equipmentID
        GROUP BY 
            ge.equipmentID, ge.equipment_name;
        """
        df = run_query(conn, query)
        st.write(df)

    elif choice == "Member Payment and Damage Balances":
        st.subheader("Member Payment and Damage Balances")

        query = """
        SELECT 
            m.memberID,
            CONCAT(m.first_name, ' ', m.last_name) as member_name,
            COALESCE(SUM(p.amount), 0) as total_payment,
            COALESCE(SUM(d.cost_to_repair), 0) as total_damage
        FROM 
            members m
        LEFT JOIN 
            payment p on m.memberID = p.memberID
        LEFT JOIN 
            damage d on m.memberID = d.memberID
        GROUP BY 
            m.memberID, member_name;
        """
        df = run_query(conn, query)
        st.write(df)

    elif choice == "View Feedback":
        st.subheader("View Feedback")
        query = """
        SELECT 
            f.feedback_id,
            CONCAT(m.first_name, ' ', m.last_name) as member_name,
            f.feedback_text,
            f.feedback_date
        FROM 
            feedback f
        JOIN 
            members m on f.memberID = m.memberID;
        """
        df = run_query(conn, query)
        st.write(df)

    # Close the connection
    conn.close()


if __name__ == '__main__':
    main()
