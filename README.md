# leiwand
leiwandner graph plotter

Use this script like this

Use with 'mathematica' string
python leiwand.py mathematica={{weight,vertex1,mode1,vertex2,mode2},{weight,vertex1,mode1,vertex2,mode2}}

Or get the data into a file which list the data of the edges like:
weight vertex1 mode1 vertex2 mode2
weight vertex1 mode1 vertex2 mode2

python leiwand.py in=filename

You can call the script with several options like this
python leiwand.py in=filename key1=value1 key2=value2

option keys are the following  
out="graph" #outputfiles will be graph.tex and graph.pdf  
line_width=2.0  
color0="{RGB}{0,0,204}"  # defines the color for mode 0  
color1="{RGB}{0,204,0}"  # defines the color for mode 1  
color2="{RGB}{204,0,0}"  # defines the color for mode 2  
vertex_color="{RGB}{255,250,205}" # defines the background color of the vertices  
