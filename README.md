# EZGrid

Using `tkinter.grid()` can be very powerful, but is also incredibly arduous to implement well.  
It is especially difficult to add new columns in the middle of your grid, and increasing the span of a widget to fit more within it's height/width is terribly difficult.  
EZGrid seeks to make this all very easy to do, while retaining the basic functionality of your widgets (`tkinter.grid()` options to come).  
EZGrid also allows rows to be split in ways that were previously very difficult.  

# Table of contents
1. [Example](#example)
2. [How to use](#how-to-use)
3. [`root`](#root)
4. [`layout`](#layout)
    1. [Adding a widget](#adding-a-widget)
    2. [Important notes](#important-notes)
    3. [Adding multiple widgets](#adding-multiple-widgets)
    4. [Modifying widget columnspan](#modifying-widget-columnspan)
    5. [Modifying widget rowspan](#modifying-widget-rowspan)
    6. [Overlapping rowspan](#overlapping-rowspan)
5. [`tkwidgets`](#tkwidgets)
6. [Other](#other)

## Example

This example shows the all the functionality of the program.

```python
import tkinter as tk, ezgrid

root = tk.Tk()


page1 = """
|     {PAGE 1}     |{page select} |
|                  |{prv} |{nxt}  |
|{The Fresh Prince}|      |       |
|           {text1}               |
"""

tkwidgets = {
    'prv' : tk.Button(text="🡄"),
    'nxt' : tk.Button(text="🡆"),
    'text1' : tk.Text(font=("helvetica", 10), width=50, height=6)
}
tkwidgets['text1'].insert(tk.INSERT, FRESH)


page1 = ezgrid.EZGrid(page1, root, tkwidgets=tkwidgets)
page1._display()

root.mainloop()
```  
![](https://i.imgur.com/OfI2mnS.png)  

# How to use

`ezgrid` has one class: `ezgrid.EZGrid`.    
That class has only __3 attributes__ and __2 methods__ you need to worry about.  
The instantiation of an `ezgrid.EZGrid` object follows this format:
```python
ezgrid.EZGrid(layout, root, tkwidgets={ })
```  
## `root`  
> `root` is the `tkinter.Tk` or `tkinter.Toplevel` object where you would normally place your widgets using `tkinter.grid()`

## `layout`  
### Adding a widget
> EZGrid uses a table set-up not dissimilar to markdown to define a grid.  
> Each widget is enclosed in pipes (`|`). The widget references are enclosed in curly braces `{}`.  
> For example:  
> ```python
> layout = """
> |{reference}|
> """
> ```  

> By default, a `tkinter.Label` will be created in the format:  
> ```python
> tkinter.Label(text="reference", borderwidth=2, relief="groove")  
> ```  

> If we display the above example, it would look like this:  
> 
> ![`|{reference}|`](https://i.imgur.com/bc0Bn68.png)

### Important notes
> __references cannot be `EZNONE` or `EZPLACEHOLDER`, these are used by the program for formatting, using them will result in undesired behaviour__  
> Only __one__ newline character is permitted either side of the layout string. Therefore, only the below formats are permitted:
> ```python
> layout = """
> line 0
> line 1
> """
> ```
> ```python
> layout = """
> line 0
> line 1"""
> ```
> ```python
> # This is useful if you are storing your layout in a .txt file.
> layout = """line 0
> line 1"""
> ```

### Adding multiple widgets
> We can easily add more widgets as below.  
> ```python
> layout = """
> |   {thing 1}   |{thing 2}|
> |{other thing 1}|{thing 3}|
> """
> ```
> ![](https://i.imgur.com/dyxAc8Y.png)  
> __alignment is not dependent on the position of the reference within the pipes.__ There can be any amount of white space either side of the curly braces.
 
### Modifying widget columnspan
> Pipes that do not line up split up the widgets vertically.
> ```python
> layout = """
> |{split 0}|{split 1}|{thing 2}|
> |  {other thing 1}  |{thing 3}|
> """
> ```
> ![](https://i.imgur.com/uO4EwMX.png)

### Modifying widget rowspan  
> Leaving white space beneath a widget will increase its `rowspan`.
> ```python
> layout = """
> |{larger rowspan}|{thing 2}|
> |                |{thing 3}|
> """
> ```
> ![](https://i.imgur.com/xrH91bg.png)  
> 
> Note: If you do not line up the pipes properly, there will be undesired behaviour.  
> Further Note: Increasing the `rowspan` works slightly differently in EZGrid, for rowspans greater than 2, the following occurs:  
> ```python 
> layout = """
> |{larger rowspan}|{thing 2}|
> |                |         |
> |                |         |
> """
> ```  
> results in  
> ![](https://i.imgur.com/DrFMX5W.png)  

### Overlapping rowspan
> Creating overlapping columns is very easy, but due to limitations with Tkinter, overlapping rows can be tricky.   
> in EZGrid, however, overlapping rows are very easy to implement! They work just like you'd expect:
> ```python
> layout = """
> |{thing 1}|{something else 1}|
> |{thing 3}|                  |
> |         |{something else 2}|
> """
> ```
> 
> ![](https://i.imgur.com/1JK3ZhO.png)  

### `tkwidgets`

> `tkwidgets` is simply a dictionary that allows you to redesign widgets by their reference.  
> example:  
> ```python
> layout = """
> |   { SOME BUTTONS }  |
> |{button 0}|{button 1}|
> |          |{thing 0 }|
> """
> 
> tkwidgets = {
>     'button 0' : Button(text="press here!"),
>     'button 1' : Button(text="no, here!")
> }
> ```
> ![](https://i.imgur.com/WpOVbGG.png)
> 
> As you can see, all layout options still work for custom widgets.

# Other

## `ezgrid._display()` and `ezgrid._clear()`

> - Running `ezgrid._display()` will run `ezgrid._clear()`, then places each widget on `root` using `tkinter.grid()`.
> - Running `ezgrid._clear()` will run `tkinter.grid_forget()` on all widgets.   
> 

## Things EZGrid is bad at

> It is possible, but difficult to modify the widgets on an `ezgrid.EZGrid`.  
> ```python
> newWidget = ezgrid.WidgetData('name') # WidgetData stores all data about a widget, it only takes one argument : 'name:str'
> newWidget.column, newWidget.row = 1, 2 # Specifying the row and column, rowspan and columnspan can be specified too
> newWidget.wij = Label(text="some text") # Creating a custom widget
> myGrid.widgets.append(newWidget) # Adding out new widget to our grid
> ```  

> It is currently impossible to pass arguments to `tkinter.grid()`. There will be options for this in the future.

