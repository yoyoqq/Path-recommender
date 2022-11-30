import pandas as pd
import collections
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from heapq import *
from collections import deque

"""
! Run the code with the MAIN function (Go to the last lines to run the code)
"""

class Graph():
    
    def __init__(self, file_name = "./Data/data_csv") -> None:
        """
        Instance variables
        """
        # :rtype pandas row data
        self.all_rows = self.read_csv_ReturnAllNodes(file_name)
        # :rtype graph with all edges
        self.graph = self.graph_all_data() 
        # :rtype pandas rows
        self.nodes = self.get_nodes()   
        self.lines = self.get_lines()

    def read_csv_ReturnAllNodes(self, name: str) -> list[list]:
        """
        Process data from excel or csv and return Pandas dataframe rows.
        Get data from the CSV 
        """
        # convert from excel to csv
        # excel_file = pd.read_excel(name)
        # excel_file.to_csv("data_csv",  index=False)
        colnames = ["Line", "Source", "Destination", "Time"]
        csv_df = pd.read_csv(name, names=colnames, header= 0)
        # clean data to get only the rows with the time
        csv_df_clean = csv_df.dropna().drop_duplicates()
        # csv_df.reset_index(drop = True, inplace = True)
        csv_df_clean.reset_index(drop = True, inplace = True)
        return csv_df_clean
    
    def graph_all_data(self) -> dict:
        """
        Returns an undirected graph
        """
        graph = defaultdict()
        for line, source, destination, time in self.all_rows.values: 
            if source not in graph: graph[source] = []
            if destination not in graph: graph[destination] = []
            graph[source].append((destination, time, line)) 
            graph[destination].append((source, time, line))
        return graph

    # Delete connections between stations
    def deleteEdge(self, src: str, dst: str) -> None:
        """
        Delete edges between the nodes
        """
        out = self.all_rows[(self.all_rows["Source"]== src) & (self.all_rows["Destination"].isin([src, dst]))]
        self.all_rows.drop(index=out.index, inplace=True)
        self.update_constants()

    def deleteLines(self, lines: list[str]) -> None:
        """
        Delete all the stations that have the same line
        """
        for i in lines:
            self.all_rows.drop(self.all_rows.loc[self.all_rows["Line"] == i].index, inplace= True)
        self.all_rows.reset_index(drop = True, inplace = True)
        self.update_constants()

    def deleteStation(self, stations: list[str]) -> None:
        """
        Delete all the stations that are in the list
        """
        for i in stations:
            self.all_rows.drop(self.all_rows.loc[self.all_rows["Source"] == i].index, inplace= True)
            self.all_rows.drop(self.all_rows.loc[self.all_rows["Destination"] == i].index, inplace= True)
        self.all_rows.reset_index(drop = True, inplace = True)
        # update graph
        self.update_constants()

    def update_constants(self) -> None:
        """
        updates the constants
        """
        self.graph = self.graph_all_data()
        self.nodes = self.get_nodes()
        self.lines = self.get_lines()
        
    def get_nodes(self) -> list[list]:
        """
        returns all the nodes of the graph
        """
        source = self.all_rows["Source"].dropna().drop_duplicates()
        source.reset_index(drop = True, inplace = True)
        return source
    
    def get_lines(self) -> list[list]:
        """
        Return line names of all the graph
        """
        source = self.all_rows["Line"].dropna().drop_duplicates()
        source.reset_index(drop = True, inplace = True)
        return source
        
    def count_node_occurrences(self) -> list:
        """
        Get the number of occurrences of each station
        """
        d = defaultdict()
        source_destination = self.all_rows[["Source", "Destination"]].dropna().drop_duplicates()
        source_destination.reset_index(drop = True, inplace = True)
        # print(source_destination.values)
        for i, j in source_destination.values:
            # if value == 0, typo or ERROR in the input/output
            d.setdefault(i, 0)
            d.setdefault(j, 0)
            d[i] += 1
            d[j] += 1
        s_list = [[k, v] for k, v in sorted(d.items(), key=lambda item: item[1])]
        return s_list
    
    def get_line(self, line) -> list[list]:
        """
        return the stations that the line has
        """
        x_line = self.all_rows[self.all_rows["Line"] == line]
        x_line.reset_index(drop=True, inplace = True)
        return x_line

    def get_graph(self, x_y: dict, title: str, xlabel: str, ylabel: str) -> plt:
        """
        Get graph with the parameters
        """
        x = []
        y = []
        for i, j in x_y:
            x.append(i)
            y.append(j)
        plt.rcParams.update({'figure.autolayout': True})
        fig, ax = plt.subplots()
        ax.barh(x, y)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')
        plt.title(title)
        plt.xlabel(xlabel, fontsize = "20")
        plt.ylabel(ylabel, fontsize = "20")
        plt.show()
    
    def stations_set(self) -> set:
        """
        Get all the stations names in a set of the current rows
        """
        source = self.all_rows[["Source", "Destination"]].dropna().drop_duplicates()
        source.reset_index(drop = True, inplace = True)
        temp = set()
        for s, d in source.values:
            temp.add(s)
            temp.add(d)
        return temp
        
    def lines_intersection(self):
        """
        Get the intersection of each line
        """
        lines = list(self.lines)
        intersections = []

        # get all the stations in x one by one 
        # put in y, the values that are not in x
        x = []
        y = []
        for i in range(len(lines)):
            temp = []
            for j in range(len(lines)):
                if i == j: continue
                
                temp.append(lines[j])
            x.append(lines[i])
            y.append(temp)
            temp = []

        # For each value in x and y map the values and get the intersection of the stations
        for i in range(len(lines)):
            g1 = Graph(file_name)
            # rest data
            g2 = Graph(file_name)

            c1 = x[i]
            g1.deleteLines(c1)
            s1 = g1.stations_set()
            # print(g1.all_rows)

            c2 = y[i]
            g2.deleteLines(c2)
            s2 = g2.stations_set()
            # print(len(s2))

            # for bakerloo it has 25 intersections, it can be connected to other lines in 25 stations
            # print(len(s1 and s2))
            intersections.append(len(s1 and s2))
        
        return [i for i in zip(x, intersections)]

    def longest_journey_time_between_each_station(self):
        """
        Get chart with the longest time between all the stations
        """
        line_name = ["Bakerloo", "Central", "Circle", "District", "Hammersmith & City", "Jubilee", "Metropolitan", "Northern", "Piccadilly", "Victoria", "Waterloo & City"]
        line_time = [44, 83, 17, 77, 48, 46, 68, 62, 77, 36, 5]

        plt.rcParams.update({'figure.autolayout': True})

        fig, ax = plt.subplots()
        ax.barh(line_name, line_time)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=45, horizontalalignment='right')
        plt.title("Longest journey time for each line")
        plt.xlabel("Minutes", fontsize = "20")
        plt.ylabel("Stations", fontsize = "20")
        plt.show()
    
    def graph_most_connected_station(self):
        """
        Get most connected station
        """
        # print(graph.count_node_occurrences())
        most_connected_lines_to_show = 30
        max_occurrences = self.count_node_occurrences()
        # print(max_occurrences)    # :rtype, get a list[list] of the most connected components
        max_occurrences = max_occurrences[len(max_occurrences)-most_connected_lines_to_show: len(max_occurrences)]
        # print(max_occurrences)
        # get graph of occurrences
        self.get_graph(max_occurrences, "Most connected station", "Occurrences", "Line")
        
    def graph_intersection_each_line(self):
        """
        Get graph of the intersection
        """
        a = self.lines_intersection()
        a = sorted(a, key= lambda x: x[1])
        self.get_graph(a, "Intersection of each line", "Intersections", "Lines")
        
                
