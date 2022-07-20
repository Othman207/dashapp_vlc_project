from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import time
import datetime
import os
import dash_alternative_viz as dav
import dash_auth
from app import app



dataset2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/pete.xlsx')

df1 = pd.read_excel(dataset2,"Uti2")

df2 = pd.read_excel(dataset2,"DVDMT")

df3 = pd.read_excel(dataset2,"Logistics Costs",usecols=['Site','Annual Transportation Cost','Transport CPD'])
df8 = pd.read_excel(dataset2,"Logistics Costs",usecols=['District','Site','Annual Transportation Cost','Transport CPD'])
df9 = df8.groupby(by=['District']).mean().reset_index()
#df1 = pd.read_excel(dataset,"Uti2")

#df2 = pd.read_excel(dataset,"DVDMT")

#df3 = pd.read_excel(dataset,"Logistics Costs",usecols=['Site','Annual Transportation Cost','Transport CPD'])


#df2.replace('-',np.nan,inplace=True)
# dataset = pd.read_excel("pete.xlsx")
#
# df1 = pd.read_excel("pete.xlsx","Uti2")
#
# df2 = pd.read_excel("pete.xlsx","DVDMT")

# df2.rename(columns={'VPO_Unopened vial wastage_VVM status':'OPV_Unopened vial wastage_VVM status',
#                         'VPI_Unopened vial wastage_VVM status':'IPV_Unopened vial wastage_VVM status',
#                         'Pneumo_Unopened vial wastage_VVM status':'PCV_Unopened vial wastage_VVM status',
#                         'VAR_Unopened vial wastage_VVM status':'MV_Unopened vial wastage_VVM status',
#                         'VAA_Unopened vial wastage_VVM status':'YF_Unopened vial wastage_VVM status',
#                         'VPH_Unopened vial wastage_VVM status':'HPV_Unopened vial wastage_VVM status',
#                         'VPO_Unopened vial wastage_Freezing':'OPV_Unopened vial wastage_Freezing',
#                         'VPI_Unopened vial wastage_Freezing':'IPV_Unopened vial wastage_Freezing',
#                         'Pneumo_Unopened vial wastage_Freezing':'PCV_Unopened vial wastage_Freezing',
#                         'VAR_Unopened vial wastage_Freezing':'MV_Unopened vial wastage_Freezing',
#                         'VAA_Unopened vial wastage_Freezing':'YF_Unopened vial wastage_Freezing',
#                         'VPH_Unopened vial wastage_Freezing':'HPV_Unopened vial wastage_Freezing'},
# inplace=True)

#df3 = pd.read_excel("pete.xlsx","Logistics Costs",usecols=['Site','Annual Transportation Cost','Transport CPD'])


#df2.replace('-',np.nan,inplace=True)

df1['Utilization'] = 100 * df1['Utilization']

df1['Monthly reports']= df1['Monthly reports'].apply(lambda x: x.strftime("%b-%y"))
df2['Monthly reports']= df2['Monthly reports'].apply(lambda x: x.strftime("%b-%y"))

# df1['Monthly reports'] = df1['Monthly reports'].astype('str')
#
# df1['Monthly reports'] = df1['Monthly reports'].str[:-3]
#
# for i in range(len(df1)):
#     df1['Monthly reports'][i] = datetime.datetime.strptime(df1['Monthly reports'][i], "%Y-%m")
#
#
#
# for i in range(len(df1)):
#     df1['Monthly reports'][i] = pd.to_datetime(df1['Monthly reports'][i]).strftime("%b-%y")
#
#
#
# df2['Monthly reports'] = df2['Monthly reports'].astype('str')
#
# df2['Monthly reports'] = df2['Monthly reports'].str[:-3]
#
# for i in range(len(df2)):
#     df2['Monthly reports'][i] = datetime.datetime.strptime(df2['Monthly reports'][i], "%Y-%m")
#
#
#
# for i in range(len(df2)):
#     df2['Monthly reports'][i] = pd.to_datetime(df2['Monthly reports'][i]).strftime("%b-%y")



