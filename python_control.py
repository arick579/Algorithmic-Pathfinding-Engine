import subprocess
import time
import sys
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv() 

server = os.getenv('AZURE_SERVER_NAME')
database = os.getenv('AZURE_DATABASE')
username = os.getenv('AZURE_USER')
password = os.getenv('AZURE_PASSWORD')
driver = os.getenv ('AZURE_DRIVER')

print("Initializing Cloud Database Connection to Microsoft Azure...")

connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'


max_retries = 3
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        conn = pyodbc.connect(connection_string, timeout=10)
        cursor = conn.cursor()
        print("Successfully connected to Azure SQL!")
        break
    except pyodbc.Error as e:
        print(f"Connection failed (Attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay}s...")
        time.sleep(retry_delay)
else:
    print("FATAL ERROR: Could not connect to database after maximum retries.")
    sys.exit(1)

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='PathfindingStats' AND xtype='U')
    CREATE TABLE PathfindingStats (
        id INT IDENTITY(1,1) PRIMARY KEY,
        algorithm VARCHAR(50),
        grid_size INT,
        path_length INT,
        nodes_expanded INT,
        execution_time_us INT
    )
''')
conn.commit()

cursor.execute('DELETE FROM PathfindingStats')
conn.commit()

print("Starting Automated C++ Benchmarks...")

grid_sizes_to_test = [10, 25, 50, 75, 100]

batch_data = [] 

for size in grid_sizes_to_test:
    print(f"Running C++ engine for Grid Size: {size}x{size}...")
    
    result = subprocess.run(['./main.exe', str(size)], capture_output=True, text=True)
    print(f"  -> C++ Output:\n{result.stdout.strip()}")
    
    output_lines = result.stdout.strip().split('\n')
    
    for line in output_lines:
        if not line:
            continue
            
        data = line.split(',')
        
        if len(data) == 5:
            algo = data[0]
            grid = int(data[1])
            path = int(data[2])
            nodes = int(data[3])
            time_us = int(data[4])
            

            batch_data.append((algo, grid, path, nodes, time_us))


if batch_data:
    print(f"\nBatch processing {len(batch_data)} records to Azure...")
    cursor.executemany('''
        INSERT INTO PathfindingStats (algorithm, grid_size, path_length, nodes_expanded, execution_time_us)
        VALUES (?, ?, ?, ?, ?)
    ''', batch_data)
    conn.commit()
    print("Data successfully committed.")

print("All benchmarks complete and data successfully pushed to Azure. Closing connection.")
