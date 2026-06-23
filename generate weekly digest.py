import os
import json
from datetime import datetime
from openai import OpenAI
import markdown

def generate_weekly_content():
    client = OpenAI()
    today_str = datetime.now().strftime("%A, %B %d, %Y")

    research_data = """
    Research Data to incorporate (June 2026 Context):

    1. Deloitte 2026 Insurance Outlook: Global life insurance growth slowing, but annuities gaining momentum (12% growth in US in 2024 to $432.4B). Shift towards indexed annuities expected as rates loosen. PE investments in life insurers growing (e.g., Lincoln Financial and Bain Capital partnership). Link: https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-outlooks/insurance-industry-outlook.html

    2. Mayer Brown on Asset-Intensive Reinsurance (AIRe): Regulators tightening rules on offshore reinsurance. NAIC AG 55 adopted for 2026, requiring cash-flow testing (CFT) for AAT on offshore cessions. Brighthouse Financial acquired by Aquarian Capital for $4.1B. Corebridge and Venerable closed $51B variable annuity deal. Link: https://www.mayerbrown.com/en/insights/publications/2026/03/the-globalization-of-asset-intensive-reinsurance

    3. Milliman LTC Report: New 2025 Milliman LTC Index published. Unum continuing closed block strategy, looking for more LTC reinsurance deals. Link: https://www.milliman.com/en/insight/long-term-care-focus-q1-2026

    4. WTW on RILA: RILA sales expected to exceed $85 billion in 2026. Link: https://www.wtwco.com/en-us/insights/2024/02/registered-index-linked-annuities-how-they-work-market-growth-trends-and-outlook
    """

    prompt = f"""
    You are an elite, aggressive Life & Annuities (L&A) consulting partner writing a WEEKLY intelligence digest for your firm's actuaries.
    Today is {today_str}.

    CRITICAL FOCUS: This is the "Weekly Digest" (The Strategic Deep Dive).
    Analytical depth and comprehensive coverage are prioritized. The output should be a thorough, actionable strategic document.
    Core Question: What mid-sized projects can we structure and scope this week?

    **Tone:** Brutally honest, highly analytical, commercial, action-oriented.
    **Formatting:** Use clean Markdown headers, bullet points, and bold tags.

    Structure exactly as follows:

    # L&A Consulting Weekly Digest | {today_str}
    *Strategic Deep Dive & Pitch Playbooks*

    ## 1. The Macro Ledger (Multi-Quarter Trends)
    Provide a 2-paragraph summary of the macro environment based on the Deloitte and WTW reports. Focus on annuity growth, RILA expansion, and PE investments.

    ## 2. Regulatory Deep Dive: The Offshore Reinsurance Crackdown
    * **The Context:** Summarize the Mayer Brown report on AIRe and AG 55.
    * **The Pitch Playbook:** Detail a 3-step consulting engagement for carriers caught in the AG 55 crosshairs. Include resource scoping (e.g., "Phase 1: 2 weeks, 1 Partner, 2 Sr. Managers").

    ## 3. Block Strategy & Transaction Pipelines
    * **LTC Blocks:** Summarize the Milliman report and Unum's strategy. Provide a consulting play for mutuals holding legacy LTC.
    * **VA & Fixed Consolidation:** Mention the closed Corebridge/Venerable and Brighthouse deals as indicators of the Q3/Q4 pipeline.

    ## 4. Consulting Firm Intelligence & Competitive Vulnerability
    Summarize the key takeaways from the competitor publications provided in the research data. What are our competitors telling our clients?
    For each peer firm mentioned, add an explicit **"Vulnerability Window"** section. For example, if a firm is selling broad strategy roadmaps, tell our consultants to pitch the execution-level model validation to poke holes in that strategy.

    Output ONLY the markdown content.

    {research_data}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a specialized L&A actuarial consulting partner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


def generate_html_email(markdown_content):
    html_content = markdown.markdown(markdown_content, extensions=['tables'])

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
            background-color: #f4f7f6;
        }}
        .container {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-top: 5px solid #003366;
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
            font-size: 16px;
            margin-top: 20px;
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
                This intelligence digest is strictly confidential and intended for internal consulting use only.<br>
                Do not forward to clients without partner review.
            </div>
        </div>
    </body>
    </html>
    """
    return html_with_style


def save_outputs(markdown_content, html_content):
    os.makedirs('output', exist_ok=True)

    with open('output/weekly_digest.md', 'w') as f:
        f.write(markdown_content)

    with open('output/weekly_digest.html', 'w') as f:
        f.write(html_content)

    print("Weekly digest generated and saved to output/")


if __name__ == "__main__":
    print("Generating weekly digest...")
    md_content = generate_weekly_content()
    html_content = generate_html_email(md_content)
    save_outputs(md_content, html_content)
    print("Done!")
