import mysql.connector
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# CSV file path
csv_path = r"C:\Users\ashna\Desktop\Python_shine_dezign\Merge_data_from_mysql_csv\dataset.csv"

# Function to fetch DB data and merge
def merge_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="studentdb"
        )

        query = "SELECT * FROM students"
        db_data = pd.read_sql_query(query, conn)
        conn.close()

        csv_data = pd.read_csv(csv_path)

        merged_data = pd.merge(db_data, csv_data, on="id")

        print("\nUpdated merged data:")
        print(merged_data)

    except Exception as e:
        print("Error:", e)


# Event handler for file changes
class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("dataset.csv"):
            print("\nCSV file changed. Merging data...")
            merge_data()


if __name__ == "__main__":

    print("Real-time merge system started. Modify CSV or DB and see updates.")

    event_handler = CSVHandler()
    observer = Observer()

    observer.schedule(event_handler, path=csv_path.rsplit("\\",1)[0], recursive=False)
    observer.start()

    # Initial merge
    merge_data()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    
# import mysql.connector
# import pandas as pd

# # Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="studentdb"
# )

# # Fetch data from database
# query = "SELECT * FROM students"
# db_data = pd.read_sql(query, conn)

# print("Database Data:")
# print(db_data)

# # Load CSV dataset
# csv_data = pd.read_csv("C:\\Users\\ashna\\Desktop\\Python_shine_dezign\\Merge_data_from_mysql_csv\\dataset.csv")

# print("\nCSV Data:")
# print(csv_data)

# # Merge both datasets
# merged_data = pd.merge(db_data, csv_data, on="id")

# print("\nMerged Data:")
# print(merged_data)

# conn.close()

# import mysql.connector
# import pandas as pd

# # Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="studentdb"
# )

# cursor = conn.cursor()

# # Read CSV file
# csv_data = pd.read_csv("C:\\Users\\ashna\\Desktop\\Python_shine_dezign\\Merge_data_from_mysql_csv\\dataset.csv")

# # Fetch database data
# cursor.execute("SELECT * FROM students")

# result = []

# for row in cursor.fetchall():
#     id_db = row[0]
#     name = row[1]
#     marks = row[2]

#     # Find matching row in CSV
#     match = csv_data[csv_data["id"] == id_db]

#     if not match.empty:
#         city = match.iloc[0]["city"]
#         department = match.iloc[0]["department"]

#         # Store only merged result
#         result.append((id_db, name, marks, city, department))

# # Print final result
# for r in result:
#     print(r)

# conn.close()

# import mysql.connector
# import pandas as pd
# import time
# import os

# def get_merged_data():
#     try:
#         # 1. Connect to MySQL
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="1234",
#             database="studentdb"
#         )

#         # 2. Fetch fresh DB data
#         query = "SELECT * FROM students"
#         db_data = pd.read_sql(query, conn)
#         conn.close()

#         # 3. Load fresh CSV data
#         csv_path = r"C:\Users\ashna\Desktop\Python_shine_dezign\Merge_data_from_mysql_csv\dataset.csv"
#         csv_data = pd.read_csv(csv_path)

#         # 4. Merge
#         merged_data = pd.merge(db_data, csv_data, on="id")
        
#         return merged_data

#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# # The Continuous Loop
# print("Starting real-time monitoring... Press Ctrl+C to stop.")

# while True:
#     os.system('cls' if os.name == 'nt' else 'clear') # Clears console for a clean view
    
#     current_data = get_merged_data()
    
#     if current_data is not None:
#         print(f"--- Last Updated: {time.strftime('%H:%M:%S')} ---")
#         print(current_data)
    
#     # Wait for 5 seconds before checking again
#     time.sleep(5)

