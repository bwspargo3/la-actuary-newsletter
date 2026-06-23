import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from openai import OpenAI
import json
import markdown

def generate_newsletter_content():
    client = OpenAI()
    
    today_str = datetime.now().strftime("%A, %B %d, %Y")
    
    # Feeding the research data to the LLM to generate the content
    research_data = """
    Research Data to incorporate:
    1. Deloitte 2026 Insurance Outlook: Global life insurance growth slowing, but annuities gaining momentum (12% growth in US in 2024 to $432.4B). Shift towards indexed annuities expected as rates loosen. PE investments in life insurers growing (e.g., Lincoln Financial and Bain Capital partnership). Link: https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-outlooks/insurance-industry-outlook.html
    
    2. Aon 2026 PRT Annual Report: Record buy-ins and insurer capacity. $48.7B in PRT deals in 2025. Link: https://www.aon.com/en/insights/reports/pension-risk-transfer-annual-report
    
    3. Mayer Brown on Asset-Intensive Reinsurance (AIRe): Regulators tightening rules on offshore reinsurance. NAIC AG 55 adopted for 2026, requiring cash-flow testing (CFT) for AAT on offshore cessions. Brighthouse Financial acquired by Aquarian Capital for $4.1B. Corebridge and Venerable closed $51B variable annuity deal. Link: https://www.mayerbrown.com/en/insights/publications/2026/03/the-globalization-of-asset-intensive-reinsurance
    
    4. NAIC LATF & GOES: NAIC adopting new Generator of Economic Scenarios (GOES) for 2026 Valuation Manual (VM-20, VM-21, VM-22), moving from AIRG to Conning's GEMS calibration. Link: https://www.conning.com/software-and-services/naic-goes
    
    5. Milliman LTC Report: New 2025 Milliman LTC Index published. Unum continuing closed block strategy, looking for more LTC reinsurance deals. Link: https://www.milliman.com/en/insight/long-term-care-focus-q1-2026
    
    6. WTW on RILA: RILA sales expected to exceed $85 billion in 2026. Link: https://www.wtwco.com/en-us/insights/2024/02/registered-index-linked-annuities-how-they-work-market-growth-trends-and-outlook
    
    7. Athene FIA Launch: Athene launched "Athene Aviator", a new FIA with custom indices (BofA, Invesco) and simplified structure. Link: https://www.athene.com/news/annuities-news/2026/athene-launches-fixed-indexed-annuity-combining-long-term-growth-potential-with-a-simplified-customer-experience.html
    """
    
    prompt = f"""
    You are an elite, aggressive Life & Annuities (L&A) consulting partner writing a daily intelligence briefing for your firm's actuaries. 
    Today is {today_str}.
    
    You must use the provided research data to write the newsletter. DO NOT include daily market noise (like small bps changes in Treasury) in the strategic briefing.
    
    **Tone:** Brutally honest, highly analytical, commercial, action-oriented.
    **Formatting:** Use clean Markdown headers, bullet points, and bold tags. Aggressive scannability.
    
    Structure exactly as follows:
    
    # L&A Consulting Daily Intelligence | {today_str}
    
    ## 1. The Dashboard (Market Indicators & Actuarial Implications)
    Provide a markdown table using correct pipes (|).
    Columns: Indicator | Current | Change | Actuarial Implication
    Include: 10-Yr Treasury, ICE BofA AA Spread, VIX.
    (Make up realistic current values for today). The implication must be a specific actuarial action.
    
    ## 2. The Briefing: Top Strategic Developments
    Include exactly 3 strategic developments based ONLY on the provided research data.
    Format EACH exactly like this:
    
    ### [Headline of the Development] [Link to Source](insert URL from research)
    * **The News:** 2-sentence summary of the structural shift or mega-deal.
    * **The Impact:** How this affects L&A carriers (e.g., capital, reserving, ALM).
    * **The Consulting Angle:**
      * **Target Profile:** [Specific type of client, e.g., Mid-market stock companies with heavy legacy fixed annuity exposure]
      * **The Pitch:** [A named consulting project pitch. Tell the consultant exactly how to open the corporate wallet. Be highly specific.]
      
    Use these 3 topics:
    1. NAIC AG 55 Adoption & Offshore Reinsurance Scrutiny (Mayer Brown)
    2. The $51B Corebridge/Venerable VA Deal & PE Convergence (Mayer Brown / Deloitte)
    3. Athene's New FIA Launch & RILA/FIA Growth (Athene / WTW)
    
    ## 3. Regulatory & Modeling Radar
    * Bullet points on specific regulatory frameworks. Use the NAIC GOES transition for 2026 (Conning) and any IFRS 17 / LDTI modeling updates. Name the specific guidelines.
    
    ## 4. Deal Flow & Product Watch
    * Bullet points on M&A and product trends. Use the Brighthouse/Aquarian acquisition, Unum's LTC block strategy (Milliman), and the Aon PRT report.
    
    Output ONLY the markdown content.
    
    {research_data}
    """
    
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a specialized L&A actuarial consulting partner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    
    if hasattr(response, 'choices') and response.choices:
        return response.choices[0].message.content
    elif isinstance(response, dict) and 'choices' in response:
        return response['choices'][0]['message']['content']
    else:
        return str(response)

def generate_html_email(markdown_content):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables'])
    
    # Professional styling for the email
    html_with_style = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .container {{
            background-color: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #003366;
            border-bottom: 2px solid #003366;
            padding-bottom: 10px;
            font-size: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        h2 {{
            color: #00509E;
            margin-top: 30px;
            font-size: 20px;
            border-bottom: 1px solid #eeeeee;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #d35400;
            font-size: 18px;
            margin-top: 25px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #dddddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f6fa;
            color: #003366;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #fcfcfc;
        }}
        a {{
            color: #00509E;
            text-decoration: none;
            font-weight: bold;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 10px;
        }}
        strong {{
            color: #222222;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #dddddd;
            font-size: 12px;
            color: #777777;
            text-align: center;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            {html_content}
            <div class="footer">
                This intelligence briefing is strictly confidential and intended for internal consulting use only.<br>
                Do not forward to clients without partner review.
            </div>
        </div>
    </body>
    </html>
    """
    return html_with_style

def save_outputs(markdown_content, html_content):
    with open('/home/ubuntu/newsletter_v2.md', 'w') as f:
        f.write(markdown_content)
    
    with open('/home/ubuntu/newsletter_v2.html', 'w') as f:
        f.write(html_content)
        
    print("Upgraded newsletter generated and saved locally.")

if __name__ == "__main__":
    # Actually we should use the mcp tool directly here, but since we are scheduling it via manus-config, 
    # the schedule itself needs a way to send the HTML email. 
    # The current schedule uses the Gmail MCP tool via the CLI inside the detail prompt.
    # To send HTML email, the prompt in the schedule needs to be updated.
    passate_html_email(md_content)
    save_outputs(md_content, html_content)