total_volume = df1.groupby(by=['Districts']).sum()

# total_volume['lat'] = total_volume.index.map(district_lat)
# total_volume['lon'] = total_volume.index.map(district_lng)

avg_volume_district = df1.groupby(by=['Districts']).mean()



dfpt= pd.pivot_table(df1, values='Number of Trips',index=['Country', 'Monthly reports'],aggfunc=np.sum)
dfpt.reset_index(inplace=True)
dfpt2 = dfpt.iloc[pd.to_datetime(dfpt['Monthly reports'], format='%b-%y').argsort()]
total_trips_date = dfpt2.groupby(by=['Monthly reports'],sort=False).sum()

total_vacc_sessions = df2.groupby(by=['District']).sum()

total_vacc_sessions_date = df2.groupby(by=['Monthly reports'],sort=False).sum()


vvm_cols = [col for col in df2.columns if 'VVM status' in col]


freezing_cols = [col for col in df2.columns if 'wastage_Freezing' in col]

wastage_cols = [col for col in df2.columns if '_Unopened vial wastage' in col]

total_vvm_change = total_vacc_sessions_date[vvm_cols]

total_freezing = total_vacc_sessions_date[freezing_cols]

total_wastage = total_vacc_sessions_date[wastage_cols]

total_vvm_change_by_vacc = total_vvm_change.T

total_vvm_change_by_vacc.index = total_vvm_change_by_vacc.index.str.replace('_Unopened vial wastage_VVM status','')

total_wastage_by_date = total_wastage.sum(axis=1).to_frame().rename(columns={0:'Total Wastage'})


total_freezing_by_vacc = total_freezing.T

total_freezing_by_vacc.index = total_freezing_by_vacc.index.str.replace('_Unopened vial wastage_Freezing','')


total_vvm_change = total_vvm_change.sum(axis=1).to_frame().rename(columns={0:'Total VVM Change'})


total_freezing = total_freezing.sum(axis=1).to_frame().rename(columns={0:'Total Freezing'})


df_wastage_by_reason = pd.concat([total_vvm_change,total_freezing],axis=1)

total_vvm_change_by_vacc = total_vvm_change_by_vacc.sum(axis=1).to_frame().rename(columns={0:'Total VVM Change'})


total_vvm_change_by_vacc.sort_values(by='Total VVM Change',inplace=True)

total_freezing_by_vacc = total_freezing_by_vacc.sum(axis=1).to_frame().rename(columns={0:'Total Freezing'})


total_freezing_by_vacc.sort_values(by='Total Freezing',inplace=True)



avg_volume = avg_volume_district['Total Volume (L)'].sum()
avg_util = avg_volume_district['Utilization'].mean()
baseline_annual_tp_cost = df3['Annual Transportation Cost'].sum()

avg_tcpd = df3["Transport CPD"].mean().round(decimals=3)


district_names = []
volume_data = []
wastage_data = []

vvm_vacc = []

freezing_vacc = []

map_data2 = []


# for district in total_volume.index:
#     volume_data.append([district,total_volume['Total Volume (L)'][district]])
#     map_data2.append({'name':district,'lat':total_volume['lat'][district],'lon':total_volume['lon'][district],'volume':total_volume['Total Volume (L)'][district]})

for district in df1['Districts'].unique():
    district_names.append({'label':district,'value':district})

for vaccine in total_vvm_change_by_vacc.index:
    vvm_vacc.append([vaccine,total_vvm_change_by_vacc['Total VVM Change'][vaccine]])

for vaccine in total_freezing_by_vacc.index:
    freezing_vacc.append([vaccine,total_freezing_by_vacc['Total Freezing'][vaccine]])

for date in total_wastage_by_date.index:
    wastage_data.append([date,total_wastage_by_date['Total Wastage'][date]])



df3 = df3.loc[df3['Site'].isin(total_volume.index.tolist())]

