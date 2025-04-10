import pandas as pd
import re
from datetime import datetime
# For SMS alerts (optional):
from twilio.rest import Client 

# Mock data (replace with real bank API/CSV)
transactions = [
    {"date": "2023-10-01", "amount": 21000, "description": "Rental Income - Property A"},
    {"date": "2023-10-05", "amount": -8000, "description": "CAPE TOWN RENT"},
    {"date": "2023-10-10", "amount": -3000, "description": "Medical Aid"},
]

def track_income(transactions):
    # Parse transactions
    df = pd.DataFrame(transactions)
    rental_income = df[df["description"].str.contains("Rental Income")]["amount"].sum()
    ct_expenses = df[df["description"].str.contains("CAPE TOWN")]["amount"].sum()
    
    # Calculate net
    net = rental_income + ct_expenses  # Expenses are negative
    safety_net = 0.3 * rental_income  # 30% buffer
    
    # Generate report
    report = f"""
    📊 Passive Income Report ({datetime.now().strftime('%Y-%m-%d')})
    ----------------------------------
    ✅ Rental Income: R{rental_income}
    💸 Cape Town Costs: R{abs(ct_expenses)}
    🔥 Net Savings: R{net}
    🚨 Safety Buffer: R{safety_net} (30% of income)
    """
    print(report)
    
    # SMS Alert if funds low (optional)
    if net < safety_net:
        send_alert(f"Warning: Net savings (R{net}) below safety buffer!")

def send_alert(message):
    # Twilio setup (add your credentials)
    account_sid = "YOUR_TWILIO_SID"
    auth_token = "YOUR_TWILIO_TOKEN"
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_="+123456789",  # Your Twilio number
        to="+YOUR_PHONE_NUMBER"
    )

track_income(transactions)