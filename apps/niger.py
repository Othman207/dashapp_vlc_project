from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import os
import pandas as pd
import numpy as np
import datetime
import dash_alternative_viz as dav
#pip install git+https://github.com/plotly/dash-alternative-viz.git#egg=dash_alternative_viz
from app import app
import json


dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/Attachment_1642767473.xlsx')

delivery = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data/Niger_Delivery_1.xlsx')

df1 = pd.read_excel(dataset,"Uti2")

df2 = pd.read_excel(dataset,"DVDMT")

df3 = pd.read_excel(dataset,"Logistics Costs",usecols=['Site','Annual Transportation Cost','Transport CPD'])

d1 = pd.read_excel(delivery,"OTIF")

d2 = d1.groupby(by=['Vehicle']).mean()
d3 = d2['Total Doses Delivered']
d4 = d1.filter(['Vehicle','Total Doses Delivered'], axis=1)
# d4.rename(columns={'Vehicle':'name', 'Total Doses Delivered':'y'}, inplace=True)
d5 = d4.groupby(by=['Vehicle']).sum().reset_index()
d5['Sum'] = d5['Total Doses Delivered'].sum()
d5['Percent'] = d5['Total Doses Delivered']/d5['Sum']*100
d5 = d5.filter(['Vehicle','Percent'], axis=1)
d5['drilldown'] = d5['Vehicle']

d6 = d1.rename(columns={'DESTINATIONS / ALLOCATION Main_Allocation':'name', 'Vehicle':'id', }, inplace=False)
d6['Sum'] = d6['Total Doses Delivered'].sum()
d6['data'] = d6['Total Doses Delivered']/d6['Sum']*100

d6 = d6.filter(['name','id', 'data'], axis=1)
dvlc = d6[d6['id'].str.contains("VLC")]
dvlc = dvlc.drop(['id'], axis=1)

dvlc2 = dvlc.groupby(by=['name']).sum()

dcon = d6[d6['id'].str.contains("Conventional Truck")]
dcon = dcon.drop(['id'], axis=1)

dcon2= dcon.groupby(by=['name']).sum()

new = d5.rename(columns={'Vehicle':'name', 'Percent':'y'}, inplace=False)

new2 = new.groupby(new.columns, axis=1).agg(lambda x: x.to_numpy().tolist() if x.shape[1]>1 else x.to_numpy().flatten()).to_dict('records')

df2.rename(columns={'VPO_Unopened vial wastage_VVM status':'OPV_Unopened vial wastage_VVM status',
                        'VPI_Unopened vial wastage_VVM status':'IPV_Unopened vial wastage_VVM status',
                        'Pneumo_Unopened vial wastage_VVM status':'PCV_Unopened vial wastage_VVM status',
                        'VAR_Unopened vial wastage_VVM status':'MV_Unopened vial wastage_VVM status',
                        'VAA_Unopened vial wastage_VVM status':'YF_Unopened vial wastage_VVM status',
                        'VPH_Unopened vial wastage_VVM status':'HPV_Unopened vial wastage_VVM status',
                        'VPO_Unopened vial wastage_Freezing':'OPV_Unopened vial wastage_Freezing',
                        'VPI_Unopened vial wastage_Freezing':'IPV_Unopened vial wastage_Freezing',
                        'Pneumo_Unopened vial wastage_Freezing':'PCV_Unopened vial wastage_Freezing',
                        'VAR_Unopened vial wastage_Freezing':'MV_Unopened vial wastage_Freezing',
                        'VAA_Unopened vial wastage_Freezing':'YF_Unopened vial wastage_Freezing',
                        'VPH_Unopened vial wastage_Freezing':'HPV_Unopened vial wastage_Freezing'},
inplace=True)

df4 = df1[['BCG_Quantity (doses)_received', 'VPO_Quantity (doses)_received',
       'VPI_Quantity (doses)_received', 'Penta_Quantity (doses)_received',
       'Pneumo_Quantity (doses)_received', 'Rota_Quantity (doses)_received',
       'VAR_Quantity (doses)_received', 'VAA_Quantity (doses)_received',
       'MenA_Quantity (doses)_received', 'Td_Quantity (doses)_received',]]