class ShortestPath():
    def __init__(self, edges, src, dst) -> None:
        self.edges = edges
        self.src = src
        self.dst = dst

    def dijkstra(self) -> tuple:
        """
        q: values to iterate
        seen: checked values
        mins: minimum values
        """
        q, seen, mins = [(0, self.src, [], [], [])], set(), {self.src: 0}
        while q:
            # pop the min value of the heap
            (cost, v1, path, lines, times) = heappop(q)
            # if the station haven't been seen
            if v1 not in seen:
                seen.add(v1)
                path = [v1] + path
                # if we have found the path return
                if v1 == self.dst:
                    return (cost, path, lines, times)
                # put the station edges to a dict 
                for v2, c, line in self.edges[v1]:
                    if v2 in seen:
                        continue
                    prev = mins.get(v2, None)
                    next = cost + c
                    if prev is None or next < prev:
                        mins[v2] = next
                        # append to heap
                        heappush(q, (next, v2, path, lines + [line] , times + [c]))
        return (float("inf"), [])

    def print_output(self):
        """
        Process the raw data of the Dijkstra algorithm
        Get the rows in pandas
        """
        try:
            out = self.dijkstra()
            out[1].reverse()
            time, source, line, times = out
            line = line + ["h"]
            source_pairs = source[0: len(source) - 1]
            destination_pairs = []
            for i in range(1, len(source)):
                destination_pairs.append(source[i])
            # get data of the Dijkstra output in pandas rows
            detailed_df = pd.DataFrame(list(zip(line , source_pairs, destination_pairs, times)), columns=["Line", "Source", "Destination", "Times"])
            # output 
            print(detailed_df)
            print("Total time will be: {} minutes starting from {} to {}.".format(time, self.src, self.dst))
        except:
            return print("Invalid input")
            
            