df3 = df3.drop_duplicates(subset=['Site'])

df3['Transport CPD'] = df3['Transport CPD'].round(decimals=1)


options_1 = {
    'chart': {
        'type': 'bar',
        'height':500
    },
    'title': {
        'text': 'Total Volume (liters) of Vaccines Received by Health Facilities (2021)'
    },
    'xAxis': {
        'type': 'category',
        'title':{
            'text':'Health Facilities'
        }
    },
    'yAxis': {
        'title': {
        'text': 'Volume (L)'
        }
    },
    'legend': {
        'enabled': False
    },
    'credits': {
        'enabled': False
    },
    'series': [{
            'name':'Volume',
            'data': volume_data,
            'tooltip': {
                'valueDecimals': 2
            }
    }]

}

options_2 = {
    'title': {
        'text': 'Number of Trips Done to Pickup Vaccines by Health Facilities'
    },
    'chart': {
            'height':520
        },
    'xAxis': {
        'categories':total_trips_date.index
    },
    'yAxis': {
            'title':{
                        'text':'Trips'
                    },
            'labels': {
                'format': '{value}',
            }
        },
    'credits': {
        'enabled': False
    },
    'legend': {
        'enabled': False
    },
    'series':[
    {
        'name': 'Number of Trips',
        'data':total_trips_date['Number of Trips'].tolist(),
         'tooltip': {
                     'valueDecimals': 0,
                     'valueSuffix': ''
                     }
    }]
}



options_6 = {
    'title': {
        'text': 'Immunization Sessions Conducted Jan-Dec 2021'
    },
    'xAxis': {
        'type': 'category',
        'title':{
            'text':'Districts'
        },
        'categories':total_vacc_sessions.index
    },
    'yAxis': [{
        'title':{
            'text':'Fixed'
        }
    },
    {
    'title': {
        'text':'Outreach and Mobile'
    },
    'opposite': True
    }],
    'credits': {
        'enabled': False
    },
    'plotOptions': {
        'scatter': {
            'dataLabels': {
                'enabled': True
            }
        }
    },
    'tooltip': {
        'shared': True
    },

    'series': [
    {
        'type':'column',
        'name':'fixed',
        'data':total_vacc_sessions['No. of vaccination sessions__fixed'].tolist()
    },
    {
       'type':'column',
       'name':'outreach',
       'yAxis': 1,
       'data':total_vacc_sessions['No. of vaccination sessions__outreach'].tolist()
    },
    {
       'type':'column',
       'name':'mobile',
       'yAxis': 1,
       'data':total_vacc_sessions['No. of vaccination sessions__mobile'].tolist()
    }]

}

options_4 = {
    'title': {
        'text': 'Mobile Immunization Strategy (i.e. Outreach to Locations >15km from Health Facilities)'
    },
    'xAxis': {
        'categories':total_vacc_sessions_date.index
    },
    'credits': {
        'enabled': False
    },
    'legend': {
        'enabled': False
    },
    'series':[
    {
        'name': 'Mobile',
        'data':total_vacc_sessions_date['No. of vaccination sessions__mobile'].tolist()

    }]
}

options_7 = {
    'chart': {
        'type':'area'
    },
    'title': {
        'text':'Wastage by Freezing & VVM Changes Jan-Dec 2021'
    },
    'xAxis': {
        'categories':df_wastage_by_reason.index
    },
    'yAxis': {
        'title':{
                 'text':'Doses'
             }
    },
    'credits': {
        'enabled': False
    },
    'tooltip': {
        'shared': True
    },
    'series':[{
        'name': 'Total VVM Change',
        'data': df_wastage_by_reason['Total VVM Change'].tolist()
    },
    {
    'name': 'Total Freezing',
    'data': df_wastage_by_reason['Total Freezing'].tolist()
    }]
}