df4.rename(columns={'BCG_Quantity (doses)_received':'BCG', 'VPO_Quantity (doses)_received':'OPV',
       'VPI_Quantity (doses)_received':'IPV', 'Penta_Quantity (doses)_received':'Penta',
       'Pneumo_Quantity (doses)_received':'PCV', 'Rota_Quantity (doses)_received':'Rota',
       'VAR_Quantity (doses)_received':'MV', 'VAA_Quantity (doses)_received':'YF',
       'MenA_Quantity (doses)_received':'MenA', 'Td_Quantity (doses)_received':'Td'},
inplace=True)
df4['Hep-B'] = 0
df4['HPV'] = 0

df5 = df4[['BCG', 'OPV', 'IPV', 'Penta', 'PCV', 'Rota', 'MV', 'YF', 'MenA', 'Td', 'Hep-B', 'HPV']].sum()

#df3 = pd.read_excel("Attachment_1642767473.xlsx","Logistics Costs",usecols=['Site','Annual Transportation Cost','Transport CPD'])


df2.replace('-',np.nan,inplace=True)

df1['Utilization with 3990L Capacity'] = 100 * df1['Utilization with 3990L Capacity']

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


# Sum up all values of df1
total_volume = df1.groupby(by=['Districts']).sum()


avg_volume_district = df1.groupby(by=['Districts']).mean()

dfpt= pd.pivot_table(df1, values='Utilization with 3990L Capacity',index=['Country', 'Monthly reports'],aggfunc=np.mean)
dfpt.reset_index(inplace=True)
dfpt2 = dfpt.iloc[pd.to_datetime(dfpt['Monthly reports'], format='%b-%y').argsort()]
total_utilization_date = dfpt2.groupby(by=['Monthly reports'],sort=False).mean()

total_vacc_sessions = df2.groupby(by=['Districts']).sum()

total_vacc_sessions_date = df2.groupby(by=['Monthly reports'],sort=False).sum()


vvm_cols = [col for col in df2.columns if 'VVM status' in col]


freezing_cols = [col for col in df2.columns if 'wastage_Freezing' in col]

wastage_cols = [col for col in df2.columns if '_Unopened vial wastage' in col]

received_cols = [col for col in df2.columns if '_Quantity (doses)_received' in col]

# Select only columns with vvm, freeze and wastage change from total_vacc_session_date
total_vvm_change = total_vacc_sessions_date[vvm_cols]

total_freezing = total_vacc_sessions_date[freezing_cols]

total_wastage = total_vacc_sessions_date[wastage_cols]

total_received = total_vacc_sessions_date[received_cols]
# transpose
total_vvm_change_by_vacc = total_vvm_change.T
# Remove string with Unopened vial text to leave only the vaccine name
total_vvm_change_by_vacc.index = total_vvm_change_by_vacc.index.str.replace('_Unopened vial wastage_VVM status','')
# Sum total wastage by date
total_wastage_by_date = total_wastage.sum(axis=1).to_frame().rename(columns={0:'Total Wastage'})

total_received_by_date = total_received.sum(axis=1).to_frame().rename(columns={0:'Total Received'})

#Combine total wastage with total received doses
df_received = total_received_by_date.combine_first(total_wastage_by_date)

# Calculate percentage of wastage
df_received['Percent Wasted'] = df_received['Total Wastage']/df_received['Total Received']*100

df_received['Percent Wasted'] = df_received['Percent Wasted'].round(decimals=2)


# Transpose
total_freezing_by_vacc = total_freezing.T

total_freezing_by_vacc.index = total_freezing_by_vacc.index.str.replace('_Unopened vial wastage_Freezing','')

# sum vvm change by date and make a single column
total_vvm_change = total_vvm_change.sum(axis=1).to_frame().rename(columns={0:'Total VVM Change'})

# sum freeze change by date and make a single column
total_freezing = total_freezing.sum(axis=1).to_frame().rename(columns={0:'Total Freezing'})

# merge vvm, freeze into single df
df_wastage_by_reason = pd.concat([total_vvm_change,total_freezing],axis=1)
# total vvm change by vaccine into a single column
total_vvm_change_by_vacc = total_vvm_change_by_vacc.sum(axis=1).to_frame().rename(columns={0:'Total VVM Change'})

