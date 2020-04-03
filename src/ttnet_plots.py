"""
Plotting functions related to the Time-Triggered Wireless project.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import src.colors as colors
from src.ttnet_model import *

# Series list
serie_1 = {'label' : 'serie1',
           'node_list' : [1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15, 16,
                          17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 32, 33]}
serie_2 = {'label' : 'serie2',
           'node_list' : [1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15, 16,
                          17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 32, 33]}
serie_3 = {'label' : 'serie3',
           'node_list' : [1, 2, 3, 4, 6, 8, 10, 11, 13, 15, 16, 17,
                          18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33]}

linewidth_pt = 384
linewidth_px = 512 # https://www.ninjaunits.com/converters/pixels/points-pixels/

# ==============================================================================
def plot_inheritance_results():

    df = pd.read_csv('data_processed/inheritance_evaluation.csv', delimiter=',')

    fig = go.Figure()

    inheritance_types = [
            {'value':0,},
            {'value':1,
             'name':'No inheritance',
             'color':colors.light_orange, },
            {'value':2,
             'name':'Minimal inheritance',
             'color':colors.orange, },
            {'value':3,
             'name':'Full inheritance',
             'color':colors.dark_orange, },
        ]

    for inheritance in df.inheritance_type.unique():
        data = []
        for mode in df.modeID.unique():
            nb_round = df.loc[(df.modeID == mode)
                                & (df.inheritance_type == inheritance)].nb_rounds_norm
            data.append(nb_round.values[0])


        series = go.Bar(
            name=inheritance_types[inheritance]['name'],
            x=df.modeID.unique(),
            y=data,
            marker_color=inheritance_types[inheritance]['color'],
            text=[str(int(i)) for i in data],
            textposition='outside',
            hoverinfo="none"
        )
        fig.add_trace(series)

    # y axis title
    ytitle = go.layout.Annotation(
            x=0,
            y=1.20,
            xref="paper",
            yref="paper",
            text="Number of rounds scheduled",
            showarrow=False,
            xanchor='left'
        )

    fig.update_layout(
        xaxis=dict(
            title='Operation modes'
        ),
        legend=dict(
            x=0,
            y=1.0,
            orientation='h'
        ),
        barmode='group',
        bargap=0.3,     # gap between bars of adjacent location coordinates.
        bargroupgap=0.1, # gap between bars of the same location coordinate.
        annotations=[ytitle]
    );
    return fig


# ==============================================================================
def plot_protocol_overhead():
    # Tround = f(B,H,L=16,N=2)
    L = 16
    N = 2
    H = [1,2,4,8]
    B = [
            {'value':1,
             'color':colors.darker_orange, },
            {'value':2,
             'color':colors.dark_orange, },
            {'value':5,
             'color':colors.orange, },
            {'value':10,
             'color':colors.light_orange, },
        ]

    fig = go.Figure()
    categories = []
    for h in H:
        categories.append('H = %i' % h)

    for b in B:
        data = []
        for h in H:
            overhead = compute_T_beacon(h,N)/compute_T_round(h,N,L,b['value'])*100
            data.append(overhead)

        series = go.Bar(
            name='B = %s' % str(b['value']),
            x=categories,
            y=data,
            marker_color=b['color'],
            text=[str(int(i)) for i in data],
            textposition='outside',
            hoverinfo="none"
        )
        fig.add_trace(series)


    # y axis title
    ytitle = go.layout.Annotation(
            x=0,
            y=1.20,
            xref="paper",
            yref="paper",
            text="Protocol overhead [%]",
            showarrow=False,
            xanchor='left'
        )

    fig.update_layout(
        xaxis=dict(
            title='Network diameter H [hops]'
        ),
        legend=dict(
            x=0,
            y=1.0,
            orientation='h'
        ),
        barmode='group',
        bargap=0.15,     # gap between bars of adjacent location coordinates.
        bargroupgap=0.1, # gap between bars of the same location coordinate.
        annotations=[ytitle]
    );
    return fig


# ==============================================================================
def plot_round_length(
        L=16,
        N=2,
        Hs=[1,2,4,8],
        Bs=[1,2,5,10],
        ):
    # Tround = f(B,H,L=16,N=2)
    H = Hs
    B = [
            {'value':1,
             'color':colors.darker_orange, },
            {'value':2,
             'color':colors.dark_orange, },
            {'value':5,
             'color':colors.orange, },
            {'value':10,
             'color':colors.light_orange, },
        ]
    for i in range(4):
        B[i]['value']=Bs[i]

    fig = go.Figure()
    categories = []
    for h in H:
        categories.append('H = %i' % h)

    for b in B:
        data = []
        for h in H:
            data.append(compute_T_round(h,N,L,b['value']))

        series = go.Bar(
            name='B = %s' % str(b['value']),
            x=categories,
            y=data,
            marker_color=b['color'],
            text=[str(int(i)) for i in data],
            textposition='outside',
            hoverinfo="none"
        )
        fig.add_trace(series)


    # y axis title
    ytitle = go.layout.Annotation(
            x=0,
            y=1.20,
            xref="paper",
            yref="paper",
            text="Round length Tr [ms]",
            showarrow=False,
            xanchor='left'
        )

    fig.update_layout(
        xaxis=dict(
            title='Network diameter H [hops]'
        ),
        legend=dict(
            x=0,
            y=1.0,
            orientation='h'
        ),
        barmode='group',
        bargap=0.15,     # gap between bars of adjacent location coordinates.
        bargroupgap=0.1, # gap between bars of the same location coordinate.
        annotations=[ytitle]
    );
    return fig

# ==============================================================================
def plot_series(
        df,
        custom_layout={},
        save=False,
        plot_path='.',
        prefix='',
        sample=None
        ):

    Bs = df.B_n_slots.unique()
    Ls = df.L_payload_size.unique()
    Hs = df.H.unique()
    Ns = df.N.unique()
    if sample is not None:
        if 'B' in sample:
            Bs = [sample['B']]
        if 'L' in sample:
            Ls = [sample['L']]

    for H in Hs:
        for N in Ns:
            for B in Bs:
                for L in Ls:
                    x = (df.loc[(df['B_n_slots']==B) &
                                (df['L_payload_size']==L) &
                                (df['H']==H) &
                                (df['N']==N)]).dropna()

                    print("B = %u, L = %u, H = %u, N = %u" % (B,L,H,N))

                    print("  T_round")
                    x_data = x.T_round/1000
                    x_model = compute_T_round(H,N,L,B) # in ms
                    fig = TTW_hist(x_data,0,x_model)
                    fig.update_layout({"xaxis":{'title':'Round length Tr [ms]'}})
                    fig.update_layout(custom_layout)
                    fig.show()
                    plot_filename = "%sT_round_H%u_N%u_L%u_B%u.pdf" % (prefix,H,N,L,B)
                    if save:
                        fig.write_image(str(plot_path/plot_filename))

                    print("  T_on_round")
                    x_data = x.T_on_round/1000
                    x_model = compute_T_on_round(H,N,L,B) # in ms
                    fig = TTW_hist(x_data,0,x_model)
                    fig.update_layout({"xaxis":{'title':'Radio-on time in a round [ms]'}})
                    fig.update_layout(custom_layout)
                    fig.show()
                    plot_filename = "%sT_on_round_H%u_N%u_L%u_B%u.pdf" % (prefix,H,N,L,B)
                    if save:
                        fig.write_image(str(plot_path/plot_filename))


# ==============================================================================
def plot_energy_savings_model(
        H=4,
        N=2,
        Bs=np.arange(1,35),
        Ls=[8,16,64]
        ):

    fig = go.Figure()

    for l in Ls:
        data = [100*compute_energy_saving(H,N,l,b) for b in Bs]
        series = go.Scatter(
            name='L = %sB' % l,
            x=Bs,
            y=data,
            line={'width':3},
            mode='lines',
        )
        fig.add_trace(series)

    # y axis title
    ytitle = go.layout.Annotation(
            x=0,
            y=1.20,
            xref="paper",
            yref="paper",
            text="Energy savings E [%]",
            showarrow=False,
            xanchor='left'
        )

    fig.update_layout(
        xaxis=dict(
            title='Number of slots per round B [.]'
        ),
        legend=dict(
            x=0.05,
            y=1.0,
            orientation='h'
        ),
        annotations=[ytitle],
    )
    return fig

# ==============================================================================
def plot_energy_savings(KPIs=None):

    # Plot first the model data
    H = 4
    N = 2
    B = np.arange(1,35)
    L = [
            {'value':8,
             'color':colors.darker_orange, },
            {'value':16,
             'color':colors.dark_orange, },
            {'value':64,
             'color':colors.orange, },
        ]

    fig = go.Figure()

    for l in L:
        data = [100*compute_energy_saving(H,N,l['value'],b) for b in B]
        series = go.Scatter(
            name='L = %sB' % str(l['value']),
            x=B,
            y=data,
            line={'color':l['color'],
                  'width':3},
            mode='lines',
        )
        fig.add_trace(series)

    # y axis title
    ytitle = go.layout.Annotation(
            x=0,
            y=1.20,
            xref="paper",
            yref="paper",
            text="Energy savings E [%]",
            showarrow=False,
            xanchor='left'
        )

    fig.update_layout(
        xaxis=dict(
            title='Number of slots per round B [.]'
        ),
        legend=dict(
            x=0.05,
            y=1.0,
            orientation='h'
        ),
        annotations=[ytitle],
    )

    if KPIs is not None:
        KPI_legend = go.Scatter(
            name='KPIs',
            x=[np.nan],
            y=[np.nan],
            marker={'color':'black',
                    'symbol':'diamond-open',
                    'size':8},
            mode='markers',
        )
        fig.add_trace(KPI_legend)

        # Plot the experimental data (KPIs)
        for l in KPIs:
            if l['L'] == 8:
                color = L[0]['color']
            if l['L'] == 16:
                color = L[1]['color']
            if l['L'] == 64:
                color = L[2]['color']

            KPI = go.Scatter(
                name='KPI, %s' % str(l['series']),
                x=l['data']['B'],
                y=l['data']['KPI'],
                showlegend=False,
                marker={'color':color,
                        'symbol':'diamond-open',
                        'size':8},
                mode='markers',
            )
            fig.add_trace(KPI)


    return fig

# ==============================================================================
def TTW_hist(x, KPI, max_model):

    # Vertical positioning of annotations
    top_annot = 0.95
    second_annot = 0.5


    max_observed = max(x)

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=x,
            histnorm='percent',
            # nbinsx=50,
            marker_color=colors.light_orange,
        )
    )

    notes = []
    shapes = []

    # Analytical bound
    note = go.layout.Annotation(
            x=max_model,
            y=top_annot,
            xref="x",
            yref="paper",
            text="Model",
            showarrow=False,
            xanchor='right',
            xshift=-10
        )
    notes.append(note)
    line = go.layout.Shape(
            type="line",
            xref="x",
            x0=max_model,
            x1=max_model,
            yref="paper",
            y0=0,
            y1=top_annot,
            line=dict(
                color=colors.red,
                width=3,
            )
        )
    shapes.append(line)

    # Reached bound
    note = go.layout.Annotation(
            x=max_observed,
            y=second_annot,
            xref="x",
            yref="paper",
            text=("%2.2f ms" % max_observed),
            showarrow=False,
            xanchor='left',
            xshift=10,
            yshift=-10
        )
    notes.append(note)
    line = go.layout.Shape(
            type="line",
            xref="x",
            x0=max_observed,
            x1=max_observed,
            yref="paper",
            y0=0,
            y1=second_annot,
            line=dict(
                color=colors.red,
                width=3,
                dash="dot",
            )
        )
    shapes.append(line)

    ytitle = go.layout.Annotation(
            x=0,
            y=1.25,
            xref="paper",
            yref="paper",
            text="Number of samples [%]",
            showarrow=False,
            xanchor='left',
        )
    notes.append(ytitle)

    # Default Layout
    default_layout = go.Layout(
        annotations=notes,
        shapes=shapes,
        )
    fig.update_layout(default_layout)

    return fig
