from Code import first_and_second_task

"""
User input
CHOOSE WHAT TO RETURN 
"""
# Lines to delete
# lines = ["Victoria", "Waterloo & City", "Piccadilly", "Northern", "Metropolitan", "Circle", "District", "Jubilee"]
lines = []

# Connections to delete, edges
# delete_edges_src = "Goldhawk Road"
# delete_edges_dst = "Hammersmith"
delete_edges_dst = None
delete_edges_src = None

# Delete Station
# delete_stations = ["Wood Lane", "Goldhawk Road", "South Kenton", "North Wembley", "Harrow & Wealdstone", "Stockwell"]
delete_stations = []

# Source - Destination
source = "Bank"
destination = "Kenton" 
file_name = "./Data/data_csv" # use csv 

# ! CHOOSE WHAT TO RETURN
calculate_shortest_path = False
calculate_is_path = False
show_longest_journey_time = False
graph_most_connected_station = False
graph_intersection_each_line = False    # run in "first_and_second_task.py"




"""
User output
"""
graph = first_and_second_task.Graph(file_name)
if len(lines) > 0:
    graph.deleteLines(lines)
if delete_edges_src != None and delete_edges_dst != None:
    graph.deleteEdge(delete_edges_src, delete_edges_dst)
if len(delete_stations) > 0:
    graph.deleteStation(delete_stations)
if calculate_is_path:
    path = first_and_second_task.isPath(graph.graph, source, destination)
    a = path.hasPath()
    if a != 0:
        print("It is possible to go from {} to {} in {} levels. Deleting: {}, {}, {} and {}".format(source, destination, a, delete_edges_src, delete_edges_dst, delete_stations, lines))
    else: 
        print(f"It is not possible to go from {source} to {destination}. Deleting: {delete_edges_src}, {delete_edges_dst}, {delete_stations} and {lines}")
if calculate_shortest_path:
    graph = first_and_second_task.Graph(file_name)
    shortest = first_and_second_task.ShortestPath(graph.graph, source.strip(), destination.strip())
    shortest.print_output()
if show_longest_journey_time:
    graph.longest_journey_time_between_each_station()
if graph_most_connected_station:
    graph.graph_most_connected_station()
if graph_intersection_each_line:
    graph.graph_intersection_each_line()
