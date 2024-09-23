!pip install openpyxl
import streamlit as st
import pandas as pd

st.title('Traffic Update Cost Calculator')

file = st.file_uploader('Upload an Excel file', type=['xls'])

# Cost constants
FIXED_COST = 0.00405  # Fixed cost per new call
VARIABLE_COST = 0.00405  # Cost per active call at the moment a new call is received

# Function to calculate total spendings over the entire period with additional time points for cost calculations
def calculate_total_spending_over_period_with_time_checks(df_raw, time_points):
    df = df_raw.copy()
    # Calculate full received date for each call
    df['FullDataPedido'] = pd.to_datetime(df['Data'].astype(str) + ' ' + df['HoraPedido'])

    # Calculate isolated time for each ChegMedico
    df['FullDataChegMedico'] = df['HoraChegMedico']
    df['HoraChegMedico'] = df['FullDataChegMedico'].dt.time

    # Drop phone consultations
    df = df[df['HoraChegMedico'].notna()]

    # Ensure timestamps are in correct datetime format
    df['FullDataPedido'] = pd.to_datetime(df['FullDataPedido'])
    df['HoraPedido'] = df['HoraPedido'].apply(lambda x: pd.to_datetime(x).time())

    # Sort the dataframe by the time each call was received to process them in chronological order
    df = df.sort_values(by='FullDataPedido').reset_index(drop=True)

    # Initialize total spending to zero
    total_spending = 0.0

    # Loop through each call in the dataframe
    for i, row in df.iterrows():
        current_time = row['FullDataPedido']

        # Count the number of active calls at the moment this call is received
        active_calls = df[(df['FullDataPedido'] <= current_time) & (df['FullDataChegMedico'] > current_time)].shape[0]

        # Add the fixed cost for the new call
        total_spending += FIXED_COST

        # Add the variable cost for each active call (including the new one)
        total_spending += active_calls * VARIABLE_COST

    # Now apply the additional costs at the specified time points
    for time_point in time_points:
        # Convert the time point to a datetime object
        time_point_dt = pd.to_datetime(time_point, format='%H:%M:%S').time()
        for day in df['Data'].unique():
            df_day = df[df['Data'] == day]
            # Count the number of active calls at this time point
            active_calls_at_time_point = df_day[(df_day['HoraPedido'] <= time_point_dt) & (df_day['HoraChegMedico'] > time_point_dt)].shape[0]
            print(f"Active calls on {day} at {time_point}: {active_calls_at_time_point}")
            # Add n * n * VARIABLE_COST at the specified time point
            total_spending += active_calls_at_time_point * active_calls_at_time_point * VARIABLE_COST
    return total_spending

time_options = ['09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00', '18:00:00', '18:30:00', '19:00:00', '19:30:00', '20:00:00', '20:30:00', '21:00:00', '21:30:00', '22:00:00', '22:30:00', '23:00:00', '23:30:00']

time_points = st.multiselect('Update Times', time_options)

#print(f"Total spending for the 2-month period: €{total_spending:.6f}")

if st.button('Calculate'):
    st.write('Calculating...')
    df = pd.read_excel(file)
    total_spending = calculate_total_spending_over_period_with_time_checks(df, time_points)
    st.write(f"Total spending for the 2-month period: €{total_spending:.2f}")


# can I run on 1 core 1GB? <<<<
