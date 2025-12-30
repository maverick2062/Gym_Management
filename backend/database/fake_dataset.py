import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# We will generate data for the last 90 days
DAYS_TO_GENERATE = 90
NUM_MEMBERS = 180
GYM_OPEN_HOUR = 6  # 6 AM
GYM_CLOSE_HOUR = 22 # 10 PM

# Peak hours are usually 6-9 AM and 6-9 PM
PEAK_MORNING = [6, 7, 8, 9]
PEAK_EVENING = [17, 18, 19, 20, 21]

def generate_dummy_data():
    print("Generating gym traffic data... this may take a moment.")
    
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_TO_GENERATE)
    
    current_date = start_date
    while current_date <= end_date:
        # Logic: Weekends are less busy than Weekdays
        is_weekend = current_date.weekday() >= 5
        daily_traffic_factor = 0.6 if is_weekend else 1.0
        
        # For each hour the gym is open
        for hour in range(GYM_OPEN_HOUR, GYM_CLOSE_HOUR):
            # Base probability of a member entering
            prob_entry = 0.1 
            
            # Increase probability during peak hours
            if hour in PEAK_MORNING or hour in PEAK_EVENING:
                prob_entry = 0.3
            
            # Adjust for weekend
            prob_entry *= daily_traffic_factor
            
            # Simulate members entering
            num_entries = np.random.binomial(n=NUM_MEMBERS, p=prob_entry)
            
            for _ in range(num_entries):
                # Create a timestamp with random minute/second
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                entry_time = current_date.replace(hour=hour, minute=minute, second=second)
                
                # Random member ID
                member_id = random.randint(100, 100 + NUM_MEMBERS)
                
                data.append({
                    "timestamp": entry_time,
                    "member_id": member_id,
                    "event_type": "swipe_in"
                })
                
                # Simulate swipe_out (45 mins to 90 mins later)
                duration_minutes = random.randint(45, 90)
                exit_time = entry_time + timedelta(minutes=duration_minutes)
                
                if exit_time.hour < GYM_CLOSE_HOUR:
                     data.append({
                        "timestamp": exit_time,
                        "member_id": member_id,
                        "event_type": "swipe_out"
                    })

        current_date += timedelta(days=1)

    # Convert to DataFrame and sort
    df = pd.DataFrame(data)
    df = df.sort_values(by="timestamp")
    
    # Save to CSV
    filename = "gym_traffic_data.csv"
    df.to_csv(filename, index=False)
    print(f"Success! Generated {len(df)} records in '{filename}'")
    print("You can now load this file into Pandas to start your analysis.")

if __name__ == "__main__":
    generate_dummy_data()