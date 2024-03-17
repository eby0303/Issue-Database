import streamlit as st
import mysql.connector

# Function to connect to MySQL database
def connect_db():
    # Load MySQL connection details from secrets
    mysql_secrets = st.secrets["connections.mysql"]
    return mysql.connector.connect(
        host=mysql_secrets["host"],
        user=mysql_secrets["username"],
        password=mysql_secrets["password"],
        port=mysql_secrets["port"],
        database=mysql_secrets["database"]
    )

# Function to create new issue
def create_issue(title, description, status):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO issues (title, description, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, description, status))
    conn.commit()
    conn.close()

# Function to retrieve all issues
def get_all_issues():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM issues"
    cursor.execute(query)
    issues = cursor.fetchall()
    conn.close()
    return issues

# Main function to run the app
def main():
    # Print secrets for debugging
    st.write(st.secrets)

    st.title("Issue Tracker")

    # Sidebar to add new issue
    title = st.sidebar.text_input("Title", key="title")
    description = st.sidebar.text_area("Description", key="description")
    status = st.sidebar.selectbox("Status", ["Open", "In Progress", "Closed"], key="status")
    if st.sidebar.button("Add Issue"):
        create_issue(title, description, status)
        st.sidebar.success("Issue added successfully!")

    # Display existing issues
    issues = get_all_issues()
    if issues:
        st.write("Existing Issues:")
        for issue in issues:
            st.write(issue)
    else:
        st.write("No issues found.")

if __name__ == "__main__":
    main()
