import plotly.graph_objs as go
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.io as pio
import plotly.offline as py
import colorsys


class DrawShape:
    """
    Methods
    ------
    __init__(self,minx,maxx,miny,maxy,Title)
        Initialise le graphique avec les valeurs minimales et maximales des coordonnées

    add_point (self,name,x,y)
        Permet d'ajouter un point aux coordonnées x d'abscisse et y d'ordonnée
    """

    def __init__(self, minx: int, maxx: int, miny: int, maxy: int, Title: str):
        """
        Parameters :
        ----------
        :param minx : int
            Valeur minimale de l'axe des abscisses
        :param maxx : int
            Valeur maximale de l'axe des abscisses
        :param miny : int
            Valeur minimale de l'axe des ordonnées
        :param maxy : int
            Valeur maximale de l'axe des ordonnées
        :param Title:
            Titre donné au graphique
        """
        self.min_x = minx
        self.max_x = maxx
        self.min_y = miny
        self.max_y = maxy
        self.fig = go.Figure()
        self.fig.update_layout(
            title=Title,
            yaxis_range=[miny, maxy],
            xaxis_range=[minx, maxx],
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0)),
        self.fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1
        )
        pd.options.plotting.backend = "plotly"

    def HideLegend(self):
        self.fig.update(layout_showlegend=False)

    def addDoubleFleche(self, name, coord):
        x = coord[1][0] - coord[0][0]
        y = coord[1][1] - coord[0][1]
        self.addVector(name, coord[0], (x, y))
        self.addVector(name, coord[1], (-x, -y))

    def addDroite(self, nom, coord, debut=False, fin=False, color="#000000"):
        """
       Parameters :
       ----------
       :param nom : str
           nom de la droite
       :param coord : list
           Coordonné de la droite
       :param début : Bool
           La droite a un début ?
       :param fin : Bool
           La droite a une fin ?
       :param color : String
           Couleur HTML de la droite
       """
        x1 = coord[0][0]
        y1 = coord[0][1]
        x2 = coord[1][0]
        y2 = coord[1][1]
        if debut:
            _debut_ = int(self.min_x)
        if fin:
            _fin_ = int(self.max_x)
        # Définition de la pente et de l'ordonnée à l'origine de la droite
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        # Définition de l'équation de la droite
        eq_droite = f'y = {a:.2f}x + {b:.2f}'

        # Définition des abscisses pour tracer la droite
        x = [_debut_, _fin_]

        # Calcul des ordonnées correspondantes
        y = [a * xi + b for xi in x]
        color = 'rgb' + str(self.html_to_rgba(color))
        # Ajout de la droite à la figure
        self.fig.add_trace(go.Scatter(x=x, y=y, marker_color=color, mode='lines', name=nom))

    def addParallele(self, droite, coord, name="", color="#000000", debut="False", fin="False"):
        if (debut == "False"):
            debut = int(self.min_x)
        if (fin == "False"):
            fin = int(self.max_x)
        x1 = droite[0][0]
        y1 = droite[0][1]
        x2 = droite[1][0]
        y2 = droite[1][1]

        dx = x2 - x1
        dy = y2 - y1
        theta = np.arctan2(dy, dx)
        x3 = coord[0]
        y3 = coord[1] + (x3 - coord[0]) * dy / dx

        xDebut = debut
        yDebut = coord[1] + (xDebut - coord[0]) * dy / dx

        xFin = fin
        yFin = coord[1] + (xFin - coord[0]) * dy / dx

        color = 'rgb' + str(self.html_to_rgba(color))
        self.fig.add_trace(
            go.Scatter(x=[xDebut, x3, xFin], y=[yDebut, y3, yFin], marker_color=color, mode='lines', name=name))

    def html_to_rgba(self, html_color):
        r, g, b = tuple(int(html_color[i:i + 2], 16) for i in (1, 3, 5))
        r, g, b = r / 255, g / 255, b / 255
        return tuple(map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*colorsys.rgb_to_hsv(r, g, b)) + (1,)))

    def addPoint(self, name, coord):
        self.fig.add_trace(
            go.Scatter(x=[coord[0]],
                       y=[coord[1]],
                       mode='markers+text',
                       text=[name],
                       textposition="bottom center",
                       marker=dict(size=10, symbol='x')))

    def addPolyline(self, name, coord, color="#000000", pointille=False):
        X = []
        Y = []
        for i in range(len(coord) - 1):
            x = coord[i][0]
            y = coord[i][1]
            X.append(x)
            Y.append(y)
            x_1 = coord[i + 1][0]
            y_1 = coord[i + 1][1]
            if (pointille == True):
                self.fig.add_shape(type="line",
                                   x0=x,
                                   y0=y,
                                   x1=x_1,
                                   y1=y_1,
                                   line=dict(
                                       color=color,
                                       width=2,
                                       dash="dot",
                                   ))
            else:
                self.fig.add_shape(type="line",
                                   x0=x,
                                   y0=y,
                                   x1=x_1,
                                   y1=y_1,
                                   line=dict(
                                       color=color,
                                       width=2
                                   ))
        X.append(coord[-1][0])
        Y.append(coord[-1][1])
        xmin = sorted(X)[0]
        xmax = sorted(X)[-1]
        ymin = sorted(Y)[0]
        ymax = sorted(Y)[-1]
        mid = ((xmin + (xmax - xmin) / 2), ymin + (ymax - ymin) / 2)
        self.fig.add_annotation(x=mid[0], y=mid[1], text=name, showarrow=False)

    def addText(self, name, coord):
        self.fig.add_annotation(text=name,
                                x=coord[0],
                                y=coord[1],
                                showarrow=False)

    def addPolygone(self, name, coord):
        X = []
        Y = []
        for i in coord:
            X.append(i[0])
            Y.append(i[1])
        self.fig.add_trace(go.Scatter(
            x=X,
            y=Y,
            fill='toself',
        ))
        xmin = sorted(X)[0]
        xmax = sorted(X)[-1]
        ymin = sorted(Y)[0]
        ymax = sorted(Y)[-1]
        mid = ((xmin + (xmax - xmin) / 2), ymin + (ymax - ymin) / 2)
        self.fig.add_annotation(x=mid[0], y=mid[1], text=name, showarrow=False)

    def addVector(self, name, point, coord):
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
                                arrowcolor='rgb(255,51,0)')
        self.fig.add_annotation(text=name,
                                x=point[0] + (coord[0] / 2) + 0.2,
                                y=point[1] + (coord[1] / 2) + 0.2,
                                showarrow=False)

    def addFunction(self, func, Domain, precision):
        X = np.arange(Domain[0], Domain[1], precision)
        Y = []
        for x in X:
            Y.append(func(x))
        self.fig.add_trace(go.Scatter(x=X, y=Y, mode='lines'))

    def ellipseArc(self,
                   x_center=0,
                   y_center=0,
                   a=1,
                   b=1,
                   start_angle=0,
                   end_angle=2 * np.pi,
                   N=100,
                   closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    def addCircle(self, name, r, coord,fg_color="#000000",bg_color="#000000",txt_color="#FFFFFF"):
        self.fig.add_shape(
            type="path",
            path=self.ellipseArc(coord[0], coord[1], a=r, b=r),
            line_color=fg_color,
            fillcolor=bg_color,
        )
        self.fig.add_annotation(xref="x",
                                yref="y",
                                x=coord[0],
                                y=coord[1],
                                text=name,
                                font=dict(color=txt_color),
                                showarrow=False)

    def addAngle(self, coord, angle, distance, name):
        mid = angle[0] + (angle[1] - angle[0]) / 2
        self.fig.add_shape(
            type="path",
            path=self.ellipseArc(x_center=coord[0],
                                 y_center=coord[1],
                                 a=distance,
                                 b=distance,
                                 start_angle=angle[0],
                                 end_angle=angle[1]),
            line_color="RoyalBlue",
        )
        self.fig.add_annotation(x=coord[0] + distance * np.cos(mid),
                                y=coord[1] + distance * np.sin(mid),
                                text=name,
                                showarrow=False)

    def showBrowser(self):
        self.fig.show(renderer="browser")

    def showSvg(self):
        self.fig.show(renderer="svg")

    def showPng(self):
        png_renderer = pio.renderers["png"]
        png_renderer.scale = 6
        pio.renderers.default = "png"
        self.fig.show()

    def show(self):
        """tab = ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
         'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
         'cocalc', 'json', 'png', 'jpeg', 'jpg', 'svg',
         'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
         'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']
        for i in tab :
            self.fig.show(renderer=i)"""
        self.fig.show()

    def get(self):
        return self.fig
