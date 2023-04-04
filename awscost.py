import boto3
import datetime
from helpers import notify

billing_client = boto3.client('ce')

today = datetime.date.today() - datetime.timedelta(1)
yesterday = today - datetime.timedelta(1)

start = yesterday.strftime('%Y-%m-%d')
end =today.strftime('%Y-%m-%d')

response = billing_client.get_cost_and_usage( 
   TimePeriod={ 
     'Start': start, 
     'End': end 
    }, 
   Granularity='DAILY', 
   Metrics=[
    'BlendedCost','UnblendedCost',
    'NetAmortizedCost','NetUnblendedCost',
    'NormalizedUsageAmount','AmortizedCost'] 
)
            
# print(response['ResultsByTime'])

for r in response['ResultsByTime']:
    blendedCost = r['Total']['BlendedCost']['Amount']
    unblendedCost = r['Total']['UnblendedCost']['Amount']
    netAmortizedCost = r['Total']['NetAmortizedCost']['Amount']
    netUnblendedCost = r['Total']['NetUnblendedCost']['Amount']
    normalizedUsageAmount = r['Total']['NormalizedUsageAmount']['Amount']
    amortizedCost = r['Total']['AmortizedCost']['Amount']
        
    #convert the amount to float
    amount = float(blendedCost) + float(unblendedCost) + float(netAmortizedCost) + float(netUnblendedCost) + float(normalizedUsageAmount) + float(amortizedCost)

# print(amount)

content = "\nAWS Cost: {} USD".format(amount)

notify.send(content)