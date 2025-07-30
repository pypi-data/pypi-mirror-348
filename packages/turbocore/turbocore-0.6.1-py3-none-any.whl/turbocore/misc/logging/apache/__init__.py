import datetime
import turbocore
import sys
from rich.pretty import pprint as PP


def a2_errorlog(filename, funnel, transformation, selection):
    """Read typical apache errorlog.
    """

    selections = None
    if selection != "":
        selections = [ int(x) for x in  selection.split(",") ]

    transformations = None
    if transformation != "":
        transformations = []

    funnels = []
    if funnel != "":
        for f in funnel.split(","):
            cols = f.split("=")
            funnels.append([
                int(cols[0]),
                cols[1]
                ])

    with open(filename, 'r') as f:
        for line_ in f:
            line = line_.strip().replace("] [", "\t", 4).replace("[", "", 1).replace("] ", "\t", 1)
            cols = line.split("\t")
            in_funnel = True
            try:
                for fun in funnels:
                    if not fun[1].upper() in cols[fun[0]].upper():
                        in_funnel=False
                        break
            except:
                in_funnel = False

            if in_funnel:
                time_form = "%a %b %d %H:%M:%S.%f %Y"
                t = datetime.datetime.strptime(cols[0], time_form)
                t = t.replace(tzinfo=datetime.UTC)
                cols[0] = t.isoformat()
                colso = cols
                if selections is not None:
                    colso = [cols[xx_] for xx_ in selections]
                print("\t".join(colso))

def main():
    turbocore.cli_this(__name__, 'a2_')
    return
