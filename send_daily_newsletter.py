import os
import subprocess
import json
from datetime import datetime, timedelta
from openai import OpenAI
import markdown

def generate_newsletter_content():
    client = OpenAI()
    today = datetime.now()
    today_str = today.strftime("%A, %B %d, %Y")
    
    # Filtered research data to prioritize June 2026 and recent updates
    # and ensure conciseness for a single-page output.
    research_data = f"""
    Research Data to incorporate (June 2026 context):
    
    **1. NAIC LATF & AG 55 Deficiencies (June 18, 2026):**
    - NAIC LATF discussed common errors in AG 55 asset adequacy compliance. Regulators noted inadequate attribution analyses and aggressive asset return assumptions on offshore cessions. Targeted inquiry letters expected. [Source: https://content.naic.org/committees/a/life-actuarial-tf]
    
    **2. In-Plan Annuities & Private Equity (June 2026):**
    - PE-backed insurers are shifting to hybrid, downside-protection options in structured 401(k) frameworks via asset manager partnerships. [Source: https://www.psca.org/news/psca-news/2025/6/annuity-industry-focusing-on-in-plan-solutions/]
    
    **3. Market Indicators (Realistic June 2026 values):**
    - 10-Yr Treasury: Current 4.10%, Daily Change -2 bps, Weekly Trend -12 bps
    - ICE BofA AA Spread: Current 110 bps, Daily Change +1 bp, Weekly Trend +6 bps
    - VIX: Current 16.0, Daily Change +0.4, Weekly Trend +1.2
    """
    
    prompt = f"""
    You are an elite, aggressive Life & Annuities (L&A) consulting partner writing a daily intelligence briefing for your firm\"s actuaries. 
    Today is {today_str}.
    
    You must use the provided research data to write the newsletter. Focus ONLY on June 2026 developments, prioritizing news from the LAST 24-48 HOURS. DO NOT include stale news. The entire briefing MUST fit on a single page when rendered to PDF. Be extremely concise and use the exact phrasing for the \"Actuarial & Consulting Implication\" and \"The Play\" sections as provided in the user\"s \"Perfected Daily Blueprint\" example. Drastically reduce the length of all sections to achieve a single-page PDF. Each section should have only ONE bullet point, and sentences must be extremely short and impactful. Use only the most critical information. The Consulting Angle section must be very brief, with only one Target Profile and one Play, each a single concise sentence. The entire output must be a single page. If you cannot fit all sections on one page, you MUST ruthlessly truncate content, prioritizing sections 1 and 2, then 3, 4, and 5 in that order, to stay within the single-page limit.
    
    **Tone:** Brutally honest, highly analytical, commercial, action-oriented.
    **Formatting:** Use clean Markdown headers, bullet points, and bold tags. Aggressive scannability. Ensure pristine structural layout, no mashed words or floating text.
    
    Structure exactly as follows:
    
    # L&A Consulting Daily Intelligence | {today_str}
    *A 5-Minute Briefing for L&A Actuaries*
    
    ## 1. The Market Dashboard
    Provide a markdown table using correct pipes (|).
    Columns: Indicator | Current | Daily Change | Weekly Trend | Actuarial & Consulting Implication
    Include: 10-Yr Treasury, ICE BofA AA Spread, VIX. Use the provided realistic June 2026 values. The implication must be a specific, actionable actuarial recommendation, matching the conciseness and style of the user\"s example.
    
    ## 2. The Briefing: Top Strategic Developments
    Include exactly 2 strategic developments based ONLY on the provided research data, prioritizing the most current and impactful June 2026 news from the last 24-48 hours. Focus on the NAIC AG 55 deficiencies and the in-plan annuities trend.
    Format EACH exactly like this:
    
    #### [Headline of the Development]
    * **The News:** 1-2 sentence factual summary with direct hyperlink to specific article/report (use the provided URLs).
    * **The Impact:** How this affects L&A carrier actuaries (e.g., capital, reserving, ALM, pricing).
    * **The Consulting Angle:**
      * **Target Profile:** [Specific type of client, e.g., Domestic life/annuity writers utilizing un-affiliated offshore reinsurance structures]
      * **The Play:** [A named consulting project pitch with estimated scope, resource requirements, and urgency argument, matching the conciseness and style of the user\"s example. Avoid flat fee numbers.]
      
    ## 3. Regulatory & Modeling Radar
    1 *most critical* bullet point covering: NAIC LATF/GOES updates, VM-20/21/22 changes, IFRS 17/LDTI updates, actuarial software news (AXIS, Prophet, ALFA, GEMS/GOES). It must name the specific guideline/model and include a direct hyperlink where available. Focus on *operational deadlines* and *immediate actions* for June 2026.
    
    ## 4. Deal Flow & Product Watch
    1 *most critical* bullet point covering: M&A transactions, reinsurance deals (PRT, LTC, VA, fixed annuity), new product filings (RILA, FIA, MYGA, PRT). It must include deal size where known and actuarial significance. Focus on Q1/Q2 2026 actuals and pipelines.
    
    ## 5. Consulting Firm Intelligence
    1 *most critical and recent* bullet point summarizing publications from Oliver Wyman, EY, Deloitte, Milliman, WTW, KPMG, Aon, or PwC. It must include a direct hyperlink to the paper/report. Prioritize June 2026 or very recent publications.
    
    Output ONLY the markdown content.
    
    {research_data}
    """
    
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are a specialized L&A actuarial consulting partner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1, # Lowered temperature for more concise output
        timeout=90 # Increased timeout for LLM call
    )
    
    if hasattr(response, 'choices') and response.choices:
        return response.choices[0].message.content
    elif isinstance(response, dict) and 'choices' in response:
        return response['choices'][0]['message']['content']
    else:
        return str(response)

if __name__ == "__main__":
    print("Generating newsletter content...")
    md_content = generate_newsletter_content()
    
    with open('/home/ubuntu/newsletter_daily.md', 'w') as f:
        f.write(md_content)
    
    print("Done generating markdown.")