class isPath(ShortestPath):

    def __init__(self, edges, src, dst) -> None:
        super().__init__(edges, src, dst)

    # check if there is a path between the nodes, BFS
    def hasPath(self) -> int:
        visited = set()
        # node, level
        queue = deque([[self.src, 0]])

        # If value not in dict return error
        try:
            while queue:
                v, count = queue.popleft()
                # if possible 
                if v == self.dst:
                    return count
                # for all its edges
                for neighbor, time, line in self.edges[v]:
                    if neighbor not in visited:
                        queue.append([neighbor, count + 1])
                        visited.add(neighbor)
            return 0
        except: return 0
                        
                      

if __name__ == "__main__":

    """
    User input
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
    delete_stations = ["Kenton", "South Kenton", "North Wembley"]

    # Source - Destination
    source = "Bank"
    destination = "Kenton" 
    file_name = "./Data/data_csv" # use csv 
    
    # Choose: Shortest path or calculate if there is path, if True, it will run 
    calculate_shortest_path = True
    calculate_is_path = False
    show_longest_journey_time = False
    graph_most_connected_station = False
    graph_intersection_each_line = False
    
    
    """
    User output
    """
    graph = Graph(file_name)
    if len(lines) > 0:
        graph.deleteLines(lines)
    if delete_edges_src != None and delete_edges_dst != None:
        graph.deleteEdge(delete_edges_src, delete_edges_dst)
    if len(delete_stations) > 0:
        graph.deleteStation(delete_stations)
    if calculate_is_path:
        path = isPath(graph.graph, source, destination)
        a = path.hasPath()
        if a != 0:
            print("It is possible to go from {} to {} in {} levels. Deleting: {}, {}, {} and {}".format(source, destination, a, delete_edges_src, delete_edges_dst, delete_stations, lines))
        else: 
            print(f"It is not possible to go from {source} to {destination}. Deleting: {delete_edges_src}, {delete_edges_dst}, {delete_stations} and {lines}")
    if calculate_shortest_path:
        graph = Graph(file_name)
        shortest = ShortestPath(graph.graph, source.strip(), destination.strip())
        shortest.print_output()
    if show_longest_journey_time:
        graph.longest_journey_time_between_each_station()
    if graph_most_connected_station:
        graph.graph_most_connected_station()
    if graph_intersection_each_line:
        graph.graph_intersection_each_line()

    
    print(graph.graph)

