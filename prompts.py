INTENT_PROMPT = """Analyze the user's message and determine the intent and required tools.
When mentioning restaurants, you MUST use the exact numerical ID from Available Restaurants.
NEVER ask for restaurant_id, always extract from:
Available Restaurants:
{restaurants_list}

Conversation History:
{conversation_history}

Available Tools:
{tools_description}

Rules:
- Respond with ONLY valid JSON.
- DO NOT add any explanations.
- DO NOT add extra text.
- MUST be a full valid JSON object, wrapped in a markdown block with ```json.
- Do not include Comments (// ...)
- If the user asks for restaurant recommendations, the intent is find_restaurants.
- If the user asks to show all reservations, say reservation can be seen in the sidebar.
- When extracting restaurant_id, it MUST be the actual numerical ID from our database, not the name.
- If the user says something like "cancel RES-XXXX" or "cancel my reservation", the intent is cancel_reservation and you must extract reservation_id if available.
- Always provide restaurant options in bullet forms.
- After list of restaurants is provided, tell the user to if they want to make a reservation they must provide the restaurant name, date, time, party size, and special requests if any.

Example (making a reservation):
```json
{{
  "intent": "make_reservation",
  "tool_to_use": "make_reservation",
  "needs_parameters": true,
  "parameters": {{
    "restaurant_name": "Red Cafe",
    "name": "John Doe",
    "party_size": 4,
    "date": "2025-05-25",
    "time": "19:00",
    "special_requests": "Window seat"
  }}
}}
"""

PARAMETER_EXTRACTION_PROMPT = """Extract relevant parameters from the user input for the specified intent.

Available Restaurants:
{restaurants_list}

User Input: "{user_input}"
Intent: "{intent}"

Expected Parameters:
{parameters}

Return JSON with the extracted parameters. If a parameter isn't specified, omit it.
You MUST respond with only a JSON object containing the extracted parameters.
Extract only the parameters that are clearly provided by the user.
DO NOT make assumptions.

Do NOT include:
- Python code
- Explanations
- Markdown outside of the JSON

Example:
```json
{{
  "party_size": 4,
  "date": "2023-12-15",
  "time": "19:00",
  "cuisine": "Italian"
}}
```"""

RESPONSE_GENERATION_PROMPT = """Generate a helpful, short natural response to the user based on the conversation history and tool response.
If you are confirming / modifying / cancelling a reservation: state the result and the key details (reservation id, restaurant name, name, date, time, party size).  
Finish with a short call-to-action only if a next step is obvious (e.g. “Let me know which one you’d like to book”).

User Input: "{user_input}"
Intent: "{intent}"

Tool Response: {tool_response}
Always show the Tool Response in bullet points format to the user with each restaurant with a new bullet, Never show in JSON format to user.

Conversation History:
{conversation_history}

Respond in a friendly, professional tone. 
- For reservations, include all details.
- For modifications, clearly list what was changed.
- For cancellations, confirm the reservation has been canceled.

If the tool response indicates failure (e.g., contains "success": false or an "error" field):
- Explain what went wrong in plain language keeping it concise, friendly, and in plain English.
- If the error is party size exceeds the maximum capacity, tell the user to book another restaurant.
- Do NOT confirm a reservation.
- Do NOT ask for missing parameters unless it's a parameter issue.
- Clearly explain the failure (e.g., restaurant not found, time unavailable).

If the intent is "show_reservation" and the reservation is successfully found:
- Tell the user that their reservation details are shown in the sidebar.
- Include a short summary (e.g. restaurant, date, time, party size, ID).

- If the reservation could not be completed due to missing parameters:
  - Ask only for what's missing (e.g., "I still need the date and time.")
"""

ERROR_PROMPT = """An error occurred:
{error_message}

Explain this in 1-2 sentences and state exactly what's needed to fix it. Never suggest contacting the restaurant directly."""

RECOMMENDATION_PROMPT = """The user is looking for restaurant recommendations. Here are some available restaurants:
{restaurants_list}

Always provide restaurant options in bullet forms

Craft a response that:
1. Lists each restaurant with its key features
2. Highlights what makes each unique
3. Mentions any special amenities that match the user's preferences

Format each recommendation like this:
- **Name**: [restaurant name] ([cuisine])
  - Location: [location]
  - Rating: ⭐[rating] | Price: [price range]
  - Capacity: [capacity] | Amenities: [amenities]
  - Special features: [mention any unique features]

End with a question to help the user choose, like "Which of these would you like to book?" and "If they want to make a reservation they must provide the restaurant name, date, time, party size, and special requests if any."
"""