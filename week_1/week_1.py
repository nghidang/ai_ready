import openai

client = openai.OpenAI(
    base_url="https://aiportalapi.stu-platform.live/use",
    api_key="sk-amNWISclq5ZTRgAcgOBXzw"
)

text = """
Meeting Transcript
Date: October 11, 2025
Time: 10:00 AM - 11:00 AM
Location: Virtual (Zoom)
Subject: New Product Launch Planning
Attendees:

Sarah Johnson (Project Manager, Chair)
Mark Chen (Marketing Lead)
Emily Davis (Product Developer)
Raj Patel (Operations Lead)
Lisa Wong (Finance Lead)

Transcript:
Sarah Johnson (10:00 AM): Good morning, everyone. Thanks for joining today’s meeting to discuss the launch plan for our new eco-friendly water bottle. Let’s start with a quick agenda overview: product development update, marketing strategy, operations timeline, and budget review. Any additions to the agenda?
All: (No additions)
Sarah Johnson (10:02 AM): Great, let’s begin with Emily for the product development update.
Emily Davis (10:03 AM): Thanks, Sarah. The final prototype is complete, and we’ve passed all quality tests. We’re ready to start production once operations confirms capacity. One note: we’ve sourced 90% sustainable materials, but the cap supplier is delayed by a week.
Raj Patel (10:05 AM): That’s manageable. Operations can start production by October 20th, assuming the caps arrive by then. We’ve secured two manufacturing partners, and both are prepped for a 10,000-unit initial run.
Sarah Johnson (10:07 AM): Thanks, Raj. Can you confirm the delivery timeline for retailers?
Raj Patel (10:08 AM): Yes, we’re targeting delivery to major retailers by November 15th, with smaller distributors by November 20th.
Sarah Johnson (10:09 AM): Perfect. Mark, what’s the marketing plan looking like?
Mark Chen (10:10 AM): We’ve finalized the campaign. It includes social media ads on Instagram and TikTok, a launch event on December 1st, and influencer partnerships. Budget is $50,000 for Q4. We’re also planning a pre-order page to go live November 1st. Feedback?
Lisa Wong (10:13 AM): The budget looks tight but doable. I’ve reviewed the numbers, and we’re allocating $200,000 total for the launch, including production and marketing. We need to keep marketing under $60,000 to stay on track. Can you work with that, Mark?
Mark Chen (10:15 AM): I’ll review and see where we can optimize, maybe shift some ad spend to organic content. I’ll follow up by tomorrow.
Sarah Johnson (10:17 AM): Thanks, Mark. Any risks or blockers anyone wants to flag?
Emily Davis (10:18 AM): Just the cap supplier delay. I’ll monitor it and update everyone if it impacts production.
Raj Patel (10:19 AM): From operations, we’re good as long as the supplier hits the revised timeline.
Sarah Johnson (10:20 AM): Okay, sounds like we’re aligned. Action items: Emily, keep us posted on the supplier. Mark, confirm the revised marketing budget by tomorrow. Raj, prepare a backup plan for production in case of delays. Lisa, please share the final budget breakdown by next meeting. Any other business?
All: (No additional business)
Sarah Johnson (10:22 AM): Great. Let’s wrap up early. Next meeting is October 18th at 10:00 AM. Thanks, everyone!
Meeting Adjourned: 10:23 AM
"""

prompt = f"""
Summarize the key points and action items from the following meeting transcript in a concise and organized manner. 
Focus on the main discussion points, decisions made, and specific tasks assigned to each attendee, including deadlines where applicable. 
The meeting transcript:\n\n{text}
"""
print(prompt)

response = client.chat.completions.create(
    model="GPT-5-mini",
    messages=[{"role": "user", "content": prompt}]
)
print(response.choices[0].message.content)




# ============== 1. ==============
# Meeting: New Product Launch Planning
# Date/Time: Oct 11, 2025, 10:00–10:23 AM (Zoom)
# Attendees: Sarah Johnson (PM), Mark Chen (Marketing), Emily Davis (Product), Raj Patel (Operations), Lisa Wong (Finance)

# Purpose: Plan launch of eco-friendly water bottle

# Key updates / decisions
# - Product: Final prototype complete; passed quality tests. 90% of materials are sustainable. Cap supplier delayed by one week.
# - Production: Two manufacturing partners secured; ready for initial 10,000-unit run. Operations can start production on Oct 20 if caps arrive.
# - Distribution timeline: Deliver to major retailers by Nov 15; smaller distributors by Nov 20.
# - Marketing: Campaign finalized — Instagram/TikTok ads, influencer partnerships, launch event on Dec 1. Pre-order page to go live Nov 1.
# - Budget: Total launch budget $200,000 (production + marketing). Mark proposed $50,000 for Q4 marketing; finance requests marketing be kept under $60,000.

# Risks / blockers
# - Cap supplier delay (one week) — could affect Oct 20 production start if not resolved.

# Action items
# - Emily Davis: Monitor cap supplier status and notify team of any impact (ongoing).
# - Mark Chen: Confirm revised marketing budget and optimizations (e.g., more organic content) — due by tomorrow, Oct 12.
# - Raj Patel: Prepare a backup production plan in case of supplier delay — due by next meeting, Oct 18.
# - Lisa Wong: Share final budget breakdown — due by next meeting, Oct 18.

# Next meeting: Oct 18, 2025 at 10:00 AM

# Minutes prepared by: Sarah Johnson (chair)


# ============== 2. ==============
# Summary — Key points & decisions
# - Product development: Final prototype complete; all quality tests passed. Materials are 90% sustainable. Cap supplier delayed by one week (risk).
# - Production: Operations can start production on October 20 if caps arrive on time. Two manufacturing partners are ready for an initial 10,000‑unit run.
# - Distribution timeline: Target delivery to major retailers by November 15; smaller distributors by November 20.
# - Marketing: Campaign finalized (Instagram/TikTok ads, influencer partnerships), pre‑order page to go live November 1, launch event scheduled for December 1. Q4 marketing request currently $50,000.
# - Budget: Total launch budget set at $200,000 (production + marketing). Finance requests marketing stay under $60,000 to remain within overall budget.
# - Risks: Primary blocker is the cap supplier delay; operations are contingent on revised arrival.

# Decisions made
# - Proceed with production start on October 20 assuming caps arrive.
# - Initial production run set at 10,000 units with two manufacturing partners.
# - Pre‑order page launch on November 1 and public launch event on December 1.
# - Overall launch budget capped at $200,000; marketing should be kept below $60,000.

# Action items (assigned)
# - Emily Davis (Product Developer)
#   - Monitor the cap supplier and report any impact on production to the team. (No explicit deadline; ongoing; update as needed.)
# - Mark Chen (Marketing Lead)
#   - Revise/confirm the marketing budget and optimization plan (shift to organic where possible) and report back by tomorrow (Oct 12, 2025).
# - Raj Patel (Operations Lead)
#   - Prepare a backup production plan in case of supplier delays. (Assigned in meeting; no explicit deadline given.)
#   - Confirm readiness to start production on Oct 20 and manage the 10,000‑unit run with manufacturing partners.
# - Lisa Wong (Finance Lead)
#   - Share the final budget breakdown by the next meeting (Oct 18, 2025).
# - Sarah Johnson (Project Manager)
#   - Meeting chairing / coordination; next meeting scheduled for October 18, 2025 at 10:00 AM.

# Next meeting
# - October 18, 2025 at 10:00 AM (Zoom)

# Notes / Risks to monitor
# - Cap supplier one‑week delay is the main risk to the Oct 20 production start and downstream delivery dates. Team to monitor and escalate if timelines slip.