import pandas as pd
from Code import first_and_second_task

"""
The functions below create 2 new csv's with different data
"""

# get Graph class
graph = first_and_second_task.Graph()
# data with: line station 
def create_line_df():
    # create csv with only the lines
    df = pd.DataFrame(graph.get_lines())
    create_line = df.to_csv("Only_lines_csv")

# data with: line, station, destination, time
def only_stations():
    # create csv only with the data with all the information
    df = pd.DataFrame(graph.all_rows)
    create_df_stations = df.to_csv("Only_stations_csv")
    
# only_stations()