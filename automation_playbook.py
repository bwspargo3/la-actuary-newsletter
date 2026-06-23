import os
import subprocess
import sys

def run_automation(type):
    # Change directory to the Newsletter folder
    os.chdir('/home/ubuntu/newsletter_project/Newsletter')
    
    # Run the generator
    if type == 'daily':
        print("Generating daily newsletter...")
        subprocess.run(['python3', 'generate_daily_newsletter.py'], check=True)
    elif type == 'weekly':
        print("Generating weekly newsletter...")
        subprocess.run(['python3', 'generate_weekly_digest.py'], check=True)
    
    # Send via Gmail
    print(f"Sending {type} newsletter to bwspargo333@gmail.com...")
    subprocess.run(['python3', 'send_via_gmail.py', '--type', type, '--to', 'bwspargo333@gmail.com'], check=True)

if __name__ == "__main__":
    import datetime
    
    # Default to running both for testing as requested by user
    # "The weekly digest should only send on Fridays, but we can include it for now while we're testing."
    
    print("Starting automated newsletter run...")
    
    # Always run daily
    run_automation('daily')
    
    # Run weekly if it's Friday OR if we are in testing mode (which we are now)
    # For now, we always run both as requested.
    run_automation('weekly')
    
    print("Automation run complete.")
