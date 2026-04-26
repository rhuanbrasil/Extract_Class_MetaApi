from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

access_token = os.environ.get('access_token')
app_secret = os.environ.get('app_secret')
app_id = os.environ.get('app_id')
ad_account_id = os.environ.get('ad_account_id')

FacebookAdsApi.init(app_id, app_secret, access_token, ad_account_id)

Account = AdAccount(ad_account_id)

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

filtros_leads = [
    {
        'field' : 'campaign.name',
        'operator' : 'CONTAIN',
        'value' : "LEADS"
    },
    {
        'field' : 'campaign.name',
        'operator' : 'NOT_CONTAIN',
        'value' : "IA"
    }
]
params_leads = {
    'date_preset' : 'last_7d',
    'filtering' : filtros_leads,
    'level': 'campaign'
}
campos_leads = [
    'campaign_name',
    'spend',
    'impressions',
    'clicks',
    'ctr',
]
filtros_traffic = [
    {
        'field' : 'campaign.name',
        'operator' : 'CONTAIN',
        'value' : "TRÁFEGO"
    }
]
params_traffic = {
    'date_preset' : 'last_7d',
    'filtering' : filtros_traffic,
    'level': 'campaign' 
}
campos_traffic = [
    'campaign_name',
    'objective_results',
    'spend',
    'impressions',
    'clicks',
    'ctr',
]
campaign_results = Account.get_insights(fields=campos_leads, params=params_leads)
traffic_results = Account.get_insights(fields=campos_traffic, params=params_traffic)

df = pd.DataFrame([dict(i) for i in campaign_results])
df2 = pd.DataFrame([dict(i) for i in traffic_results])

visitas = [linha[0]['values'][0]['value'] for linha in df2['results']]

df2['visitas'] = visitas
df2 = df2[['campaign_name','spend','impressions','clicks','ctr','date_start', 'date_stop', 'visitas']]
df = pd.concat([df, df2.iloc[[0]]], ignore_index=True)
