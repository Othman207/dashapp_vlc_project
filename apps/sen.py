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


district_lat = {'Bah':11.3821629,'Tibiri':13.111496164791635, 'Loga':13.630843214618249, 'Gaya':11.885301486623014, 'Falmey':12.59218710888745,'Dogondoutchi':13.644155442065163,'Dioundiou':12.618310826888786, 'Dosso':13.050546691115104}

district_lng = {'Bah':-5.2855289,'Tibiri':4.01065349002892, 'Loga':3.5003297228187784, 'Gaya':3.454853618837945, 'Falmey':2.8502113335337578,'Dogondoutchi':4.033773700350723,'Dioundiou':3.543305405673443, 'Dosso':3.208135897880922}

dataset2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/pete.xlsx')

df1 = pd.read_excel(dataset2,"Uti2")

df2 = pd.read_excel(dataset2,"DVDMT")

df3 = pd.read_excel(dataset2,"Logistics Costs",usecols=['Site','Annual Transportation Cost','Transport CPD'])
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

total_volume['lat'] = total_volume.index.map(district_lat)
total_volume['lon'] = total_volume.index.map(district_lng)

avg_volume_district = df1.groupby(by=['Districts']).mean()



dfpt= pd.pivot_table(df1, values='Number of Trips',index=['Country', 'Monthly reports'],aggfunc=np.sum)
dfpt.reset_index(inplace=True)
dfpt2 = dfpt.iloc[pd.to_datetime(dfpt['Monthly reports'], format='%b-%y').argsort()]
total_trips_date = dfpt2.groupby(by=['Monthly reports'],sort=False).sum()

total_vacc_sessions = df2.groupby(by=['Health Center']).sum()

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


for district in total_volume.index:
    volume_data.append([district,total_volume['Total Volume (L)'][district]])
    map_data2.append({'name':district,'lat':total_volume['lat'][district],'lon':total_volume['lon'][district],'volume':total_volume['Total Volume (L)'][district]})

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
       'type':'scatter',
       'name':'outreach',
       'yAxis': 1,
       'data':total_vacc_sessions['No. of vaccination sessions__outreach'].tolist()
    },
    {
       'type':'scatter',
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
        'categories':df3['Site'].tolist()
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
        'data':df3['Annual Transportation Cost'].tolist(),
        'tooltip': {
            'valueDecimals': 2,
            'valuePrefix': '$'
        }
    },
    {
       'type':'scatter',
       'name':'Transport Cost per Dose',
       'yAxis': 1,
       'data':df3['Transport CPD'].tolist(),
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
                                            #dcc.Tooltip(text="Map showing "),
                                            html.H6(['Map Showing Health Facilities in Lena District'],style={'text-align':'center'}),
                                            html.Iframe(id='iframe',
                                            src="https://datawrapper.dwcdn.net/uxDWb/1/",
                                            style={"height": "500px", "width": "90%"},
                                            ),
                                            dbc.Tooltip("Description of map showing all the available locations in Senegal", target="iframe"),
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
                                                                 html.Div([dav.HighChart(id="avg-vol",constructorType='chart',options=options_1)],id="water"),
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