options_3 = {
    'chart': {
        'type':'column'
    },
    'title': {
        'text':'Closed Vial Wastage by Vaccine Jan-Dec 2021'
    },
    'xAxis': {
        'type': 'category',
        'title':{
            'text':'Vaccine'
        }
    },
    'yAxis': {
            'title':{
                'text':'Number of Doses Wasted'
            }
        },
    'credits': {
        'enabled': False
    },
    'tooltip': {
        'shared': True
    },
    'plotOptions': {
        'column': {
            'pointPadding': 0.2,
            'borderWidth': 3,
            'dataLabels': {
                'enabled': False
            }
        }
    },
    'series':[{
        'name': 'VVM',
        'data':vvm_vacc
    },
    {
    'name': 'Freezing',
    'data':freezing_vacc
    }]
}

options_5 = {

    'title': {
        'text': 'Cost of Transporting Vaccine Jan-Dec 2021'
    },
    'xAxis': {
        'type': 'category',
        'title':{
            'text':'Districts'
        },
        'categories':df9['District'].tolist()
    },
    'yAxis': [{
        'title':{
            'text':'Annual Cost'
        },
        'labels': {
            'format': '${value}',
        }
    },
    {
    'title': {
        'text':'Cost Per Dose'
    },
    'labels': {
        'format': '${value}',
    },
    'opposite': True
    }],
    'credits': {
        'enabled': False
    },
    'plotOptions': {
        'scatter': {
            'dataLabels': {
                'enabled': True,
                'format':'${y}'
            }
        }
    },
    'tooltip': {
        'shared': True
    },

    'series': [
    {
        'type':'column',
        'name':'Annual Cost of Transporting Vaccines',
        'data':df9['Annual Transportation Cost'].tolist(),
        'tooltip': {
            'valueDecimals': 2,
            'valuePrefix': '$'
        }
    },
    {
       'type':'line',
       'name':'Transport Cost per Dose',
       'yAxis': 1,
       'data':df9['Transport CPD'].tolist(),
       'tooltip': {
           'valueDecimals': 2,
           'valuePrefix': '$'
       }
    }]

}

options_8 = {
    'chart': {
        'type': 'bar'
    },
    'title': {
        'text': 'Total Doses of Closed Vial Wastage of Vaccines (Freezing & VVM Change) in Transportation Jan-Dec 2021'
    },
    'xAxis': {
        'type': 'category'
    },
    'yAxis': {
        'title': {
        'text': 'Doses'
        }
    },
    'legend': {
        'enabled': False
    },
    'credits': {
        'enabled': False
    },
    'series': [{
            'name': 'Total Wastage',
            'data': wastage_data
    }]

}

