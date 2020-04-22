from planar import Polygon
import sys

#I spü mit System, schreib ma immer Ollas auf
#Des muasst mochn, weil sunst host ka Chance

docstring="""
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
"""

variables = {
    "line_width": 2.0,
    "color0": "{RGB}{0,0,204}",
    "color1": "{RGB}{0,204,0}",
    "color2": "{RGB}{204,0,0}",
    "vertexcolor": "{RGB}{250,250,250}",
    "fontcolor": "{RGB}{0,0,0}",
    "bend00":"-5",
    "bend11":"5",
    "bend22":"0",
    "bend01":"-10",
    "bend10":"10",
    "bend02":"-15",
    "bend20":"15",
    "bend12":"-20",
    "bend21":"20",
    "angle":180,
    "vertices": None,
    "whitespace": "10pt"
}

print(docstring)
for k,v in variables.items():
    print("{}={}".format(k,v))

print("""
Additional options are:
bendall=value  | set all bendxx angles to same value
"""
)

filename = "data.txt"
output = "graph"
for arg in sys.argv:
    if "in=" in arg:
        filename = arg.split("=")[1]
    if "out=" in arg:
        output = arg.split("=")[1]
    elif "=" in arg:
        tmp = arg.split("=")
        variables[tmp[0]] = tmp[1]

if "bendall" in variables:
    for x in ["00", "11", "22", "01", "10", "02", "20", "21", "12"]:
        variables["bend"+x] = variables["bendall"]

external_vertices = None
if variables['vertices'] is not None:
    external_vertices = variables["vertices"].split(' ')
    # reverse order (drawing is counter-clockwise)
    external_vertices = list(reversed(external_vertices))
    print("got vertices: ", external_vertices)

whitespace = None
if variables["whitespace"] is not None:
    whitespace = variables["whitespace"]

with open(output + ".tex", "w") as outf:
    data = []
    if "mathematica" in data:
        lines = data["mathematica"].split("{")
        for line in lines:
            if "}" in line:
                tmp = line.split("}")
                data.append(
                    (float(tmp[0]), str(tmp[1]).strip(), int(tmp[2]), str(tmp[3]).strip(), int(tmp[4].strip("}"))))
    else:
        with open(filename, "r") as f:
            for line in f:
                if line == "\n":
                    print("caught blanc line")
                    continue
                tmp = line.split(",")
                print("tmp=", tmp, " tmp0=", tmp[0])
                data.append((float(tmp[0]), str(tmp[1]).strip(), int(tmp[2]), str(tmp[3]).strip(), int(tmp[4])))

    optionmap = {
        (0, 0): "color=zerocol, bend right="+variables["bend00"],
        (1, 1): "color=onecol, bend right="+variables["bend11"],
        (2, 2): "color=twocol, bend right="+variables["bend22"],
        (0, 1): "bicolor={zerocol}{onecol}, bend left="+variables["bend01"],
        (1, 0): "bicolor={onecol}{zerocol}, bend right="+variables["bend10"],
        (0, 2): "bicolor={zerocol}{twocol}, bend left="+variables["bend20"],
        (2, 0): "bicolor={green}{zerocol}, bend right="+variables["bend02"],
        (1, 2): "bicolor={onecol}{twocol}, bend left="+variables["bend12"],
        (2, 1): "bicolor={twocol}{onecol}, bend right="+variables["bend21"],
    }
    
    if whitespace is not None:
        print("\documentclass[border={}]{}".format(whitespace, r"{standalone}"), file=outf)
    else:
        print(r"\documentclass{standalone}", file=outf)
    print(r"""
    
    \usepackage{tikz}
    \usepackage{verbatim}
    
    \usetikzlibrary{decorations.markings}
    
    \begin{document}
    \pagestyle{empty}
""",file=outf)
    colors=r"\definecolor{vertexcol}"+variables["vertexcolor"]
    colors+=r"\definecolor{onecol}"+variables["color0"]
    colors+=r"\definecolor{twocol}"+variables["color1"]
    colors+=r"\definecolor{zerocol}"+variables["color2"]
    colors+=r"\definecolor{fontcolor}" + variables["fontcolor"]
    print(colors, file=outf)
    print(r"""
    \newlength\mylen
    % check https://tex.stackexchange.com/questions/270001/tikz-coloring-edge-segments-with-different-colors
    \tikzset{
    bicolor/.style n args={2}{
      decoration={
        markings,
        mark=at position 0.5 with {
          \node[draw=none,inner sep=0pt,fill=none,text width=0pt,minimum size=0pt] {\global\setlength\mylen{\pgfdecoratedpathlength}};
        },
      },
      draw=#1,
      dash pattern=on 0.5\mylen off 1.0\mylen,
      preaction={decorate},
      postaction={
        draw=#2,
        dash pattern=on 0.5\mylen off 0.5\mylen,dash phase=0.5\mylen
      },
      }
    }
    
    \begin{tikzpicture}
      \tikzstyle{vertex}=[circle, draw=black, ultra thick ,fill=vertexcol!80,minimum size=15pt]\textbf{}
    """, file=outf)

    vertices = []
    weights = []
    for d in data:
        weights.append(abs(d[0]))
        vertices.append(d[1])
        vertices.append(d[3])
    vertices = list(set(vertices))
    max_weight = max(weights)

    
    # check if vertices where specified manually
    if external_vertices is not None:
        print("replacing: ", vertices)
        print("with external vertices: ", external_vertices)
        vertices = external_vertices
    else:
        #sort vertices alphabetically
        vertices = list(reversed(sorted(vertices)))

    poly = Polygon.regular(len(vertices), radius=5, angle=float(variables["angle"]))

    for i, coord in enumerate(poly):
        print(coord)
        print(r"\node[vertex] ({name}) at ({x},{y}) {xname};".format(name=vertices[i], xname=r"{\color{fontcolor}" + vertices[i] + "}",
                                                                     x=coord[0], y=coord[1]), file=outf)

    edge_string = r"\path ({v1}) edge[{options}, opacity={opacity}] ({v2});"
    for d in data:
        assert (len(d) == 5)
        weight = d[0]
        v1 = d[1]
        t1 = d[2]
        v2 = d[3]
        t2 = d[4]
        opacity = max(0.3, abs(weight) / max_weight)
        print(edge_string.format(v1=v1, v2=v2,
                                 options="line width={lw},".format(lw=variables["line_width"]) + optionmap[(t1, t2)],
                                 opacity=opacity), file=outf)

    print(r"""
    \end{tikzpicture}
    
    \end{document}
    """, file=outf)

print("created {}.tex".format(output))
print("trying to compile with pdflatex ... might be caught in endless loop")

import subprocess
from shutil import which

system_has_pdflatex = which("pdflatex") is not None
if not system_has_pdflatex:
    raise Exception("You need pdflatex in order to export circuits to pdfs")

with open(output + ".log", "w") as file:
    subprocess.call(["pdflatex", output + ".tex"], stdout=file)

print("created {}.pdf".format(output))
