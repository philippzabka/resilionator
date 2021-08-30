# Resilionator
Resilionator is a small and portable Python application for identifying and mitigating potential weak points in networks. The application is built with Python's standard GUI toolkit [Tkinter](https://docs.python.org/3/library/tkinter.html) and [NetworkX](https://networkx.org/). The tool is intended primarily for university lecturers or students, but also for small and medium-sized companies and households.

# User Documentation

## Installation
Resilionator is available for Windows, macOS and Linux (64-bit operating system, x64-based processor). [Download](https://ucloud.univie.ac.at/index.php/s/JfBASDl7sSR3WdM) the appropriate file for your operating system and follow the steps described above to run the application. 

**Windows**
Download the file located in ```windows/Resilionator.zip```. Unpack it and then double click on the file in order to run it.

**maOS**
Download the file located in ```macOS/Resilionator.zip```. Unpack it and then double click on the file in order to run it.

**Linux (Ubuntu)**
Download the file located in ```linux/Resilionator.zip```. Unpack it and then open the terminal and drag and drop the file into the terminal window then hit enter.


## Usage
Resilionator offers various functionalities, which are described below:

**Quickmenu (Top)**
The quick menu allows quick access to node/edge creation, creating a test graph or deleting a graph. There is also the option to change the layout of the graph.

**Menu: Graph**
- Show graph: Show the current graph.
- Create random graph: Creates a random graph for quick testing.
- Import graph: Import a graph from a ```.txt```, ```.gml``` or ```.graphml``` file. Text file syntax has to be NetworkX compatile. For more details please consult  [File Format](https://networkx.org/documentation/stable/reference/readwrite/edgelist.html#format).
- Export graph: Export the graph into a ```.txt```, ```.gml``` or ```.graphml``` file.  
- Save graph as image: Save the current graph as ```.png or .jpg```.
- Remove graph: Remove the current graph.
- Node
  - Add node: Add a new node to the graph.
  - Remove node: Remove a node from the graph. 
- Edge
  - Add edge: Add a new edge to the graph. The edge endpoints will be created automatically if the do not exist yet.
  - Remove edge: Remove an edge from the graph.

**Menu: Analysis**
- Connectivity
  - Node connectivity: Check if the current graph is still connected after removing a specific node. This action is peformed for all nodes in the graph. 
  - Edge connectivity: Check if the current graph is still connected after removing a specific edge. This action is peformed for all edges in the graph.
- Augmentation
  - K-Node augmentation: Make the current graph resilient against one or two node failures.
  - K-Edge augmentation: Make the current graph resilient against one or two edge failures.

**Menu: Routing**
- Dijkstra - Original: Dijkstra shortest path algorithm. A ```source``` and ```target``` node need to be specified. Additionally nodes can be excluded from the path finding process. 
- Dijkstra - Recalulated distances: Dijkstra shortest path algortihm, however distances are recalculated. This prevents the algorithm to get stuck if nodes become unavailable during the routing process.
- Custom Routing: The user can specify his own simple routing process by providing a priority list. 
  - Priority list: A  ```.txt``` file containing the nodes of the graph with their neighbors ordered after their priority. The file doesn't have to contain all nodes or neighbors of a node. However, note that the routing algorithm will ignore nodes or neighbors that are not explicitly listed.
  - Syntax:  ```<node>{<neighbor 1>,<neighbor 2>,...,<neighbor n>}```. 

**Priority list example**
```python
b{c}
c{e,a}
e{l,f,c,a}
a{c,d,e}
l{f,e}
f{g,l,e}
g{j,h}
j{h,k}
k{i}
```

# Developer Documentation

For enhancing Resilionator we recommend a solid knowledge in Python as well as graph theory. Further we recommend some experience with Tkinter and NetworkX.
Resilionator is split into frontend and backend. All calculations concerning networks are processed in the backend. The results are then forwarded to the frontend where they are subsequently displayed. 

Now we introduce some functions in Resiliontor, which can be used to out of the box:

## Frames 

- ```createMainFrame```: Creates a frame that is appended to the root window.
- ```createRightFrame``` and ```createLeftFrame```: Creates a paned window. If both frames are created, both will take up an equal amount of space. If only one frame is created it takes up the whole space.
- ```createDualFrameView```: A more convenient way of creating the frames specified above.
- ```createMenu```: Creates drop down menues. 
- ```createPopupWindow```: Creates a Toplevel style window which is appended to the root window. 
- ```createCanvas```: Creates a FigureCanvas which is necessary to display figures which are generated from Matplotlib.
- ```createScrollingFrame```: Creates a scrollable frame, which is appended to the main frame. 

## Garbage collection for frames

Frames in Tkinter need to be deleted manually, if not done correctly it may cause performance issues.

- ```destroyFrame```: Destroys a specific frame. 
- ```destroyAllFrames```: This method is useful if you want to completely change views. For this method to work frames need to be added to the ```frames``` list. However if you use any of the methods described above this will happend automatically. 

## Utility

- ```importGraph```: Imports a graph from a file. Files formats that are currently supported are ```.txt, .graphml and .gml```. 
- ```exportGraph```: Exports a graph to a file. Files formats that are currently supported are ```.txt, .graphml and .gml```. 
- ```saveGraphAsImage```: Saves the graph as an image, currently supported formats are ```.jpg and .png```. 

## Graph

An empty graph is automatically created in the ```init()``` function of the Resilionator class.

- ```addNode```: Adds a new node to the graph.
- ```addEdge```: Adds a new edge to the graph.
- ```removeNode```: Removes a node from the graph. 
- ```removeEdge```: Removes an edge from the graph. 
- ```deleteGraph```: Removes the current graph and creates a new empty graph.
- ```deleteGraph```: Checks if the current graph is empty - has no edges.

## Screenshots

**Homescreen**
![Homescreen](/screenshots/home.png?raw=true "Homescreen")

**Node Connectivity**
![Node connectivity](/screenshots/node_con.png?raw=true "Node connectivity")

**Dijkstra Routing**
![Dijkstra Routing](/screenshots/routing.png?raw=true "Dijkstra Routing")

**Failure Resistance**
![Failure Resistance](/screenshots/resistance.png?raw=true "Failure Resistance")

# Resilionator Project Website

Link to the website: https://www.netidee.at/resilionator

**The project Resilionator is funded by netidee.**

