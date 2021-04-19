from leiwand import leiwand

# write datafile with edges
# using 0 (red) 1 (blue) and 2 (green) for internal modes (will be collored accordingly)

vertices = ["a","b","c","d","e","f"]
indices = [1,2,3]
distance_h=2.0
distance_v=2.0

datafile="mario.txt"
with open(datafile, "w") as f:
    # add all the horizontal ones
    for i in range(len(vertices)//2):
        for j in indices:
            print("1.0, {}{j},0,{}{j},0".format(vertices[2*i],vertices[2*i+1],j=j),file=f)
    # add the others (can also manipulate the file later)
    print("1.0,a1,0,b1,1",file=f) # bending 01
    print("1.0,e1,0,f1,1",file=f)
    print("1.0,A1,1,c1,0",file=f) # leaving 10 straight
    print("1.0,A2,1,d1,0",file=f)
    print("1.0,A2,1,d2,0",file=f)
    print("1.0,A3,1,e2,0",file=f)
    print("1.0,A3,1,e3,0",file=f)
    print("1.0,A4,1,f2,0",file=f)
    print("1.0,A4,1,f3,0",file=f)

# creating vertex coordinates
coords={}
for i,name in enumerate(vertices):
    for j in indices:
        coords["{}{}".format(name,j)] = (distance_h*float(i),distance_v*float(j-1))
# special ones
coords["A1"]=(2.5*distance_h,-1.0)
coords["A2"]=(2.5*distance_h,1.0)
coords["A3"]=(3.5*distance_h,3.0)
coords["A4"]=(4.5*distance_h,3.0)

coordstring="".join(["coord_{}={},{} ".format(k,v[0],v[1]) for k,v in coords.items()])

args="in={} bend00=0 bend01=45 bend10=0 {}".format(datafile,coordstring)
print("calling: python leiwand.py {}\n".format(args))
print("for manual changes adapt repeat the above command and adapt {}".format(datafile))

leiwand(args.split(" "))

