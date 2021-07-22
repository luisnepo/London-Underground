import openpyxl
import tkinter.messagebox as tm
import collections
from collections import namedtuple, deque


#creates all the lists.
b = []
time_next_station = []
total_time_list = []
route_line = []
route_lines = []
display_route = []
end_data = []
lines = []
stations = []
total_data = []

#clears the stored variables when the program starts so data doesnt overlap when starting the program after doing a search(instead of pressing the new trip button).
b.clear()
time_next_station.clear()
total_time_list.clear()
route_line.clear()
route_lines.clear()
display_route.clear()
end_data.clear()
lines.clear()
stations.clear()
total_data.clear()

#opens the excel file and activates the book so it can be accesed later on.
book = openpyxl.load_workbook('London Underground data.xlsx')
sheet = book.active
#creates the node compartment
class Node(object):
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev
#creates the doublelinkedlists that will later on be used to add items and itteraction thought the lists.
class DLL(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
    
    def append_item(self, data):
        new_item = Node(data, None, None)
        if self.head is None:
            self.head = new_item
            self.tail = self.head
        else:
            new_item.prev = self.tail
            self.tail.next = new_item
            self.tail = new_item
    
        self.count += 1
    
    def iter(self):
        current = self.head
        while current:
            item_val = current.data
            current = current.next
            yield item_val

total_data = DLL()

#itterates through the data in the excel and stores it so it can later on be used with the dijsktra data. 
for row in sheet.iter_rows(min_row=1, min_col=1, max_row=800, max_col=4):
    
    stations_row = []
    
    for cell in row:
        stations_row.append(cell.value)
    
    if stations_row[2] != None:
        stations.append(stations_row)
        total_data.append_item(stations_row)

    
        reversed_stations_row = stations_row[:]
        element0 = reversed_stations_row[1]
        reversed_stations_row[1] = reversed_stations_row[2]
        reversed_stations_row[2] = element0
    
        stations.append(reversed_stations_row)
        total_data.append_item(reversed_stations_row)

#when the search button is pressed,runs the dijkstra algorithm and a try statment that collects the data.If the user enters a station that doesnt appear on the excel it will promp a error.(Caps lock sensitive and space sensitive).
def searchButton_pressed(self, controller):
    global b, time_next_station, total_time_list, display_route, route_line, route_lines, end_data
    
    journeyStartTxt = getattr(self,"entry_journeyStart")
    journeyStart = journeyStartTxt.get()
    
    journeyEndTxt = getattr(self,"entry_journeyEnd")
    journeyEnd = journeyEndTxt.get()
    
    #dijsktra algorithm taken from https://rosettacode.org/wiki/Dijkstra%27s_algorithm#Python
    inf = float('inf')
    Edge = namedtuple('Edge', ['line','start', 'end', 'cost'])
    
    class Graph():
        def __init__(self, edges):
            self.edges = [Edge(*edge) for edge in edges]
            self.vertices = {e.start for e in self.edges} | {e.end for e in self.edges}
    
        def dijkstra(self, source, dest):
            assert source in self.vertices
            dist = {vertex: inf for vertex in self.vertices}
            previous = {vertex: None for vertex in self.vertices}
            dist[source] = 0
            q = self.vertices.copy()
            neighbours = {vertex: set() for vertex in self.vertices}
            for line,start, end, cost in self.edges:
                neighbours[start].add((end, cost))

            while q:
                u = min(q, key=lambda vertex: dist[vertex])
                q.remove(u)
                if dist[u] == inf or u == dest:
                    break
                for v, cost in neighbours[u]:
                    alt = dist[u] + cost
                    if alt < dist[v]:
                        dist[v] = alt
                        previous[v] = u
            s, u = deque(), dest
            while previous[u]:
                s.appendleft(u)
                u = previous[u]
            s.appendleft(u)
            return s
            
    
    graph = Graph(total_data.iter())
    
    try:
        d = collections.deque(graph.dijkstra(journeyStart, journeyEnd))
        if d == None:
            pass
    
        while True:
            try:
                
                b.append(d.popleft())
            except IndexError:
                break
        
            
        for i in range(len(b)):
            prev_station = ""
            for row in stations:
                if i < len(b) - 1:
                    if b[i] == row[1] and b[i + 1] == row[2] and row[1] is not prev_station:
                        route_line = [row[0], row[1], row[2], row[3]]
                        route_lines.append(route_line)
                        prev_station = row[1]
        
    
        total_time = 5
    
        for line in route_lines:
            for i in range(len(b) - 1):
                for j in range(1, len(b)):
                    if b[i] == line[1] and b[j] == line[2]:
                        total_time = total_time + int(line[3] + 1)
                        total_time_list.append(total_time)
    
        for i in route_lines:
            display_route.append(i[0:4])    

        
        b.reverse()
        display_route.reverse()
        total_time_list.reverse()
        controller.show_frame("nextFrame")
        
        
    #error if the name user provided doesnt match the data    
    except:
        tm.showerror("Error reading data", """Note:The program is sensitive to Caps lock and spacings,please double check the names entered.""")      
    

#wipes the data within the lists so when a new search is realized it doesnt overlap anything.The same is done when oppening the program in case the user closes the program without pressing the New Trip button.
def backButton_pressed(self, controller):
    global b, time_to_next_station, total_time_list, display_route, route_line, route_lines, end_data
    b.clear()
    time_next_station.clear()
    total_time_list.clear()
    display_route.clear()
    route_line.clear()
    route_lines.clear()
    end_data.clear()
    
    records = self.tree.get_children()
    for element in records:
        self.tree.delete(element)
    
    self.end_data.delete("1.0", 'end')
    
    controller.show_frame("startFrame")
#displays the details to the user by providing the tree created in the nextFrame with the data aquired by dijkstra.
def display_details(self, controller):
    display_route_end = [[x, *z] for x, z in zip(total_time_list, display_route)]
    

    
    records = self.tree.get_children()
    for element in records:
        self.tree.delete(element)
    
    for row in display_route_end:
        self.tree.insert('', 0, text=str(), values=(row[1], row[2], row[3], row[4], row[0]))
    
    end_data = []
    
    for i in range(len(route_lines)):
        end_data_row = []
        
        current_line = route_lines[i][0]
        
        previous_line = ""
        if i > 0:
            previous_line = route_lines[i-1][0]
            
        next_line = ""
        if i < len(route_lines)-1:
            next_line = route_lines[i+1][0]
            
        if current_line is not previous_line:
            end_data_row.append("{}".format(current_line))
            end_data_row.append("from {}".format(route_lines[i][1]))
            
        if next_line is not current_line:
            end_data_row.append("to {} - change to".format(route_lines[i][2]))
        
        if i < len(route_lines)-1:
            end_data.append(end_data_row)
        else:
            end_data_row.pop()
            end_data_row.append("to {}".format(b[0]))
            end_data.append(end_data_row)

    self.end_data.delete("1.0", 'end')

    for row in end_data:
        for item in row:
            self.end_data.insert("end", item)
            self.end_data.insert("end", "\n")


    self.end_data.insert("end", "Total travel time: ")
    self.end_data.insert("end", total_time_list[0])
    self.end_data.insert("end", " minutes")