# get total doses by vaccine to concatenate with total_vvm_change_by_vacc and calculate percentage of VVM wastage by vacc
df5.name = 'Distributed'
df7 = pd.DataFrame([df5])
df7 = df7.transpose()


# Wastage by reason to insert % of VVM and Freeze by month
df_wastage_by_reason = df_wastage_by_reason.combine_first(df_received)

## for VVM wastage by reason
df_wastage_by_reason['Percent VVM Change'] = df_wastage_by_reason['Total VVM Change']/df_wastage_by_reason['Total Received']*100

df_wastage_by_reason['Percent VVM Change'] = df_wastage_by_reason['Percent VVM Change'].round(decimals=2)

## for freezing wastage by reason
df_wastage_by_reason['Percent Freeze Change'] = df_wastage_by_reason['Total Freezing']/df_wastage_by_reason['Total Received']*100

df_wastage_by_reason['Percent Freeze Change'] = df_wastage_by_reason['Percent Freeze Change'].round(decimals=2)


total_vvm_change_by_vacc = total_vvm_change_by_vacc.combine_first(df7)

# Calculate percentage of wastage
total_vvm_change_by_vacc['VVM Percent Damage'] = total_vvm_change_by_vacc['Total VVM Change']/total_vvm_change_by_vacc['Distributed']*100

total_vvm_change_by_vacc['VVM Percent Damage'] = total_vvm_change_by_vacc['VVM Percent Damage'].round(decimals=2)

# sort in ascending order
total_vvm_change_by_vacc.sort_values(by='Total VVM Change',inplace=True)
# total freeze change by vaccine into a single column

total_freezing_by_vacc = total_freezing_by_vacc.sum(axis=1).to_frame().rename(columns={0:'Total Freezing'})

# get total doses by vaccine to concatenate with total_vvm_change_by_vacc and calculate percentage of VVM wastage by vacc
total_freezing_by_vacc = total_freezing_by_vacc.combine_first(df7)

# Calculate percentage of wastage
total_freezing_by_vacc['Freezing Percent Damage'] = total_freezing_by_vacc['Total Freezing']/total_freezing_by_vacc['Distributed']*100

total_freezing_by_vacc['Freezing Percent Damage'] = total_freezing_by_vacc['Freezing Percent Damage'].round(decimals=2)

# sort in ascending order
total_freezing_by_vacc.sort_values(by='Total Freezing',inplace=True)



avg_volume = avg_volume_district['Total Volume (L)'].mean()
avg_util = avg_volume_district['Utilization with 3990L Capacity'].mean()
avg_doses = avg_volume_district['TOTAL DOSES'].mean()

district_names = []
volume_data = []
wastage_data = []

vvm_vacc = []

freezing_vacc = []

vlc_delivery = []
dcon_delivery = []

for district in total_volume.index:
    volume_data.append([district,total_volume['Total Volume (L)'][district]])


for district in df1['Districts'].unique():
    district_names.append({'label':district,'value':district})

for name in dvlc2.index:
    vlc_delivery.append([name,dvlc2['data'][name]])

for name in dcon2.index:
    dcon_delivery.append([name, dcon2['data'][name]])

# for vaccine in total_freezing_by_vacc.index:
#     freezing_vacc.append([vaccine,total_freezing_by_vacc['Total Freezing'][vaccine]])

for vaccine in total_vvm_change_by_vacc.index:
    vvm_vacc.append([vaccine,total_vvm_change_by_vacc['VVM Percent Damage'][vaccine]])

for vaccine in total_freezing_by_vacc.index:
    freezing_vacc.append([vaccine,total_freezing_by_vacc['Freezing Percent Damage'][vaccine]])

for date in df_received.index:
    wastage_data.append([date,df_received['Percent Wasted'][date]])

# for date in total_wastage_by_date.index:
#     wastage_data.append([date,total_wastage_by_date['Total Wastage'][date]])



df3 = df3.loc[df3['Site'].isin(total_volume.index.tolist())]

df3 = df3.drop_duplicates(subset=['Site'])

df3['Transport CPD'] = df3['Transport CPD'].round(decimals=3)