nova_int = [
    [
        1656324240.0,
        9.3
    ],
    [
        1656324840.0,
        7.8
    ],
    [
        1656325440.0,
        6.4
    ],
    [
        1656326040.0,
        5.2
    ],
    [
        1656326640.0,
        10.6
    ],
    [
        1656327240.0,
        11.3
    ],
    [
        1656327840.0,
        9.6
    ],
    [
        1656328440.0,
        8.3
    ],
    [
        1656329040.0,
        7.1
    ],
    [
        1656329640.0,
        5.9
    ],
    [
        1656330180.0,
        5.0
    ],
    [
        1656330780.0,
        5.8
    ],
    [
        1656331380.0,
        5.3
    ],
    [
        1656331980.0,
        6.8
    ],
    [
        1656332580.0,
        6.2
    ],
    [
        1656333180.0,
        5.6
    ],
    [
        1656333780.0,
        5.1
    ],
    [
        1656334380.0,
        6.2
    ],
    [
        1656334980.0,
        6.3
    ],
    [
        1656335580.0,
        5.9
    ],
    [
        1656336180.0,
        5.3
    ],
    [
        1656336780.0,
        5.8
    ],
    [
        1656337380.0,
        5.6
    ],
    [
        1656337980.0,
        8.7
    ],
    [
        1656338580.0,
        7.4
    ],
    [
        1656339180.0,
        6.7
    ],
    [
        1656339780.0,
        5.8
    ],
    [
        1656340380.0,
        6.1
    ],
    [
        1656340980.0,
        7.3
    ],
    [
        1656341580.0,
        6.0
    ],
    [
        1656342180.0,
        5.2
    ],
    [
        1656342780.0,
        5.5
    ],
    [
        1656343380.0,
        7.9
    ],
    [
        1656343980.0,
        6.8
    ],
    [
        1656344580.0,
        5.8
    ],
    [
        1656345180.0,
        5.2
    ],
    [
        1656345780.0,
        5.9
    ],
    [
        1656346380.0,
        5.5
    ],
    [
        1656346980.0,
        7.9
    ],
    [
        1656347580.0,
        6.4
    ],
    [
        1656348180.0,
        5.3
    ],
    [
        1656348780.0,
        5.8
    ],
    [
        1656349380.0,
        5.1
    ],
    [
        1656349980.0,
        5.6
    ]
]
options_9 = {
    'chart': {
        'type': 'area',
        'zoomType': 'x',
        'panning': True,
        'panKey': 'shift',
        'scrollablePlotArea': {
            'minWidth': 1000
        }
        },
    'caption': {
        'text': '(scroll right to view more records)'
    },

    'title': {
        'text': 'Temperature Monitoring of the Vaccine Land Cruiser for Distribution of Vaccines'
    },

    'credits': {
        'enabled': True,
        'text': 'Toyota TTC, Parsyl'
    },

    'annotations': [{
        'draggable': '',
        'labelOptions': {
            'backgroundColor': '#ffffff',
            'verticalAlign': 'top',
            'y': 15
        },
        'labels': [{
            'point': {
                'xAxis': 0,
                'yAxis': 0,
                'x': 1656327840.0,
                'y': 9.6
            },
            'text': 'City: Ndiaye, Engine: Running, Ignition: ON'
        }, {
            'point': {
                'xAxis': 0,
                'yAxis': 0,
                'x': 1656328440.0,
                'y': 8.3
            },
            'text': 'City: Ndiaye, Engine: Running, Ignition: ON'
        }, {
            'point': {
                'xAxis': 0,
                'yAxis': 0,
                'x': 1656330180.0,
                'y': 5.0
            },
            'text': 'City: Richard Toll, Engine: Running, Ignition: ON'
        }, {
            'point': {
                'xAxis': 0,
                'yAxis': 0,
                'x': 1656331380.0,
                'y': 5.3
            },
            'x': -10,
            'text': 'City: Ndiaye, Engine: Running, Ignition: ON'
        }, {
            'point': {
                'xAxis': 0,
                'yAxis': 0,
                'x': 1656341580.0,
                'y': 6.0
            },
            'text': 'City: Ndiaye, Engine: Running, Ignition: ON'
        }]
    }, {
        'draggable': '',
        'labelOptions': {
            'shape': 'connector',
            'align': 'right',
            'justify': False,
            'crop': True,
            'style': {
                'fontSize': '0.8em',
                'textOutline': '1px white'
            }
        },
        'labels': [{
            'point': {
                'xAxis': 0,
                'yAxis': 0,
                'x': 1656327240,
                'y': 11.3
            },
            'text': 'Driver stopped to remove ambient temperature recorder'
        }]
    }],

    'xAxis': {
        'type':'datetime',
           'dateTimeLabelFormats': {
                                   'second': '%d %H:%M:%S',
                                   # 'minute': '%Y-%m-%d/%H:%M',
                                   #  'hour': '%Y-%m-%d/%H:%M',
                                   #  'day': '%Y/%m-%d',
                                   #  'week': '%Y/%m-%d',
                                   #  'month': '%Y-%m',
                                   #  'year': '%Y'
                                },
        #'format': '{value:%m-%d}',
        'tickInterval': 0.01,
        'title': {
            'text': 'Date/Time'
        }
    },

    'yAxis': {
        'startOnTick': True,
        'endOnTick': True,
        'maxPadding': '0.35',
        'title': {
            'text': 'Temperature'
        },
        'labels': {
            'format': '{value} C'
        }
    },

    'tooltip': {
        'headerFormat': 'Time: {point.x:.1f} <br>',
        'pointFormat': '{point.y} Degrees',
        'shared': True
    },

    'legend': {
        'enabled': False
    },
    'series': [{
        'data': nova_int,
        'lineColor': '#2f7ed8',
        'color': '#B5CA92',
        'fillOpacity': '0.5',
        'name': 'Temperature',
        'marker': {
            'enabled': False
        },
        'threshold': 'null'
    }]

}



