
def ClearAllWidgetInLayout(layout):
    for i in reversed(range(layout.count())):  
        widgetToRemove = layout.itemAt( i ).widget()  
        layout.removeWidget( widgetToRemove )           # remove it from the layout list
        widgetToRemove.setParent( None )                # remove it from the gui


def ClearWidgetInLayoutByNames(layout,ObjectNames):
    for i in reversed(range(layout.count())):  
        widgetToRemove = layout.itemAt( i ).widget()
        if(widgetToRemove.objectName() in ObjectNames):
            layout.removeWidget( widgetToRemove )         
            widgetToRemove.setParent( None )              

def SetQLineEditColor(widget,r,g,b):
    SetColor = "color: rgb({0}, {1}, {2});".format(r,g,b)
    widget.setStyleSheet(SetColor)

def GetAllWidgetValInLayout(layout):
    for i in reversed(range(layout.count())):  
        widget = layout.itemAt( i ).widget() 
        print(type(widget))
        
             