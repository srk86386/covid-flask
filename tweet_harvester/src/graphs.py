import matplotlib.pyplot as plt

## We will try to graphify the patients data with matplot lib

def simple_graph(x,y):
    """ steps to plot simple graph-
        1. get the X and Y axis data ( both the list should have same number of items.)
        2. call plot function (which by default plots line graph) with plt.plot(x,y)
        3. show() function
    """
    if len(x) != len(y):
        print(f" lenght of x and y are not same {len(x),len(y)}")
        return
    else:
        pass
    plt.plot(x,y)
    plt.show()

def graph_with_legends_title(x,y):
    """ steps to plot simple graph-
        1. get the X and Y axis data ( both the list should have same number of items.)
        2. call plot function (which by default plots line graph) with plt.plot(x,y, label='legend of this line plot')
        3. call plt.xlabel(""), plt.ylabel("") with text values for x and y axis respectively.
        4. call plt.title(""),to add title to the graph
        3. show() function
    """
    if len(x) != len(y):
        print(f" lenght of x and y are not same {len(x),len(y)}")
        return
    else:
        pass

    plt.plot(x,y, label='this is plot 1') # adding legend in the graph
    x1=[1,2,3,4,5]
    y1=[30,20,10,20,30]
    plt.plot(x1,y1, label='this is plot 2')
    plt.xlabel("x label titel")
    plt.ylabel("y label titel")
    plt.title("A cool graph")
    plt.legend()
    plt.show()

def bar_graph_with_legends_title(x,y):
    """ steps to plot simple graph-
        1. get the X and Y axis data ( both the list should have same number of items.)
        2. call bar function with plt.bar(x,y, label='legend of this line plot') to plot bar.
        3. call plt.xlabel(), plt.ylabel() with text values for x and y axis respectively.
        4. call plt.title(),to add title to the graph
        3. show() function
    """
    if len(x) != len(y):
        print(f" lenght of x and y are not same {len(x),len(y)}")
        return
    else:
        pass

    plt.bar(x,y, label='this is plot 1', color='r') # adding legend in the graph
    #x1=[1,2,3,4,5]
    #y1=[30,20,10,20,30]
    #plt.plot(x1,y1, label='this is plot 2' ,color='g')
    #x1=[6,7,8,9,10]
    #y1=[20,12,15,25,30]
    #plt.bar(x1,y1, label='this is plot 3', color='b')
    plt.xlabel("x label titel")
    plt.ylabel("y label titel")
    plt.title("A cool graph")
    plt.legend()
    plt.show()

def hist_graph_with_legends_title(population_data,buckets):
    """ steps to plot simple graph-
        2. call bar function with plt.bar(x,y, label='legend of this line plot') to plot bar.
        3. call plt.xlabel(), plt.ylabel() with text values for x and y axis respectively.
        4. call plt.title(),to add title to the graph
        3. show() function
    """
    #example data
    population_data = [22,32,45,23,45,130,12,4,8,90,67,76,65,56,56,90,87,97,78,120,122,56]
    buckets=[0,10,20,30,40,50,60,70,80,90,100,110,120,130]
    plt.hist(population_data,buckets, label='this is plot 1',histtype='bar',rwidth=0.8) # calling hist function instead of plot or bar to plot histogram
    plt.xlabel("x label titel")
    plt.ylabel("y label titel")
    plt.title("A cool graph")
    plt.legend()
    plt.show()

#simple_graph([1,2,3,4,5],[10,20,30,20,10])
#graph_with_legends_title([1,2,3,4,5],[10,20,30,20,10])
#bar_graph_with_legends_title([1,2,3,4,5],[10,20,30,20,10])
#hist_graph_with_legends_title([],[])
