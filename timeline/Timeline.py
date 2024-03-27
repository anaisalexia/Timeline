import pandas as pd
from plotly import express as px
from plotly import graph_objects as go
import random

## Timeline

def transforme_date(x):
    """Transform the date from dd/mm/yyyy to mm-yyyy

    Args:
        x (str): date. Format dd/mm/yyyy

    Returns:
        date (str): date. Format mm-yyyy
    """
    split_list = x.split('/')
    if len(split_list)>2:
        date = split_list[2] + '-' + split_list[1]
    else:
        date = split_list[1] + '-' + split_list[0]
        
    return date


def split_line(line,max_len=20):
    """Insert html linebreaks <br> every x words, x a chosen number.

    Args:
        line (str): a paragraph with no line break
        max_len (int, optional): number of words before a linebreak is inserted. Defaults to 20.

    Returns:
        newline (str): return the pragraph with linebreaks
    """
    line_split = line.split(" ")
    new_line = ''
    length = 0
    for w in line_split:
        length += len(w)
        if length < max_len:
            new_line += w
            new_line += ' '
        else:
            length = 0 
            new_line += '<br>'
            new_line += w
            new_line += ' '
            
    return new_line

# open the data
date = pd.read_csv('chronologie2.tsv',sep='\t',header=None)

date = date.rename(columns={1:'event',0:'date',2:'keywords'})
date = date.tail(-1)

#transform the date
date['date'] = date['date'].apply(lambda x : transforme_date(x))

# group the events that have the sale date
date_ev = date.groupby('date', as_index = False)['event'].apply("\n".join)
date_k = date.groupby('date', as_index = False)['keywords'].apply("\n".join)
date = date_ev
date['keywords'] = date_k['keywords']
#abscissa of the date on the time line
date['y'] = 0

list_id = []
nb = 3
id = 1

#gives the ordinate of the date, it alternates between above and under the time line
for  i in range(int(date.shape[0]/2)):
    if id >= nb:
        id = 1
    id2 = [id,id-nb]
    id += 1
    
    list_id += id2

# add last one coordinate for odd set of date
if date.shape[0]%2 == 1:
    if id >= nb:
        id = 1
    list_id += [id]

# ordinate of the date
date['y1'] = list_id
date['event'] = date['event'].apply(lambda x: split_line(x))
fig = go.Figure()
fig.add_trace(go.Scatter( x=date['date'],y=date['y'],mode="lines",name=""))

fig.add_trace(go.Scatter( x=date['date'],y=date['y1'],text=date['event'],mode="markers",name="",
                         hovertemplate='<br><b>Date:</b> %{x}<br><b>Event:</b> %{text}<br>'))


for x,y,ann in list(zip(date['date'],date['y1'],date['keywords'])):
    supp = 0.3
    if y > 0:
        add = supp
    else:
        add = -supp
    fig.add_annotation(text=split_line(ann,max_len=10),
                #   xref="paper", yref="paper",
                  x=x, y=y+add, showarrow=False,
                  textangle=-0,
                  font_size = 7
                  )



fig.add_trace(go.Bar(x=date['date'],y=date['y1']))

fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=0.2, opacity=1)

fig.update_layout(
    hoverlabel=dict(
        bgcolor="rgb(255,255,224)",
        font_size=12,
        # font_family=""
    )
)



fig.update_layout(showlegend=False,hovermode='closest')
fig.update_yaxes(visible=False)

fig.update_layout(title = "The evolution of women's rights in France: a chronology",
)

fig.show()

