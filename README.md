# EZGrid

Using `tkinter.grid()` can be very powerful, but is also incredibly arduous to implement well.  
It is especially difficult to add new columns in the middle of your grid, and increasing the span of a widget to fit more within it's height/width is terribly difficult.  
EZGrid seeks to make this all possible and very fast, while retaining most of the functionality of your widgets (more coming soon).  
EZGrid also allows rows to be split in ways that were previously very difficult.  

## How to use

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
> `ezgrid` uses a table set up similar to markdown to define a grid.  
> Each widget is enclosed in pipes (`|`). The widget references is enclosed in curly braces `{}`.  
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
> __references cannot be `EZNONE` or `EZPLACEHOLDER`, these will cause likely undesired behaviours__  
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

## `tkwidgets`

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


## `ezgrid._display()` and `ezgrid._clear()`

> - Running `ezgrid._display()` will run `ezgrid._clear()`, then place each widget in that grid using `tkinter.grid()`.
> - Running `ezgrid._clear()` will forget all widgets.   
> 
> If you would like to forget a specific widget or add a new one, add it to `ezgrid.widgets:list`.

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