options_1 = {
    'chart': {
        'type': 'bar',
        'height':500
    },
    'title': {
        'text': 'Total Volume (liters) of Vaccines Received by Districts (2021)'
    },
    'xAxis': {
        'type': 'category',
        'title':{
            'text':'Districts'
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
        'text': 'Average Utilization Rate of Conventional Cold Truck Refrigerator in Dosso Region, Niger Jan-Dec 2021'
    },
    'chart': {
            'height':520
        },
    'xAxis': {
        'categories':total_utilization_date.index
    },
    'yAxis': {
            'labels': {
                'format': '{value}%',
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
        'name': 'Utilization rate',
        'data':total_utilization_date['Utilization with 3990L Capacity'].tolist(),
        'tooltip': {
                    'valueDecimals': 2,
                    'valueSuffix': '%'
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
        'text':'Percentage of Vaccine Doses Wasted by Freezing & VVM Changes in Transportation Jan-Dec 2021'
    },
    'xAxis': {
        'categories':df_wastage_by_reason.index
    },
    'yAxis': {
        'title':{
                 'text':''
             },
    'labels': {
            'format': '{value}%',
        }
    },
    'credits': {
        'enabled': False
    },
    'tooltip': {
        'shared': True
    },
    'series':[{
        'name': '% VVM Change',
        'data': df_wastage_by_reason['Percent VVM Change'].tolist()
    },
    {
    'name': '% Freezing',
    'data': df_wastage_by_reason['Percent Freeze Change'].tolist()
    }]
}

options_3 = {
    'chart': {
        'type':'column'
    },
    'title': {
        'text':'Proportion of Doses Transported Damaged by Heat and Freezing Exposures, Jan-Dec 2021'
    },
    'xAxis': {
        'type': 'category',
        'title':{
            'text':'Vaccine'
        }
    },
    'yAxis': {
            'title':{
                'text':'Percent of Doses Damaged'
            },
        'labels': {
            'format': '{value}%',
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
        'text': 'Proportion of Doses Damaged in Transportation Jan-Dec 2021'
    },
    'xAxis': {
        'type': 'category'
    },
    'yAxis': {
        'title': {
        'text': 'Percent'
        },
    'labels': {
            'format': '{value}%',
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

options_9 = {
    'chart':       {
        'type': 'pie'
    },
    'title':       {
        'text': 'Distribution of Vaccines'
    },
    'subtitle':    {
        'text': 'Click the slices to view districts'
    },
    'credits': {
            'enabled': True,
            'text': 'Source: Niger SMT 2022'
        },
    'plotOptions': {
        'series': {
            'dataLabels': {
                'enabled': True,
                'format':  '{point.name}: {point.y:.1f}%'
            }
        }
    },

    'tooltip':     {
        'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
        'pointFormat':  '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    },

    'series':      [
        {
            'name': "Vehicle",
            'colorByPoint': True,
            'data': new2
        }
    ],
    'drilldown':   {
        'series': [{
             'name': "VLC",
             'id': "VLC",
            'data': vlc_delivery
        },
            {
                'name': "Conventional Truck",
                'id':   "Conventional Truck",
                'data': dcon_delivery
            }
        ]

    }
}



layout = dbc.Container(
                           [
                           html.Div([
                           html.H1(['Dosso Region, Niger Republique'],style={'text-align':'center','font-size':'3rem'}),
                           html.H3(['Vaccine Land Cruiser Evaluation'],style={'text-align':'center','font-size':'2rem', 'color':'blue'}),
                           html.Hr(style={'background-color':'rgba(61,61,61,0.5)'}),
                           ],style={'margin-top':'8px'}),

                           dbc.Row(
                                   [
                                   dbc.Col(
                                           [
                                           html.Div(id='map-1'),
                                               html.H6(['Map Showing the Last 100 Positions of the Vaccine Land Cruiser in Dosso Region, Niger'],
                                                       style={'text-align': 'center'}),
                                               html.Iframe(id='iframe', src="//www.arcgis.com/apps/Embed/index.html?webmap=49466db84b9c4661a729362974c8af48&extent=3.196,13.0424,3.2078,13.0495&zoom=true&previewImage=false&scale=true&search=true&searchextent=true&legend=true&disable_scroll=true&theme=light",
                                                           style={"height": "500px", "width": "100%"},
                                                           ),
                                               html.H6(['Map Showing District Stores and Vaccination Points'],style={'text-align':'center'}),
                                               html.Iframe(id='iframe', src="/assets/indexx.html",
                                               style={"height": "400px", "width": "100%"},
                                               )
                                           ],md=4
                                   ),

                                   dbc.Col(
                                           [
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                     html.H6([
                                                                                 'Average Doses of Vaccines Transported per Month to Districts with Vaccine Land Cruiser'],
                                                                             id='avgvol',
                                                                             style={'text-align': 'center'}),
                                                                     dbc.Tooltip(
                                                                         "This is the average number of doses transported to 5 districts (Boboye, Dogondoutchi, Falmey, Gaya, Loga) of Dosso Region per month",
                                                                         target="avgvol"),
                                                                     html.H2(["{:,.0f}".format(d3.iat[1])],
                                                                             style={'text-align': 'center', 'font-size':  '5rem'}),
                                                                     html.H6(['Average Doses of Vaccines Transported per Month to Districts with Conventional Cold Truck'],
                                                                             style={'text-align':'center'}, id="bsl_doses"),
                                                                      html.H2(["{:,.0f}".format(d3.iat[0])],
                                                                              style={'text-align':'center','font-size':'2rem'}),
                                                                            dbc.Tooltip("This is the average number of doses transported to 3 districts (Dioundou, DS Dosso, Tibiri) of Dosso Region per month",
                                                                                        target="bsl_doses")
                                                                 ]
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           ),
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [
                                                                 html.Div([dav.HighChart(id="avg-vol",constructorType='chart',options=options_1)],id='vol_received'),
                                                                 dbc.Tooltip("This is the total volume of vaccines received by each district from Jan-Dec 2021", target="vol_received")
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
                                                                    html.Div([dav.HighChart(id="deliveries_by_vehicle",constructorType='chart',options=options_9)]),
                                                                 ]
                                                    )
                                                    ],className="shadow p-3 mb-5 bg-white rounded border-light"
                                           ),
                                           dbc.Card(
                                                    [
                                                    dbc.CardBody(
                                                                 [

                                                                 html.Div([dav.HighChart(id="Utilization-with-3990L-Capacity",constructorType='chart',options=options_2)], id='avg_uti_truck'),
                                                                    dbc.Tooltip('This is the percentage of conventional truck cold storage capacity that is ccupied by vaccines and their diluents for a given time period during transportation.', target='avg_uti_truck', flip=False)


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
                                                                html.Div([dav.HighChart(id="wastage-by-vacc",constructorType='chart',options=options_6)], id='sessions_con'),
                                                                    dbc.Tooltip('Immunization sessions conducted for fixed, mobile and outreach strategies', target='sessions_con')
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
                                                                    dbc.Tooltip('Mobile strategies refers to reaching children that reside in locations that are above 15km from the health facilities by motorbikes, foot or other conventional methods using vaccine carriers or coldboxes.', target="mob_str", flip=False)


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
                                                                html.Div([dav.HighChart(id="wastage-by-date",constructorType='chart',options=options_5)], id='cost_tp'),
                                                                    dbc.Tooltip("Cost of transporting vaccines is calculated by adding all costs associated with transporting vaccines such as commercial transportation costs, fuel costs per kilometer, per diems etc.", target = "cost_tp", flip=False)
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
                                                                 html.Div([dav.HighChart(id="immunization-sessions",constructorType='chart',options=options_3)], id='cvw'),
                                                                     dbc.Tooltip("This chart shows the percentage of doses transported that were damaged by heat (VVM) or freezing temperature exposures.", target="cvw", flip=False)


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
                                                                 html.Div([dav.HighChart(id="transporting-cost",constructorType='chart',options=options_7)], id='fzvvm'),
                                                                     dbc.Tooltip("Chart showing the proportion of vaccine doses damaged by freeze and heat excursions during transportation", target="fzvvm", flip=False)
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
                                                                 html.Div([dav.HighChart(id="total-wastage",constructorType='chart',options=options_8)], id='total_wastage'),
                                                                     dbc.Tooltip("Chart showing proportion of transported doses damaged by heat and freezing exposures combined by month, that were damaged by freezing, heat or breakage", target="total_wastage", flip=False)
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
