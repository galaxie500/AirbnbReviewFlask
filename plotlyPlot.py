import plotly.graph_objs as go


# set up for plotly
def plotlyPlot(ts):
    r = go.Scatter(x=ts.index, y=ts.values,
                   line=go.scatter.Line(color='red', width = 1), opacity=0.8,
                   name='Reviews', text=[f'Reviews: {x}' for x in ts.values])
    # Create a layout with a rangeselector and rangeslider on the xaxis
    layout = go.Layout(height=600, width=900, font=dict(size=18),
                       title='Number of reviews over time(with Range selector)',
                       xaxis=dict(title='Date',
                                            # Range selector with buttons
                                             rangeselector=dict(
                                                 # Buttons for selecting time scale
                                                 buttons=list([
                                                     # 4 month
                                                     dict(count=4,
                                                          label='4m',
                                                          step='month',
                                                          stepmode='backward'),
                                                     # 1 month
                                                     dict(count=1,
                                                          label='1m',
                                                          step='month',
                                                          stepmode='backward'),
                                                     # 1 week
                                                     dict(count=7,
                                                          label='1w',
                                                          step='day',
                                                          stepmode='todate'),
                                                     # 1 day
                                                     dict(count=1,
                                                          label='1d',
                                                          step='day',
                                                          stepmode='todate'),
                                                     # Entire scale
                                                     dict(step='all')
                                                 ])
                                             ),
                                             # Sliding for selecting time window
                                             rangeslider=dict(visible=True),
                                             # Type of xaxis
                                             type='date'),
                       # yaxis is unchanged
                       yaxis=dict(title='Number of reviews')
                       )
    # Create the figure and display
    fig = go.Figure(data=[r], layout=layout)
    return fig
