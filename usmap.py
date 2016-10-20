import plotly.plotly as py
import pandas as pd


def mapplot(location,num,title_str,sub_str):
    #scl = [[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], \
           #[0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
    #scl = [[0, 'rgb(252,187,161)'],  [0.2, 'rgb(239,59,44)'], [1, 'rgb(165,15,21)']]
    scl = [[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], \
          [0.3333333333333333, 'rgb(253,174,97)'], [0.45, 'rgb(171,217,233)'],\
          [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]

    data = [dict(
        type='choropleth',
        colorscale=scl,
        autocolorscale=False,
        locations=location,
        z=num.astype(float),
        locationmode='USA-states',
        marker=dict(
            line=dict(
                color='rgb(255,255,255)',
                width=2
            )
        ),
        colorbar=dict(
            title=sub_str
        )
    )]

    layout = dict(
        title=title_str,
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
        ),
    )

    fig = dict(data=data, layout=layout)
    url = py.plot(fig, validate=False, filename='us_map')
    return url

if __name__ == '__main__':
    df1 = pd.read_csv('storenumber.csv')
    location1 = df1['States']
    num1 = df1['StoreNumber']
    #mapplot(location1, num1, 'Nike Store Distribution','Store Number')

    df2 = pd.read_csv('sentimentscore.csv')
    location2 = df2['States']
    num2 = df2['Sentiment']
    mapplot(location2, num2,'Sentiment Score','Score Number')


