from tkinter import *
import time


class WidgetData:

    def __init__(self, name):
        self.row = 0
        self.column = 0
        self.rowspan = 1
        self.columnspan = 0
        self.name = name
        self.ipady = 0
        self.ipadx = 0
        self.wij = None
    
    def __str__(self):
        return f"{self.name} | pos:({self.column}, {self.row}) | span:({self.columnspan}, {self.rowspan})"

def _time_it(function, *args, iterations=10000):
    rangeI = range(iterations)
    start = time.time()
    for i in rangeI:
        function(*args)
    end = time.time()
    print(f"took: {round(end-start, 5)}s")
    print(f"ips: {int(iterations/(end-start))}")


def get_name(cell):
    name = ""
    collect_name = False
    for _ in cell:
        if _ == "{": collect_name = True
        elif _ == "}": break
        elif collect_name:
            name += _
    return name

def get_cells(layout):
    cells = []
    cell = ""
    row = -1
    i = 0
    while True:
        try:
            _ = layout[i]
            if _ == "\n":
                i += 1
                row += 1
                cells.append([])
            elif _ == "|":
                cells[row].append(cell + "|")
                cell = ""
            else:
                cell += _
            i += 1
        except: return cells

def get_colIxs(row, colCutoffs, rowNum=0):
    cutoffs = []
    prev = 0
    for col in range(len(row)):
        ix = len(row[col]) + prev
        current = colCutoffs[ix]
        try: columnspan = current - colCutoffs[prev]
        except: columnspan = current + 1
        name = get_name(row[col])
        if name == "": name = "EZNONE"
        wrkWidg = WidgetData(name)
        wrkWidg.column = current - columnspan + 1
        wrkWidg.columnspan = columnspan
        wrkWidg.row = rowNum
        cutoffs.append(wrkWidg)
        prev += len(row[col])
    return cutoffs

def get_maxCols(cells):
    maxCols = 0
    wrow = []
    colCutoffs = {}
    for row in cells:
        if len(row) > maxCols:
            maxCols = len(row)
            wrow = row

    ixs = []
    prev = 0
    ix = 0
    for row in cells:
        prev = 0
        ix = 0
        for col in row:
            ix = len(col) + prev 
            if ix not in ixs:
                ixs.append(ix)
            prev = ix
    ixs = sorted(ixs)

    i = 0
    for key in ixs:
        colCutoffs[key] = i
        i += 1

    return maxCols, colCutoffs


def search_col(someWijs, starti, column, columnspan):
    i = starti-1
    while True:
        try:
            if someWijs[i].column == column and someWijs[i].columnspan == columnspan:
                print(someWijs[i])
                return i
            else: 
                i -= 1
        except:
            raise Exception("blank cell not in line with a filled cell, cannot create multi-row widget")


class EZGrid:

    def __init__(self, layout:str, root:Toplevel, tkwidgets={ }):
        
        self.tkwidgets = tkwidgets
        self.root = root
        self.toRemove = []
        if layout[0] != "\n": layout = "\n" + layout
        if layout[-1] == "\n": layout = layout[:-1]
        
        i = 1
        while True:
            try:
                if layout[i] == "\n":
                    layout = layout[:i] + "|{EZPLACEHOLDER}|\n" + layout[i+1:]
                    i += len("|{EZPLACEHOLDER}|\n")
                i += 1
            except: 
                layout += "|{EZPLACEHOLDER}|"
                break

        cells = get_cells(layout)
        maxRows = len(cells)
        maxCols, colCutoffs = get_maxCols(cells)
        cellsWithIX = [get_colIxs(cells[rowi], colCutoffs, rowNum=rowi) for rowi in range(len(cells))]
        widgetDatas = []
        for row in cellsWithIX:
            widgetDatas.extend(row)

        wiji = 0
        while True:
            try:
                if widgetDatas[wiji].name == "EZNONE":
                    connectedWiji = search_col(widgetDatas, wiji, widgetDatas[wiji].column, widgetDatas[wiji].columnspan)
                    widgetDatas.pop(wiji)
                    widgetDatas[connectedWiji].rowspan += 1
                    wiji -= 1
                wiji += 1
            except: break
                

        self.widgets = widgetDatas

        for wij in self.widgets:
            try: wij.wij = self.tkwidgets[wij.name]
            except: pass

    def _display(self):

        self._clear()
        self.toRemove = []

        print([w.__str__() for w in self.widgets])

        for w in self.widgets:
            if w.wij == None: 
                if w.name != "EZPLACEHOLDER":
                    w.wij = Label(text=f" {w.name} ", borderwidth=2, relief="groove")
                elif w.name == "EZPLACEHOLDER":
                    self.toRemove.append(Label(text=""))
                    w.wij = self.toRemove[-1]
            w.wij.grid(
                row=w.row,
                column=w.column,
                rowspan=w.rowspan,
                columnspan=w.columnspan,
                sticky=(N, E, S, W)
            )
        
        print([w.__str__() for w in self.widgets])
        print([w.__str__() for w in self.toRemove])

        width = 0
        try: 
            self.toRemove[-1].update()
            width = self.toRemove[-1].winfo_width()
        except: pass
        self.root.update()
        self.root.geometry(f"{self.root.winfo_width()-width}x{self.root.winfo_height()}")
        self.root.update()
        

    def _clear(self):
        for wij in self.widgets:
            try: wij.wij.grid_forget()
            except: pass

        for wij in self.toRemove:
            try: wij.wij.grid_forget()
            except: pass

