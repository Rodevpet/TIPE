import plotly.graph_objs as go
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sympy import *

DROITE = 0
AFFINE = 1
POLYNOMINIALE = 2
EXPONENTIEL = 3
INVEXPONENTIEL = 4

class ChemPlot:
    def __init__(self,Title,x_axe,y_axe,Title_Legend):
        """"
        __init__ (self,data,sep,axe_x,axe_y) : es
        """
        Data = []
        model = []
        self.list_plot = []
        self.fig = go.Figure()
        self.fig.update_layout(
            title=Title,
            legend_title=Title_Legend,
            yaxis=dict(
                title=y_axe
            ),
            xaxis=dict(
                title=x_axe,
            )
    )
        self.fig.update_xaxes(gridcolor='black', griddash='solid', minor_griddash="dot",minor_gridcolor='gray')
        self.fig.update_yaxes(gridcolor='black', griddash='solid', minor_griddash="dot",minor_gridcolor='gray')
        self.fig.update_layout(template="plotly_white")
    def axes_ratio (self):
        self.fig.update_xaxes(
        scaleanchor = "x",
        scaleratio = 1,
        )
        self.fig.update_yaxes(
        scaleanchor = "y",
        scaleratio = 1,
        )
        self.fig.update_layout(
            width = 800,
            height = 800,
        )
    def add_plot (self,data,sep,legend,symbole="lines",color="rgb(0,0,0)"):
        if (type(data) is str):
            csv_data = pd.read_csv(data,sep=sep)
            numpy_data = csv_data.to_numpy(copy=True,dtype=float)
            self.Data = [numpy_data[...,0],numpy_data[...,1]]
        if (type(data) is list):
            self.Data=[np.array(data[0]),np.array(data[1])]
        if (type(data) is type(np.array(0))):
            self.Data = data
        if (symbole=="lines"):
            if (len(data[1])>10000):
                self.fig.add_trace(go.Scatter(
                    name=legend,
                    x = self.Data[0], # non-uniform distribution
                    y = self.Data[1], # zoom to see more points at the center
                    mode='lines',
                    line=dict(color=color),opacity=0.5,))
            else :
                self.fig.add_trace(go.Scatter(name=legend,x=self.Data[0], y=self.Data[1],mode='lines',line=dict(color=color)))
        else:
            if (len(data[1])>10000):
                 self.fig.add_trace(go.Scattergl(
                    name=legend,
                    x = self.Data[0], # non-uniform distribution
                    y = self.Data[1], # zoom to see more points at the center
                    mode='markers',
                    marker=dict(color=color)))
            else :
                self.fig.add_trace(go.Scatter(name=legend,x=self.Data[0], y=self.Data[1],mode='markers',marker=dict(
                    symbol=symbole,
                    color=color,
                )))
        self.list_plot.append((self.Data[0],self.Data[1]))

    def add_point(self, name, coord,color="rgb(0,0,0"):
        self.fig.add_trace(
            go.Scatter(x=[coord[0]],
                       y=[coord[1]],
                       mode='markers+text',
                       text=[name],
                       textposition="bottom center",
                       marker=dict(size=10, symbol='x',color=color)))
    def change_to_polare (self):
        for i in self.list_plot :
            self.fig = go.Figure(data=
            go.Scatterpolar(
                r = i[0],
                theta = i[1],
                mode = 'markers',
            ))
    def fit (self,type_fit,precision):
        newData = self.Data[0].tolist()
        Y = []
        X = self.Data[0]
        self.model = None
        if (type_fit==0):
            coef = (curve_fit(lambda x,m: m*x,  self.Data[0],  self.Data[1])[0])
            for i in range (0,int(newData[-1]/precision)):
                for x in range (i,i+int((1/precision))):
                    Y.append(coef[0]*i*precision)
                    X.append(i*precision)
            self.model = np.array(Y)
        elif (type_fit==INVEXPONENTIEL):
            coef = (curve_fit(lambda x,a,k: a*np.exp(-k*x),  self.Data[0],  self.Data[1])[0])
            for i in range (0,int(newData[-1]/precision)):
                for x in range (i,i+int((1/precision))):
                    Y.append(coef[0]*np.exp(-coef[1]*i*precision))
                    X.append(i*precision)
            self.model = np.array(Y)
        elif (type_fit==1):
            coef = (curve_fit(lambda x,m,p: m*x+p,  self.Data[0],  self.Data[1])[0],)
            self.model = np.array([coef[0][0]*i+coef[0][1] for i in self.Data[0]],)
        self.fig.add_trace(go.Scatter(name=r"Modèle",x=np.array(X),y=self.model))

    def addVector(self, name, point, coord,color=(255,255,255)):
        self.fig.add_annotation(ax=point[0],
                                ay=point[1],
                                xref="x",
                                yref="y",
                                showarrow=True,
                                axref="x",
                                ayref='y',
                                x=point[0] + coord[0],
                                y=point[1] + coord[1],
                                arrowhead=3,
                                arrowwidth=1.5,
                                arrowcolor='rgb'+str(color))
        self.fig.add_annotation(text=name,
                                x=point[0] + (coord[0] / 2) + 0.2,
                                y=point[1] + (coord[1] / 2) + 0.2,
                                showarrow=False)
    def show(self):
        self.fig.show()

    def show_png(self):
        self.fig.show(renderer="svg")

    def show_browser(self):
        self.fig.show(renderer="browser")
#%%