layout = dbc.Container(
                           [
                           html.Div([
                           html.H2(['Pete & Podor Districts of Saint Louis Region, Senegal Baseline Analysis'],style={'text-align':'center','font-size':'3rem'}),
                           html.Hr(style={'background-color':'rgba(61,61,61,0.5)'}),
                           ],style={'margin-top':'8px'}),

                           dbc.Row(
                                   [
                                    dbc.Col(
                                            [
                                            html.Div(id="datawrapper-chart-uxDWb"),
                                            html.H6(['Map Showing the Last 100 Positions of the Vaccine Land Cruiser in St. Louis Region, Senegal'],style={'text-align':'center'}),
                                            html.Iframe(id='iframe',src="//www.arcgis.com/apps/Embed/index.html?webmap=4d86714227ca4eb092064fef1797efe7&extent=-16.841,15.8343,-15.3249,16.6544&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light",
                                            style={"height": "500px", "width": "100%"},
                                            ),
                                            dbc.Tooltip("Locations traveled by the Vaccine Land Cruiser in St. Louise Region of Senegal", target="iframe"),
                                            ],md=4
                                    ),

                                   dbc.Col(
                                           [
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                  html.H6(['VLC Annual Vaccine Transportation Cost'],style={'text-align':'center'}, id="target"),
                                                                  html.H3([str("$"+"0"+" (TBD)")],style={'text-align':'center','font-size':'5rem'}),
                                                                  html.H6(['Baseline Annual Vaccine Transportation Cost'],style={'text-align':'center'}, id="bsl_cost"),
                                                                  html.H2(["$"+"{:,.0f}".format(baseline_annual_tp_cost)],style={'text-align':'center','font-size':'2rem'}),
                                                                     dbc.Tooltip("Cost of transporting vaccines using the Toyota Vaccine Land Cruiser. It comprises of the cost of fuel, per diems and any other operational costs", target="target"),
                                                                     dbc.Tooltip("Cost of transporting vaccines with the conventional method used in the region, district and health facilities", target="bsl_cost")



                                                                 ]
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           ),
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [

                                                                 html.Div([dav.HighChart(id="container",constructorType='chart',options=options_9)], id='container'),
                                                                    #dcc.Store(id='nov-data',data=nova_int),
                                                                     dbc.Tooltip("This is the total amount of routine immunization vaccines received in liters for each location", target="water")
                                                                 ],style={'color':'white'}
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           )


                                           ],md=4
                                   ),
                                   dbc.Col(
                                           [
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                  html.H6(['VLC Cost per Dose'],style={'text-align':'center'},id='vlccpd'),
                                                                    html.H3([str("$"+"0"+" (TBD)")],style={'text-align':'center','font-size':'5rem'}),
                                                                     dbc.Tooltip("The Vaccine Land Cruiser (VLC) cost per dose sums up the total cost of transporting vaccines with the land cruiser and divides it by the total number of doses transported", target="vlccpd", flip=False),
                                                                  html.H6(['Baseline Cost per Dose'],style={'text-align':'center'}, id='bsl_costpd'),
                                                                     dbc.Tooltip("This is the cost of transporting vaccines per dose. It is calculated by adding all the transportation cost and dividing it by the total number of doses.", target="bsl_costpd", flip=False),
                                                                  html.H2([str("$"+"{:.2f}".format(avg_tcpd))],style={'text-align':'center','font-size':'2rem'})
                                                                  ]
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           ),
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [

                                                                 html.Div([dav.HighChart(constructorType='chart',options=options_2)], id='trips-done'),
                                                                     dbc.Tooltip("This is the number of trips done to fulfil the supply period demand based on the transport storage capacity and the quantity of vaccines", target="trips-done")


                                                                ],style={'color':'white'}
                                                   )
                                                   ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                          )

                                          ],md=4
                                   )
                                   ]
                           ),
                           dbc.Row(
                                  [
                                  dbc.Col(
                                          [
                                          dbc.Card(
                                                   [
                                                   dbc.CardBody(
                                                                [
                                                                html.Div([dav.HighChart(id="wastage-by-vacc",constructorType='chart',options=options_6)], id='sessions_cond'),
                                                                    dbc.Tooltip("Immunization sessions conducted for fixed, mobile and outreach strategies.", target="sessions_cond", flip=False)
                                                                ],style={'color':'white'}
                                                   )
                                                   ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                          )
                                          ],md=4
                                  ),

                                  dbc.Col(
                                          [
                                          dbc.Card(
                                                   [
                                                   dbc.CardBody(
                                                                [
                                                                html.Div([dav.HighChart(id="immunization-sessions-strategy",constructorType='chart',options=options_4)], id='mob_str'),
                                                                    dbc.Tooltip("Mobile strategies refers to reaching children that reside in locations that are above 15km from the health facilities by motorbikes, foot or other conventional methods using vaccine carriers or coldboxes.", target="mob_str", flip=False)


                                                                ],style={'color':'white'}
                                                   )
                                                   ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                          )

                                          ],md=4
                                  ),
                                  dbc.Col(
                                          [
                                          dbc.Card(
                                                   [
                                                   dbc.CardBody(
                                                                [
                                                                html.Div([dav.HighChart(id="wastage-by-date",constructorType='chart',options=options_5)],id='cost_tp'),
                                                                    dbc.Tooltip("Cost of transporting vaccines is calculated by adding all costs associated with transporting vaccines such as commercial transportation costs, fuel costs per kilometer, per diems etc.", target="cost_tp", flip=False)
                                                                ],style={'color':'white'}
                                                   )
                                                   ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                          )
                                          ],md=4
                                  )

                                  ]
                           ),
                           dbc.Row(
                                   [
                                   dbc.Col(
                                           [
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                 html.Div([dav.HighChart(id="immunization-sessions",constructorType='chart',options=options_3)],id='cvw'),
                                                                     dbc.Tooltip("Closed vial wastage refers to physical damage, heat or freeze excursions on a vaccine vial", target="cvw", flip=False)


                                                                 ],style={'color':'white'}
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           )

                                           ],md=4
                                   ),


                                   dbc.Col(
                                           [
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                 html.Div([dav.HighChart(id="transporting-cost",constructorType='chart',options=options_7)],id='wastge_fzvvm'),
                                                                     dbc.Tooltip("Wastage by freezing and VVM change calculates the number of doses of vaccines damaged by freeze and heat excursions during transportation", target="wastge_fzvvm", flip=False)
                                                                 ],style={'color':'white'}
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           )
                                           ],md=4
                                   ),
                                   dbc.Col(
                                           [
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                 html.Div([dav.HighChart(id="total-wastage",constructorType='chart',options=options_8)],id='total_wastage'),
                                                                     dbc.Tooltip("This refers to the sum of all vaccines, in doses, that were damaged by freezing, heat or breakage", target="total_wastage", flip=False)
                                                                 ],style={'color':'white'}
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           )
                                           ],md=4
                                   )
                                   ]
                           )

                           ],fluid=True
)

# app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside2',
#         function_name='large_params_function'
#     ),
#     Output('map-2', 'children'),
#     Input('map-2', 'id'),
#     Input('map-data2','data')
# )
#


