# zabka-resilionator-internal

# Resilionator
Resilionator is a small and portable Python application for identifying and mitigating potential weak points in networks. The application is still in development, so your feedback is welcome! It is build with Python's standard GUI toolkit [Tkinter](https://docs.python.org/3/library/tkinter.html) and [NetworkX](https://networkx.org/).


## Installation
Resilinator is available for Windows, macOS and Linux. [Download](https://ucloud.univie.ac.at/index.php/s/JfBASDl7sSR3WdM) the appropriate file for your operating system and follow the steps described above to run the application on your operating system. 

**Windows**
Download the file located in ```windows/resilionator.zip```. Unpack it and then double click on the file in order to run it.

**maOS**
Download the file located in ```macOS/resilionator.zip```. Unpack it and then double click on the file in order to run it.

**Linux (Ubuntu)**
Download the file located in ```linux/resilionator.zip```. Unpack it and then open the terminal and drag and drop the file into the terminal window then hit enter.


## Usage
Currently, Resilionator offers various functionalities, which are described below:

**Menu: Graph**
- Show graph: Show the current imported or created graph.
- Import graph: Import a graph from a ```text file (.txt)```. For testing purposes and syntax you can find an example graph located in ```graphs/testGraph.txt```.
- Export graph: Export the current graph into a ```.txt``` file. 
- Save graph as image: Save the current graph as ```.png or .jpg```.
- Remove graph: Remove the currently imported graph.
- Node
  - Add node: Add a new node to the graph.
  - Remove node: Remove a node from the graph. 
- Edge
  - Add edge: Add a new edge to the graph. The edge endpoints will be created automatically if the do not exist yet.
  - Remove edge: Remove an edge from the graph.

**Menu: Analysis**
- Connectivity
  - Node connectivity: Check if the current graph is still connected after removing a specific node. 
  - Edge connectivity: Check if the current graph is still connected after removing a specific edge. 
- Augmentation
  - K-Node augmentation: Make the current graph resiliient against one or two node failures.
  - K-Edge augmentation: Make the current graph resiliient against one or two edge failures.

