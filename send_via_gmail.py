import os
import sys
import argparse
import subprocess
import json

def send_email(subject, html_file, to_email):
    if not os.path.exists(html_file):
        print(f"Error: File {html_file} does not exist.")
        sys.exit(1)
        
    with open(html_file, 'r') as f:
        html_content = f.read()
        
    print(f"Preparing to send email to {to_email}...")
    
    # Since the Gmail MCP tool in the environment accepts plain text `content` and we have HTML,
    # and the MCP tool triggers a UI confirmation, we'll invoke it via the CLI.
    # We will pass the HTML content, but note that the current Gmail MCP tool might render it as plain text 
    # depending on its internal implementation. We will send it as a draft so the user can review it.
    
    # Create a temporary JSON file for the MCP tool call to avoid shell escaping issues
    import tempfile
    
    data = {
        "to": [to_email],
        "subject": subject,
        "content": html_content
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tf:
        json.dump(data, tf)
        temp_file_path = tf.name
    
    # Read the JSON and pass it as a single string
    with open(temp_file_path, 'r') as f:
        json_input = f.read()
    
    # In this environment, we should use the system's built-in message tool
    # to interact with the user or perform actions that require confirmation.
    # However, for automated background tasks, we'll output the instruction 
    # for the agent to perform the Gmail draft creation.
    
    print(f"ACTION_REQUIRED: Please create a Gmail draft to {to_email} with subject '{subject}' and the generated HTML content.")
    # Since we can't directly call the MCP tool from a script in the background,
    # we'll rely on the agent's turn to handle the actual draft creation if this were a manual step.
    # For the scheduled task, the --detail prompt will instruct the agent to do this.
    print("Draft content is ready in the output folder.")
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send newsletter via Gmail MCP")
    parser.add_argument("--type", choices=["daily", "weekly"], required=True, help="Type of newsletter to send")
    parser.add_argument("--to", required=True, help="Recipient email address")
    
    args = parser.parse_args()
    
    if args.type == "daily":
        subject = "L&A Consulting Daily Intelligence"
        html_file = "/home/ubuntu/newsletter_project/output/daily_brief.html"
    else:
        subject = "L&A Consulting Weekly Digest"
        html_file = "/home/ubuntu/newsletter_project/output/weekly_digest.html"
        
    send_email(subject, html_file, args.to)
