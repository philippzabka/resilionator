import time
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
from ttkthemes import ThemedTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from FullScreen import FullScreenApp
import networkx as nx
import network as net
import webbrowser


class GUI:
    root = ThemedTk(theme="default")
    # ttk.Style().theme_use('default')
    windowWidth = 1500
    windowHeight = 800
    screenWidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    xCord = (screenWidth/2) - (windowWidth/2)
    yCord = (screenheight/2) - (windowHeight/2)
    root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, xCord, yCord))
    root.title("Resilionator")
    G = nx.Graph()
    nodesFromTextBox = list()
    frames = list()

    def __init__(self):
        self.layouts = ['Spring',
                        'Planar',
                        'Circular',
                        # 'Kamada-Kawai',
                        'Random',
                        'Spectral',
                        'Spiral']
        self.G = net.importGraphGraphml('./imports/testGraphRouting.graphml')
        self.dir = '/home'
        self.routingFilePath = ''
        self.createMenu()
        self.createCanvas()
        FullScreenApp(self.root)
        self.root.mainloop()


    def on_mousewheel(self, event):
        scroll = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(scroll, "units")


    def createScrollingFrame(self):
        self.createMainFrame()

        # Create canvas
        self.canvas = Canvas(self.mainFrame, width=160)
        self.canvas.pack(side=LEFT, fill=BOTH)
        # self.canvas.pack(fill=BOTH, expand=1)

        # Add scrollbar to canvas
        self.scrollBar = Scrollbar(self.mainFrame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollBar.pack(side=LEFT, fill=Y)
        # self.scrollBar.pack(side=RIGHT, fill=Y)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Create another frame inside canvas
        self.scrollFrame = Frame(self.canvas)

        # Add that new frame to a window in the canvas
        self.canvas.create_window((0, 0), window=self.scrollFrame, anchor="nw")


    def createConnectivityFrames(self, graph, figure, nodes=False):
        self.createDualFrameView()

        Lb = Listbox(self.leftFrame)
        Lb.configure(width=40)
        if nodes:
            Lb.insert(1, " Node: " + str(graph[0]))
        else:
            Lb.insert(1, " Edge: " + str(graph[0]))

        Lb.insert(2, " Connected: " + str(graph[1]))
        Lb.insert(3, " Has bridges: " + str(graph[2]))
        if graph[2]:
            Lb.insert(4, " Bridges: " + str(graph[3]))
            Lb.insert(4, " Articulation Points: " + str(graph[4]))
        Lb.pack(fill='both', expand=1)

        Button(self.leftFrame, text="Save as image", command=lambda: self.saveGraphAsImage(figure)).pack(fill=BOTH)

        try:
            self.fig.get_tk_widget().destroy()
        except Exception as e:
            print(e)
            pass
        self.fig = FigureCanvasTkAgg(figure, master=self.rightFrame)
        self.fig.get_tk_widget().pack(fill='both', expand=1)
        self.addFigureCanvasNavigation(self.fig, self.rightFrame)


    def createEdgeAugmentationFrames(self, graph, figure, edges):
        self.createDualFrameView()

        Lb = Listbox(self.leftFrame)
        Lb.configure(width=40)
        Lb.insert(1, " New egdes: " + str(edges))
        Lb.pack(fill='both', expand=1)

        Button(self.leftFrame, text="Adapt graph", command=lambda: self.adaptGraph(graph)).pack(fill=BOTH)
        Button(self.leftFrame, text="Export graph", command=lambda: self.exportGraph(graph)).pack(fill=BOTH)
        Button(self.leftFrame, text="Save graph as image", command=lambda: self.saveGraphAsImage(figure)).pack(fill=BOTH)

        try:
            self.fig.get_tk_widget().destroy()
        except Exception as e:
            print(e)
            pass
        self.fig = FigureCanvasTkAgg(figure, master=self.rightFrame)
        self.fig.get_tk_widget().pack(fill='both', expand=1)
        self.addFigureCanvasNavigation(self.fig, self.rightFrame)


    def createNodeAugmentationFrames(self, graph, figure, nodes):
        self.createDualFrameView()

        Lb = Listbox(self.leftFrame)
        Lb.configure(width=40)
        Lb.insert(1, " New nodes: " + str(nodes))
        Lb.pack(fill='both', expand=1)

        Button(self.leftFrame, text="Adapt graph", command=lambda: self.adaptGraph(graph)).pack(fill=BOTH)
        Button(self.leftFrame, text="Export graph", command=lambda: self.exportGraph(graph)).pack(fill=BOTH)
        Button(self.leftFrame, text="Save graph as image", command=lambda: self.saveGraphAsImage(figure)).pack(fill=BOTH)

        try:
            self.fig.get_tk_widget().destroy()
        except Exception as e:
            print(e)
            pass
        self.fig = FigureCanvasTkAgg(figure, master=self.rightFrame)
        self.fig.get_tk_widget().pack(fill='both', expand=1)
        self.addFigureCanvasNavigation(self.fig, self.rightFrame)


    def initConnectivity(self, nodesActive=True):

        self.isGraphEmtpy()
        self.createScrollingFrame()

        if nodesActive:
            graphs, figures = net.nodeConnectivity(self.G, layout=self.layouts[0])
            self.createConnectivityFrames(graphs[0], figures[0], nodes=nodesActive)
            for g, f, i in zip(graphs, figures, range(len(graphs))):
                if i == 0:
                    text = 'Original'
                else:
                    text = 'Removed: ' + str(g[0])
                Button(self.scrollFrame, text=text,
                       command=lambda graph=g, figure=f: self.createConnectivityFrames(graph, figure, nodes=nodesActive),
                       width=18).grid(row=i, column=0, sticky="we", columnspan=1)
        else:
            graphs, figures = net.edgeConnectivity(self.G, layout=self.layouts[0])
            self.createConnectivityFrames(graphs[0], figures[0])
            for g, f, i in zip(graphs, figures, range(len(graphs))):
                if i == 0:
                    text = 'Original'
                else:
                    text = 'Removed: ' + str(g[0])
                Button(self.scrollFrame, text=text,
                       command=lambda graph=g, figure=f: self.createConnectivityFrames(graph, figure),
                       width=18).grid(row=i, column=0, sticky="we", columnspan=1)


    def initEdgeAugmentation(self):
        self.isGraphEmtpy()
        self.createScrollingFrame()

        graphs, figures, edges = net.edgeAugementation(self.G, 3, layout=self.layouts[0])
        self.createEdgeAugmentationFrames(graphs[0], figures[0], edges[0])
        for g, f, e, i in zip(graphs, figures, edges, range(len(graphs))):
            if i == 0:
                text = 'Original'
            elif i == 1:
                text = 'Resistance: ' + str(i) + ' Fail'
            else:
                text = 'Resistance: ' + str(i) + ' Fails'
            Button(self.scrollFrame, text=text,
                   command=lambda graph=g, figure=f, edges=e: self.createEdgeAugmentationFrames(graph, figure, edges),
                   width=18).grid(row=i, column=0, sticky="we", columnspan=1)


    def initNodeAugmentation(self):
        self.isGraphEmtpy()
        self.createScrollingFrame()

        graphs, figures, nodes = net.kNodeAlgorithm(self.G, layout=self.layouts[0])
        self.createNodeAugmentationFrames(graphs[0], figures[0], nodes[0])
        for g, f, n, i in zip(graphs, figures, nodes, range(len(graphs))):
            if i == 0:
                text = 'Original'
            elif i == 1:
                text = 'Resistance: ' + str(i) + ' Fail'
            else:
                text = 'Resistance: ' + str(i) + ' Fails'
            Button(self.scrollFrame, text=text,
                   command=lambda graph=g, figure=f, nodes=n: self.createNodeAugmentationFrames(graph, figure, nodes),
                   width=18).grid(row=i, column=0, sticky="we", columnspan=1)


    def initRouting(self, source, target, original=False):
        try:
            path = list()
            if original:
                path = net.dijkstra_original(self.G, source, target, self.nodesFromTextBox)
            else:
                path = net.shortest_path_dijkstra(self.G, source, target, self.nodesFromTextBox)

            figures = net.create_figures_for_routing(self.G, source, target, path, self.nodesFromTextBox, layout=self.layouts[0])
            self.popupWindow.destroy()
            self.createScrollingFrame()
            self.createRoutingFrames(0, figures, path, path[0], self.nodesFromTextBox)
            for i, f in zip(range(len(figures)), figures):
                Button(self.scrollFrame, text="Step " + str(i + 1),
                       command=lambda index=i, figure=f: self.createRoutingFrames(index, figures, path, path[index],
                                                                                  self.nodesFromTextBox),
                       width=18).grid(row=i, column=0, sticky="we", columnspan=1)
        except Exception as e:
            messagebox.showerror(title=None, message=e)


    def initCustomRouting(self, source, target, file_path):
        path = list()
        try:
            print(file_path)
            path = net.build_path(self.G, source, target, self.nodesFromTextBox, file_path)
            figures = net.create_figures_for_routing(self.G, source, target, path, self.nodesFromTextBox, layout=self.layouts[0])
            self.popupWindow.destroy()
            self.createScrollingFrame()
            self.createRoutingFrames(0, figures, path, path[0], self.nodesFromTextBox)
            for i, f in zip(range(len(figures)), figures):
                Button(self.scrollFrame, text="Step " + str(i + 1),
                       command=lambda index=i, figure=f: self.createRoutingFrames(index, figures, path, path[index],
                                                                                  self.nodesFromTextBox),
                       width=18).grid(row=i, column=0, sticky="we", columnspan=1)
        except Exception as e:
            messagebox.showerror(title=None, message=e)


    def createRoutingAnimationWindow(self, figures):
        animationWindow = Toplevel(self.root)
        animationWindow.title('Routing Animation')
        animationWindow.geometry('1400x1000')
        for figure, index in zip(figures, range(len(figures))):
            fig = FigureCanvasTkAgg(figure, master=animationWindow)
            fig.get_tk_widget().pack(fill='both', expand=1)
            animationWindow.update()
            time.sleep(1.5)
            if index < len(figures)-1:
                fig.get_tk_widget().destroy()
        animationWindow.destroy()


    def createRoutingFrames(self, index, figures, path, currentNode, excluded=None):
        try:
            self.fig.get_tk_widget().destroy()
        except Exception as e:
            print(e)
            pass

        self.createDualFrameView()

        Lb = Listbox(self.leftFrame)
        Lb.configure(width=40)
        Lb.insert(1, "Routing step: (" + str(index+1) + "/" + str(len(path)) + ")")
        Lb.insert(2, "Current node: " + currentNode)
        Lb.insert(3, "Path: " + str(path))
        if excluded is not None:
            Lb.insert(4, "Excluded nodes: " + str(excluded))
        Lb.pack(fill='both', expand=1)

        Button(self.leftFrame, text="Animate routing", command=lambda: self.createRoutingAnimationWindow(figures)).pack(fill=BOTH)
        Button(self.leftFrame, text="Save graph as image", command=lambda: self.saveGraphAsImage(figures)).pack(fill=BOTH)

        self.fig = FigureCanvasTkAgg(figures[index], master=self.rightFrame)
        self.fig.get_tk_widget().pack(fill='both', expand=1)
        self.addFigureCanvasNavigation(self.fig, self.rightFrame)


    def addEdge(self, nodeID1, nodeID2, weight):
        if weight == '':
            weight = 1
        if nodeID1.strip() != "" and nodeID2.strip() != "":
            self.popupWindow.destroy()
            net.addEdge(self.G, nodeID1, nodeID2, float(weight))
            self.createCanvas(layout=self.layouts[0])
        else:
            Label(self.popupWindow, text="Field can't be empty", font=('calibre', 10, 'normal'), fg='red') \
                .grid(row=0, column=0, columnspan=2, padx=5, sticky="we")


    def removeEdge(self, nodeID1, nodeID2):
        self.popupWindow.destroy()
        net.removeEdge(self.G, nodeID1, nodeID2)
        self.createCanvas(layout=self.layouts[0])


    def addNode(self, nodeID):
        if nodeID.strip() != "":
            self.popupWindow.destroy()
            net.addNode(self.G, nodeID)
            self.createCanvas(layout=self.layouts[0])
        else:
            Label(self.popupWindow, text="Field can't be empty", font=('calibre', 10, 'normal'), fg='red')\
                .grid(row=0, column=0, columnspan=2, padx=5, sticky="we")


    def removeNode(self, nodeID):
        self.popupWindow.destroy()
        net.removeNode(self.G, nodeID)
        self.createCanvas(layout=self.layouts[0])


    def importTxTFile(self):
        filepath = filedialog.askopenfilename(initialdir=self.dir, title="Select a File",
                                              filetypes=(("Text files", "*.txt"),))
        self.routingFilePath = filepath
        partitionedString = filepath.rpartition('/')
        self.dir = partitionedString[0]

        self.popupWindow.destroy()
        self.createCustomRoutingWindow()

    def importGraph(self):
        filepath = filedialog.askopenfilename(initialdir=self.dir, title="Select a File",
                                              filetypes=(("Text files", "*.txt"),
                                                         ("Graphml files", "*.graphml"),
                                                         ("GML", "*.gml")))
        fileExtension = filepath.rpartition('.')
        if fileExtension[2] == "txt":
            self.G = net.importGraph(filepath)
            self.createCanvas(layout=self.layouts[0])
        if fileExtension[2] == "graphml":
            self.G = net.importGraphGraphml(filepath)
            self.createCanvas(layout=self.layouts[0])
        if fileExtension[2] == "gml":
            self.G = net.importGraphGml(filepath)
            self.createCanvas(layout=self.layouts[0])


        partitionedString = filepath.rpartition('/')
        self.dir = partitionedString[0]


    def exportGraph(self, G):

        self.isGraphEmtpy()

        filepath = filedialog.asksaveasfilename(initialdir=self.dir, title='Export graph',
                                                filetypes=[("Text files", "*.txt"),
                                                           ("Graphml files", "*.graphml"),
                                                           ("GML files", "*.gml")
                                                           ])

        fileExtension = filepath.rpartition('.')
        if fileExtension[2] == "txt":
            print(filepath)
            net.exportGraphTxt(G, filepath)
        if fileExtension[2] == "graphml":
            net.exportGraphGraphml(G, filepath)
        if fileExtension[2] == "gml":
            net.exportGraphGml(G, filepath)

        partitionedString = filepath.rpartition('/')
        self.dir = partitionedString[0]


    def saveGraphAsImage(self, figure):

        self.isGraphEmtpy()

        filepath = filedialog.asksaveasfilename(initialdir=self.dir, title='Save graph',
                                                filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")])
        if filepath:
            print(filepath)
            net.saveGraphAsImage(filepath, figure)

        partitionedString = filepath.rpartition('/')
        self.dir = partitionedString[0]


    def adaptGraph(self, newGraph):
        answer = messagebox.askokcancel("Warning", "Adapt current graph to this one?")
        if answer:
            self.G = newGraph
            self.createCanvas(layout=self.layouts[0])


    def removeGraph(self):
        answer = messagebox.askokcancel("Warning", "Delete current graph?")
        if answer:
            self.G = nx.Graph()
            self.createCanvas(layout=self.layouts[0])


    def validate_float_input(self, action, index, value_if_allowed,
                             prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if (action == '1'):
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True


    def createAddEdgeWindow(self):

        try:
            if len(self.G.nodes) < 2:
                raise nx.NetworkXError('Create at least two nodes to create an edge!')
        except Exception as e:
            messagebox.showerror(title=None, message=e)
            raise e

        self.createPopupWindow('Add edge')
        Label(self.popupWindow, text='Select 1.Endpoint:').grid(row=0, column=0, padx=5)
        nodeSelect1 = Combobox(self.popupWindow, values=[node for node in self.G.nodes],  state="readonly")
        nodeSelect1.current(0)
        nodeSelect1.bind("<<ComboboxSelected>>")
        nodeSelect1.grid(row=0, column=1)

        Label(self.popupWindow, text='Select 2.Endpoint:').grid(row=1, column=0, padx=5)
        nodeSelect2 = Combobox(self.popupWindow, values=[node for node in self.G.nodes],  state="readonly")
        nodeSelect2.current(1)
        nodeSelect2.bind("<<ComboboxSelected>>")
        nodeSelect2.grid(row=1, column=1)

        weight = StringVar(self.popupWindow)
        Label(self.popupWindow, text='Weight:').grid(row=2, column=0, padx=5)

        vcmd = (self.popupWindow.register(self.validate_float_input),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        Entry(self.popupWindow, textvariable=weight, validate='key', validatecommand=vcmd).grid(row=2, column=1)

        Button(self.popupWindow, text="Confirm", command=lambda: self.addEdge(nodeSelect1.get(), nodeSelect2.get(), weight.get()),
               width=15).grid(row=3, column=0, sticky="we", columnspan=2)


    def createRemEdgeWindow(self):

        self.isGraphEmtpy()

        self.createPopupWindow('Remove edge')
        Label(self.popupWindow, text='Select an Edge:').grid(row=0, column=0, padx=5)
        edgeSelect = Combobox(self.popupWindow, values=[edge for edge in self.G.edges],  state="readonly")
        edgeSelect.current(0)
        edgeSelect.bind("<<ComboboxSelected>>")
        edgeSelect.grid(row=0, column=1)

        nodes = edgeSelect.get().split()
        Button(self.popupWindow, text="Confirm", command=lambda: self.removeEdge(nodes[0], nodes[1]),
               width=15).grid(row=1, column=0, sticky="we", columnspan=2)


    def createAddNodeWindow(self):
        self.createPopupWindow('Add node')
        Label(self.popupWindow, text='Node:').grid(row=1, column=0, padx=5)
        nodeID = StringVar()
        Entry(self.popupWindow, textvariable=nodeID, font=('calibre', 12, 'normal')) \
            .grid(row=1, column=1, pady=5, padx=5)
        Button(self.popupWindow, text="Confirm", command=lambda: self.addNode(nodeID.get()),
               width=15).grid(row=2, column=0, sticky="we", columnspan=2)


    def createRemNodeWindow(self):

        self.isGraphEmtpy()

        self.createPopupWindow('Remove node')
        Label(self.popupWindow, text='Select a Node:').grid(row=0, column=0, padx=5)
        nodeSelect = Combobox(self.popupWindow, values=[node for node in self.G.nodes],  state="readonly")
        nodeSelect.current(0)
        nodeSelect.bind("<<ComboboxSelected>>")
        nodeSelect.grid(row=0, column=1)

        Button(self.popupWindow, text="Confirm", command=lambda: self.removeNode(nodeSelect.get()),
               width=15).grid(row=1, column=0, sticky="we", columnspan=2)


    def createTextBox(self, row, column, text=None):
        try:
            self.nodeText.destroy()
        except Exception as e:
            print(e)

        self.nodeText = Text(self.popupWindow, height=4, width=23)
        if text is not None:
            self.nodeText.insert(END, text)
        self.nodeText.config(state=DISABLED)
        self.nodeText.grid(row=row, column=column)


    def createNodesFromTextBox(self, node, row, column):
        if node in self.nodesFromTextBox:
            messagebox.showerror(title='Failed', message=node + ' is already in the list!')
        else:
            self.nodesFromTextBox.append(node)
            self.createTextBox(row, column, self.nodesFromTextBox)


    def createRoutingWindow(self, original=False):

        self.isGraphEmtpy()

        # Clear list when window is created
        self.nodesFromTextBox.clear()

        self.createPopupWindow('Dijkstra')
        Label(self.popupWindow, text='Source:').grid(row=0, column=0, padx=5)
        source = Combobox(self.popupWindow, values=[node for node in self.G.nodes], state="readonly")
        source.current(0)
        source.bind("<<ComboboxSelected>>")
        source.grid(row=0, column=1)

        Label(self.popupWindow, text='Target:').grid(row=1, column=0, padx=5)
        target = Combobox(self.popupWindow, values=[node for node in self.G.nodes], state="readonly")
        target.current(1)
        target.bind("<<ComboboxSelected>>")
        target.grid(row=1, column=1)

        Label(self.popupWindow, text='Exclude:').grid(row=2, column=0, padx=5)
        exclude = Combobox(self.popupWindow, values=[node for node in self.G.nodes], state="readonly")
        exclude.bind("<<ComboboxSelected>>")
        exclude.grid(row=2, column=1)

        self.createTextBox(3, 1, 'Excluded nodes...')

        Button(self.popupWindow, text="Add",
               command=lambda: self.createNodesFromTextBox(exclude.get(), 3, 1),
               width=10).grid(row=2, column=2, sticky="we", columnspan=1)

        Button(self.popupWindow, text="Clear",
               command=lambda: (self.nodesFromTextBox.clear(), self.createTextBox(3, 1, 'Excluded nodes...')),
               width=10).grid(row=3, column=2, sticky="we", columnspan=1)

        Button(self.popupWindow, text="Start",
               command=lambda: self.initRouting(source.get(), target.get(), original),
               width=15).grid(row=5, column=0, sticky="we", columnspan=3)


    def createCustomRoutingWindow(self):

        self.isGraphEmtpy()

        # Clear list when window is created
        self.nodesFromTextBox.clear()

        self.createPopupWindow('Custom Routing')

        Label(self.popupWindow, text='Priorities:').grid(row=0, column=0, padx=5, pady=10)
        Button(self.popupWindow, text="Open file",
               command=self.importTxTFile,
               width=15).grid(row=0, column=1, sticky="we", columnspan=3, pady=10)

        loadedFile = self.routingFilePath.rpartition('/')
        Label(self.popupWindow, text='File:').grid(row=1, column=0, padx=5, pady=10)
        Label(self.popupWindow, text=loadedFile[2]).grid(row=1, column=1, padx=5, pady=10)

        Label(self.popupWindow, text='Source:').grid(row=2, column=0, padx=5)
        source = Combobox(self.popupWindow, values=[node for node in self.G.nodes], state="readonly")
        source.current(0)
        source.bind("<<ComboboxSelected>>")
        source.grid(row=2, column=1)

        Label(self.popupWindow, text='Target:').grid(row=3, column=0, padx=5)
        target = Combobox(self.popupWindow, values=[node for node in self.G.nodes], state="readonly")
        target.current(1)
        target.bind("<<ComboboxSelected>>")
        target.grid(row=3, column=1)

        Label(self.popupWindow, text='Exclude:').grid(row=4, column=0, padx=5)
        exclude = Combobox(self.popupWindow, values=[node for node in self.G.nodes], state="readonly")
        exclude.current(2)
        exclude.bind("<<ComboboxSelected>>")
        exclude.grid(row=4, column=1)

        self.createTextBox(5, 1, 'Excluded nodes...')

        Button(self.popupWindow, text="Add",
               command=lambda: self.createNodesFromTextBox(exclude.get(), 5, 1),
               width=10).grid(row=4, column=2, sticky="we", columnspan=1)

        Button(self.popupWindow, text="Clear",
               command=lambda: (self.nodesFromTextBox.clear(), self.createTextBox(3, 1, 'Excluded nodes...')),
               width=10).grid(row=5, column=2, sticky="we", columnspan=1)

        Button(self.popupWindow, text="Start",
               command=lambda: self.initCustomRouting(source.get(), target.get(), self.routingFilePath),
               width=15).grid(row=6, column=0, sticky="we", columnspan=3)


    def createDualFrameView(self):
        try:
            self.destroyFrame(self.leftPW)
        except Exception as e:
            print(e)
        try:
            self.destroyFrame(self.rightPW)
        except Exception as e:
            print(e)

        self.leftPW = PanedWindow(self.mainFrame, orient=HORIZONTAL)
        self.leftFrame = Frame(self.leftPW)
        self.leftPW.pack(fill='both', expand=1)
        self.frames.append(self.leftPW)
        self.leftPW.add(self.leftFrame)

        self.rightPW= PanedWindow(self.mainFrame, orient=HORIZONTAL)
        self.rightFrame = Frame(self.rightPW)
        self.frames.append(self.rightPW)
        self.leftPW.add(self.rightPW)
        self.rightPW.add(self.rightFrame)


    def createLeftFrame(self):
        try:
            self.destroyFrame(self.leftFrame)
        except Exception as e:
            print(e)

        self.leftFrame = PanedWindow(self.mainFrame, orient=HORIZONTAL)
        self.frames.append(self.leftFrame)
        self.leftFrame.pack(fill='both', expand=1)


    def createRightFrame(self):
        try:
            self.destroyFrame(self.rightFrame)
        except Exception as e:
            print(e)

        self.rightFrame = PanedWindow(self.mainFrame, orient=HORIZONTAL)
        self.frames.append(self.rightFrame)
        self.leftFrame.add(self.rightFrame)


    def createMainFrame(self):
        self.destroyAllFrames()
        self.mainFrame = Frame(self.root)
        self.frames.append(self.mainFrame)
        self.mainFrame.pack(fill=BOTH, expand=1)


    def createNavigationFrame(self, frame=None):
        try:
            self.destroyFrame(self.navigationFrame)
        except Exception as e:
            print(e)

        # style = Style()
        # style.configure("BW.TLabel", background="grey")
        # style = "BW.TLabel" (Paste this into frame constructor)
        if frame is None:
            self.navigationFrame = Frame(self.mainFrame)
        else:
            self.navigationFrame = Frame(frame)
        self.frames.append(self.navigationFrame)
        self.navigationFrame.pack(fill=X)


    def addFigureCanvasNavigation(self, figureCanvas, parentFrame):
        # Add matplotlib toolbar
        NavigationToolbar2Tk(figureCanvas, parentFrame)


    def addNavigation(self):
        Label(self.navigationFrame, text='Graph Layout:').grid(row=0, column=0, padx=5)
        layoutSelect = Combobox(self.navigationFrame, values=self.layouts,  state="readonly")
        layoutSelect.current(0)
        layoutSelect.bind("<<ComboboxSelected>>", lambda x: self.changeLayout(layoutSelect.get()))
        layoutSelect.grid(row=0, column=1)

        Label(self.navigationFrame, text='Nodes:').grid(row=0, column=2, padx=5)
        Button(self.navigationFrame, text="+", command=self.createAddNodeWindow).grid(row=0, column=3)
        Button(self.navigationFrame, text="-", command=self.createRemNodeWindow).grid(row=0, column=4)

        Label(self.navigationFrame, text='Edges:').grid(row=0, column=5, padx=5)
        Button(self.navigationFrame, text="+", command=self.createAddEdgeWindow).grid(row=0, column=6)
        Button(self.navigationFrame, text="-", command=self.createRemEdgeWindow).grid(row=0, column=7)

        Label(self.navigationFrame, text='|').grid(row=0, column=8, padx=5)
        Button(self.navigationFrame, text="Create random graph", command=self.createRandomGraph).grid(row=0, column=9)
        Label(self.navigationFrame, text='|').grid(row=0, column=10, padx=5)
        Button(self.navigationFrame, text="Remove graph", command=self.removeGraph).grid(row=0, column=11)


    def changeLayout(self, selectedLayout):
        self.layouts.remove(selectedLayout)
        self.layouts.insert(0, selectedLayout)
        self.createCanvas(layout=selectedLayout)


    def createCanvas(self, layout='Spring', text=None):
        self.createMainFrame()
        self.createNavigationFrame()
        self.addNavigation()
        try:
            self.figCanvas.get_tk_widget().destroy()
        except Exception as e:
            print(e)
            pass

        if len(self.G.nodes) == 0:
            self.figCanvas = FigureCanvasTkAgg(net.createFigure(self.G, text='Import or create a graph'), master=self.mainFrame)
        elif text is None:
            text = 'Nodes ' + str(self.G.nodes)
            self.figCanvas = FigureCanvasTkAgg(net.createFigure(self.G, layout=layout, text=text), master=self.mainFrame)
        else:
            self.figCanvas = FigureCanvasTkAgg(net.createFigure(self.G, layout=layout, text=text), master=self.mainFrame)

        self.addFigureCanvasNavigation(self.figCanvas, self.mainFrame)

        self.figCanvas.get_tk_widget()
        self.figCanvas.get_tk_widget().pack(expand=1, fill="both")


    def createPopupWindow(self, title):
        self.popupWindow = Toplevel(self.root)
        self.popupWindow.title(title)
        centerCoord = self.calcRootCenter()
        self.popupWindow.geometry(f'+{centerCoord["x"]}+{centerCoord["y"]}')
        self.popupWindow.resizable(False, False)


    def createMenu(self):
        mainMenu = Menu(self.root)
        self.root.config(menu=mainMenu)
        graphMenu = Menu(mainMenu, tearoff=0)
        analysisMenu = Menu(mainMenu, tearoff=0)
        routingMenu = Menu(mainMenu, tearoff=0)
        helpMenu = Menu(mainMenu, tearoff=0)

        mainMenu.add_cascade(label='Graph', menu=graphMenu)
        mainMenu.add_cascade(label='Analysis', menu=analysisMenu)
        mainMenu.add_cascade(label='Routing', menu=routingMenu)
        mainMenu.add_cascade(label='Help', menu=helpMenu)

        graphMenu.add_command(label="Show graph", command=lambda: self.createCanvas(self.layouts[0]))
        graphMenu.add_command(label="Create random graph", command=self.createRandomGraph)
        graphMenu.add_command(label="Import graph", command=self.importGraph)
        graphMenu.add_command(label="Export graph", command=lambda: self.exportGraph(self.G))
        graphMenu.add_command(label="Save graph as image", command=lambda: self.saveGraphAsImage(net.createFigure(self.G)))
        graphMenu.add_command(label="Remove graph", command=self.removeGraph)

        nodeMenu = Menu(graphMenu, tearoff=0)
        graphMenu.add_cascade(label="Nodes", menu=nodeMenu)
        nodeMenu.add_command(label="Add node", command=self.createAddNodeWindow)
        nodeMenu.add_command(label="Remove node", command=self.createRemNodeWindow)

        edgeMenu = Menu(graphMenu, tearoff=0)
        graphMenu.add_cascade(label="Edges", menu=edgeMenu)
        edgeMenu.add_command(label="Add edge", command=self.createAddEdgeWindow)
        edgeMenu.add_command(label="Remove edge", command=self.createRemEdgeWindow)

        conMenu = Menu(analysisMenu, tearoff=0)
        analysisMenu.add_cascade(label="Connectivity", menu=conMenu)
        conMenu.add_command(label="Node connectivity", command=self.initConnectivity)
        conMenu.add_command(label="Edge connectivity", command=lambda: self.initConnectivity(nodesActive=False))

        augmentMenu = Menu(analysisMenu, tearoff=0)
        analysisMenu.add_cascade(label="Augmentation", menu=augmentMenu)
        augmentMenu.add_command(label="K-Edge augmentation", command=self.initEdgeAugmentation)
        augmentMenu.add_command(label="K-Node augmentation", command=self.initNodeAugmentation)

        routingMenu.add_command(label="Dijkstra - Original", command=lambda: self.createRoutingWindow(original=True))
        routingMenu.add_command(label="Dijkstra - Recalculated distances", command=self.createRoutingWindow)
        routingMenu.add_command(label="Custom Routing", command=self.createCustomRoutingWindow)

        helpMenu.add_command(label="Github Repository", command=lambda: self.openURL('https://github.com/philippzabka/resilionator'))
        helpMenu.add_command(label="About", command=self.createAboutWindow)

        # mainMenu.add_command(label="Quit", command=self.root.destroy)


    def calcRootCenter(self):
        root_x = int(self.root.winfo_rootx() + (self.root.winfo_width() / 2.25))
        root_y = int(self.root.winfo_rooty() + (self.root.winfo_height() / 3.0))
        return {'x': root_x, 'y': root_y}


    def destroyFrame(self, frame):
        try:
            frame.destroy()
        except Exception as e:
            print(e)


    def destroyAllFrames(self):
        for frame in self.frames:
            print(len(self.frames))
            try:
                frame.destroy()
            except Exception as e:
                print(e)
            finally:
                continue
        self.frames = list()


    def hideFrames(self):
        [frame.pack_forget() for frame in self.frames]


    def openURL(self, url):
        webbrowser.open(url)


    def isGraphEmtpy(self):
        try:
            if nx.is_empty(self.G):
                raise nx.NetworkXError('No graph found!')
        except Exception as e:
            messagebox.showerror(title=None, message=e)
            raise e


    def createRandomGraph(self):
        # self.removeGraph()
        self.G = net.createRandomGraph()
        self.createCanvas(layout=self.layouts[0])


    def createAboutWindow(self):
        self.createPopupWindow('About')
        f1 = Frame(self.popupWindow)
        f2 = Frame(self.popupWindow)
        f1.pack(fill=BOTH, expand=1)
        f2.pack(fill=BOTH, expand=1)

        url_python = 'https://www.python.org/'
        url_python_license = 'https://docs.python.org/3.8/license.html'
        url_matplotlib = 'https://matplotlib.org/stable/index.html'
        url_networkx = 'https://networkx.org/'
        url_networkx_license = 'https://raw.githubusercontent.com/networkx/networkx/master/LICENSE.txt'
        url_tkinter = 'https://docs.python.org/3.8/library/tkinter.html'
        url_re = 'https://docs.python.org/3.8/library/re.html'
        url_web = 'https://docs.python.org/3.8/library/webbrowser.html'
        url_rnd = 'https://docs.python.org/3.8/library/random.html'
        url_time = 'https://docs.python.org/3/library/time.html'
        url_ttkthemes = 'https://ttkthemes.readthedocs.io/en/latest/'
        url_ttkthemes_license = 'https://ttkthemes.readthedocs.io/en/latest/licenses.html'

        Label(f1, text='Author: 2021, Philipp Zabka').grid(row=0, column=0, padx=5, pady=5)
        Label(f1, text='This software uses following products:')\
            .grid(row=1, column=0, padx=5, pady=5, sticky='we')

        # Matplotlib Homepage and License
        label_matplotlib = Label(f2, text='Matplotlib', foreground="blue")
        label_matplotlib.grid(row=2, column=0, padx=5, pady=5)
        label_matplotlib_license = Label(f2, text='License', foreground="blue")
        label_matplotlib_license.grid(row=2, column=1, padx=5, pady=5)

        # NetworkX Homepage and License
        label_networkx = Label(f2, text='NetworkX', foreground="blue")
        label_networkx.grid(row=3, column=0, padx=5, pady=5)
        label_networkx_license = Label(f2, text='License', foreground="blue")
        label_networkx_license.grid(row=3, column=1, padx=5, pady=5)

        # Python Homepage and License
        label_python = Label(f2, text='Python 3.8', foreground="blue")
        label_python.grid(row=4, column=0, padx=5, pady=5)
        label_python_license = Label(f2, text='License', foreground="blue")
        label_python_license.grid(row=4, column=1, padx=5, pady=5)

        # Random Homepage and License
        label_rnd = Label(f2, text='Python-Random', foreground="blue")
        label_rnd.grid(row=5, column=0, padx=5, pady=5)
        label_rnd_license = Label(f2, text='License', foreground="blue")
        label_rnd_license.grid(row=5, column=1, padx=5, pady=5)

        # Re Homepage and License
        label_re = Label(f2, text='Python-Re', foreground="blue")
        label_re.grid(row=6, column=0, padx=5, pady=5)
        label_re_license = Label(f2, text='License', foreground="blue")
        label_re_license.grid(row=6, column=1, padx=5, pady=5)

        # Time Homepage and License
        label_time = Label(f2, text='Python-Time', foreground="blue")
        label_time.grid(row=7, column=0, padx=5, pady=5)
        label_time_license = Label(f2, text='License', foreground="blue")
        label_time_license.grid(row=7, column=1, padx=5, pady=5)

        # Web Homepage and License
        label_web = Label(f2, text='Python-Webbrowser', foreground="blue")
        label_web.grid(row=8, column=0, padx=5, pady=5)
        label_web_license = Label(f2, text='License', foreground="blue")
        label_web_license.grid(row=8, column=1, padx=5, pady=5)

        # Tkinter Homepage and License
        label_tkinter = Label(f2, text='Tkinter', foreground="blue")
        label_tkinter.grid(row=9, column=0, padx=5, pady=5)
        label_tkinter_license = Label(f2, text='License', foreground="blue")
        label_tkinter_license.grid(row=9, column=1, padx=5, pady=5)

        #Ttkthemes Homepage and License
        label_ttkthemes = Label(f2, text='Ttkthemes', foreground="blue")
        label_ttkthemes.grid(row=10, column=0, padx=5, pady=5)
        label_ttkthemes_license = Label(f2, text='License', foreground="blue")
        label_ttkthemes_license.grid(row=10, column=1, padx=5, pady=5)

        label_python.bind("<Button-1>", lambda e: self.openURL(url_python))
        label_python_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_tkinter.bind("<Button-1>", lambda e: self.openURL(url_tkinter))
        label_tkinter_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_networkx.bind("<Button-1>", lambda e: self.openURL(url_networkx))
        label_networkx_license.bind("<Button-1>", lambda e: self.openURL(url_networkx_license))
        label_matplotlib.bind("<Button-1>", lambda e: self.openURL(url_matplotlib))
        label_matplotlib_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_re.bind("<Button-1>", lambda e: self.openURL(url_re))
        label_re_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_web.bind("<Button-1>", lambda e: self.openURL(url_web))
        label_web_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_rnd.bind("<Button-1>", lambda e: self.openURL(url_rnd))
        label_rnd_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_time.bind("<Button-1>", lambda e: self.openURL(url_time))
        label_time_license.bind("<Button-1>", lambda e: self.openURL(url_python_license))
        label_ttkthemes.bind("<Button-1>", lambda e: self.openURL(url_ttkthemes))
        label_ttkthemes_license.bind("<Button-1>", lambda e: self.openURL(url_ttkthemes_license))


GUI()
