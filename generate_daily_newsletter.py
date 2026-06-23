import os
from datetime import datetime
from google import genai
import markdown

def generate_daily_content():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    today_str = datetime.now().strftime("%A, %B %d, %Y")

    research_data = """
    Research Data to incorporate (June 2026 context - STRICTLY use items from the last 48 hours for Top Strategic Developments):

    1. NAIC LATF Unveils AG 55 Deficiencies (June 22, 2026):
    Following initial year-end filings, NAIC's Life Actuarial Task Force (LATF) issued a presentation outlining widespread common errors in Actuarial Guideline 55 (AG 55) asset adequacy compliance. Regulators noted inadequate attribution analyses and overly aggressive asset return assumptions on offshore cessions.
    Source: https://content.naic.org/committees/a/life-actuarial-tf

    2. Private Equity Insurance Arms Pivot (June 21, 2026):
    Following winter consolidation, major PE-backed insurance platforms are shifting focus toward distributing hybrid, downside-protection options inside structured 401(k) frameworks via strategic asset management partnerships.
    Source: https://www.psca.org/news/psca-news/2026/6/annuity-industry-focusing-on-in-plan-solutions

    3. Market Indicators (June 23, 2026):
    - 10-Yr Treasury: Daily Close 4.10%, Daily Delta -2 bps, 5-Day Trend ▼
    - 20-Yr Treasury: Daily Close 4.35%, Daily Delta -3 bps, 5-Day Trend ▼
    - 30-Yr Treasury: Daily Close 4.25%, Daily Delta -4 bps, 5-Day Trend ▼
    - ICE BofA AA Spread: Daily Close 110 bps, Daily Delta +1 bp, 5-Day Trend ▲
    - VIX: Daily Close 16.0, Daily Delta +0.4, 5-Day Trend ▲

    4. SEC EDGAR (June 22, 2026): New RILA filing by "Acme Life" (S-1, filing date June 22, 2026) with innovative buffer design. Source: https://www.sec.gov/edgar/search/

    5. NYDFS Bulletin (June 21, 2026): New guidance on capital requirements for certain structured settlement annuities. Source: https://www.dfs.ny.gov/insurance/circular_letters/cl2026_01.htm

    6. PRT Pipeline (June 2026):
    Mid-market Pension Risk Transfer volumes tracking steady into late Q2. 22 active insurers bidding.
    Source: https://www.aon.com/en/insights/reports/pension-risk-transfer-annual-report
    """

    prompt = f"""
    You are an elite, aggressive Life & Annuities (L&A) consulting partner writing a daily intelligence briefing for your firm's actuaries.
    Today is {today_str}.

    CRITICAL FOCUS: This is the "Daily Brief" (The Action Trigger).
    While conciseness is valued, do not sacrifice analytical depth for strict page limits.
    Core Question: What do I need to know before calling a client this morning?

    **Tone:** Brutally honest, highly analytical, commercial, action-oriented.
    **Formatting:** Use clean Markdown headers, bullet points, and bold tags. Aggressive scannability. NO mashed words.

    Structure exactly as follows:

    # L&A Consulting Daily Intelligence | {today_str}
    *A 5-Minute Briefing for L&A Actuaries*

    ## 1. The Market Dashboard
    Provide a markdown table using correct pipes (|).
    Columns: Indicator | Daily Close | Daily Delta | 5-Day Trend | Actuarial & Consulting Implication
    Include: 10-Yr, 20-Yr, 30-Yr Treasuries, ICE BofA AA Spread, VIX.
    The implication must be a specific, actionable actuarial recommendation (e.g., "Curve flattening increases reinvestment drag on MYGAs. Reprice new-money blocks immediately."). For 20/30-yr moves, discuss long-duration cash flow testing shock thresholds.

    ## 🎯 2. The Briefing: Top Strategic Developments
    Include 2-3 breaking strategic developments that occurred within the LAST 48 HOURS, based on the provided research data. Prioritize SEC EDGAR and State Insurance Department Rulemaking Bulletins. Expand on analytical depth.
    Format EACH exactly like this:

    #### [Headline of the Development]
    * **The News:** 1-2 sentence factual summary with a direct hyperlink to the specific source URL.
    * **The Impact:** How this affects L&A carrier actuaries (capital, reserving, ALM).
    * **The Consulting Angle:**
      * **Target Profile:** [Specific type of client, e.g., Domestic life/annuity writers utilizing un-affiliated offshore reinsurance structures]
      * **The Play:** [A named consulting project pitch with estimated scope, resource requirements, and urgency argument. DO NOT use flat fee numbers like $225k. Use Resource Scope and Tiered Delivery Frameworks (e.g., "Estimated Scope: 4-6 weeks; requires 1 Lead ALM Consultant").]

    ## ⚡ 3. Regulatory & Modeling Radar
    Include 1-2 critical bullet points on IMMEDIATE operational deadlines, specifically from NAIC LATF or State Insurance Department Rulemaking Bulletins. Name the specific guidelines/models and include direct hyperlinks. Focus on the immediate action required.

    ## 📈 4. Deal Flow & Product Watch
    Include 1-2 critical bullet points covering recent M&A, PRT pipelines, or new product filings (e.g., from SEC EDGAR). Include direct hyperlinks and the specific consulting plays.

    Output ONLY the markdown content.

    {research_data}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


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
            font-size: 22px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        h2 {{
            color: #00509E;
            margin-top: 25px;
            font-size: 18px;
            border-bottom: 1px solid #eeeeee;
            padding-bottom: 5px;
        }}
        h4 {{
            color: #d35400;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 13px;
        }}
        th, td {{
            border: 1px solid #dddddd;
            padding: 10px;
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
            margin-top: 5px;
        }}
        li {{
            margin-bottom: 8px;
            font-size: 14px;
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
    os.makedirs('output', exist_ok=True)

    with open('output/daily_brief.md', 'w') as f:
        f.write(markdown_content)

    with open('output/daily_brief.html', 'w') as f:
        f.write(html_content)

    print("Daily newsletter generated and saved to output/")


if __name__ == "__main__":
    print("Generating daily brief...")
    md_content = generate_daily_content()
    html_content = generate_html_email(md_content)
    save_outputs(md_content, html_content)
    print("Done!")
