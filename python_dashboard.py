import pyodbc
import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import urllib
import seaborn as sns

load_dotenv()

print("Connecting to Azure SQL Database...")

server = os.getenv('AZURE_SERVER_NAME')
database = os.getenv('AZURE_DATABASE')
username = os.getenv('AZURE_USER')
password = os.getenv('AZURE_PASSWORD')
driver = os.getenv ('AZURE_DRIVER')

params = urllib.parse.quote_plus(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

query = "SELECT algorithm, grid_size, nodes_expanded, execution_time_us FROM PathfindingStats"
df = pd.read_sql_query(query, engine)

if df.empty:
    print("Error: No data found in Azure. Did the controller.py script finish running?")
    exit()

print("Data successfully downloaded! Rendering Seaborn graphs...")

sns.set_theme(style="darkgrid", palette="deep")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Algorithmic Pathfinding Complexity: BFS vs A* Search', fontsize=16, fontweight='bold')

sns.lineplot(data=df, x='grid_size', y='execution_time_us', hue='algorithm', marker='o', linewidth=2.5, ax=axes[0])
axes[0].set_title('Compute Cost: Execution Time vs. Grid Size', fontsize=12)
axes[0].set_xlabel('Maze Size (N x N)', fontsize=11)
axes[0].set_ylabel('Execution Time (Microseconds)', fontsize=11)

sns.lineplot(data=df, x='grid_size', y='nodes_expanded', hue='algorithm', marker='s', linewidth=2.5, ax=axes[1])
axes[1].set_title('Memory Cost: Nodes Expanded vs. Grid Size', fontsize=12)
axes[1].set_xlabel('Maze Size (N x N)', fontsize=11)
axes[1].set_ylabel('Total Nodes Checked (Lower is Better)', fontsize=11)

plt.tight_layout()
plt.show()
