import csv
import random
from datetime import datetime, timedelta

def generate_support_data(file_path: str, num_rows: int = 5000):
    """
    Generates synthetic call center dataset mimicking real SLA metrics,
    agent behavior profiles (AHT, CSAT, RNA), and weekly load distribution.
    """
    agents = ['Dmitriy', 'Sveta', 'Anna', 'Maria', 'Igor', 'Alex', 'Elena']
    statuses = ['Solved', 'Waiting for user info', 'Escalated (In progress)']

    categories_map = {
        'Sale': ['Refund: Other Reason/Unknown', 'How to purchase?', 'Mistyped email'],
        'Activating and Licensing': ['Activating by assigning license', 'Key blocked'],
        'Installation or Uninstallation': ['How to install?', 'Error during installation'],
        'General / Other': ['Not category', 'Non support (Prank/Drop)']
    }

    start_date = datetime(2025, 12, 1)

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Ticket_ID', 'Date', 'Time_HM', 'Agent', 'Category', 'Subcategory',
            'Status', 'Wait_Time_Sec', 'Talk_Time_Sec', 'Hold_Time_Sec', 'RNA_Accident', 'CSAT_Score'
        ])

        for i in range(num_rows):
            ticket_id = 100000 + i

            # Generate realistic date distribution (weekdays have higher volume)
            while True:
                days_offset = random.randint(0, 85)
                dt_candidate = start_date + timedelta(days=days_offset)
                weekday = dt_candidate.weekday()
                probs = {0: 1.0, 1: 0.85, 2: 0.75, 3: 0.70, 4: 0.60, 5: 0.20, 6: 0.15}
                if random.random() < probs[weekday]:
                    dt = dt_candidate
                    break

            hour = random.randint(10, 21)
            agent = random.choice(agents)

            # Agent Profiles setup
            if agent == 'Dmitriy':
                rna_prob = 0.002
                aht_base = 260
                csat_weights = [0.01, 0.01, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.3]
            elif agent in ['Igor', 'Alex']:
                rna_prob = 0.08
                aht_base = 480
                csat_weights = [0.15, 0.15, 0.15, 0.15, 0.2, 0.1, 0.05, 0.03, 0.02]
            else:
                rna_prob = 0.025
                aht_base = 340
                csat_weights = [0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.2]

            category = random.choices(list(categories_map.keys()), weights=[0.30, 0.45, 0.20, 0.05])[0]
            subcategory = random.choice(categories_map[category])
            status = random.choices(statuses, weights=[0.7, 0.2, 0.1])[0]

            is_rna = random.random() < rna_prob
            rna_text = 'Yes' if is_rna else 'No'

            # Time metrics logic
            if is_rna:
                wait_time = random.randint(45, 120)
            elif 18 <= hour <= 21:
                wait_time = int(random.triangular(30, 300, 120))
            else:
                wait_time = int(random.triangular(5, 60, 15))

            talk_time = max(60, min(int(random.gauss(aht_base, 50)), 900))

            if category in ['Installation or Uninstallation', 'Activating and Licensing'] or status == 'Escalated (In progress)':
                hold_time = random.randint(1, 4) * 150 - random.randint(10, 40) if random.random() > 0.5 else random.randint(30, 150)
            else:
                hold_time = random.randint(30, 150) if random.random() > 0.7 else 0

            csat = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9], weights=csat_weights)[0] if random.random() > 0.3 else ""

            writer.writerow([
                ticket_id, dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M'),
                agent, category, subcategory, status,
                wait_time, talk_time, hold_time, rna_text, csat
            ])

if __name__ == '__main__':
    OUTPUT_FILE = 'kaspersky_support_data.csv'
    generate_support_data(OUTPUT_FILE)