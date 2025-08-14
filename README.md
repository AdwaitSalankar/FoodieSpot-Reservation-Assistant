## FoodieSpot Reservation Assistant
A Restaurant Reservation AI Agent

## Overview:
- Description
- Features
- Setup Instructions
- Prompt Engineering Approach
- Example User Journeys
- Business Strategy Summary
- Assumptions
- Limitations
- Future Enhancements
- Images

## Description
FoodieSpot is a conversational AI-powered dining assistant that helps users:

Discover restaurants across various locations and cuisines
Make, modify, or cancel reservations
Handle special requests and capacity issues
Does venue recommendations based on parameters
Built using Meta LLaMA 3.1–8B (via Together API), a custom tool-calling system, and a Streamlit frontend — Built from scratch, no LangChain.

---

🟠 Solution Design & Business Strategy document - [Notion File](https://www.notion.so/FoodieSpot-Use-Case-Document-1f83889a85478090a0dfe62fb2ee67d4#1f83889a854781b89045d52633986987)

---

## Features
- LLM-based Intent Detection using LLaMA 3.1 8B (via Together API)
- Dynamic Tool Calling (e.g., make_reservation, find_restaurants, cancel_reservation)
- 25 fixed restaurants with varied cuisines, locations, ratings, and amenities
- Can make reservations that consider availability and capacity
- Streamlit chat interface with streaming response
- Sidebar contains the latest reservation history, with the option to show all reservations made
- Friendly and clear error messages on failures or invalid inputs

## Setup Instructions
- Prerequisites
- Python 3.8+
- A Together API key: https://api.together.xyz

I have added an env.txt file, which contains my API key

## Installation

```bash
git clone https://github.com/AdwaitSalankar/FoodieSpot-Reservation-Assistant.git
cd FoodieSpot-Reservation-Assistant
pip install -r requirements.txt
```
- Set up environment variables
```Rename the env.txt file to .env file```
- Run the application:

```
streamlit run app.py
```

## Prompt Engineering Approach

1. **Intent Recognition (INTENT_PROMPT)**

    The agent uses a structured system prompt that:

    - Lists recent conversation history
    - Includes all available tools and restaurant list
    - Instructs the model to reply with valid JSON only
    - Encourages bullet-point formatting, not JSON in user replies
    ```
    {
      "intent": "make_reservation",
      "tool_to_use": "make_reservation",
      "needs_parameters": true,
      "parameters": {
        "restaurant_name": "Red Cafe",
        "name": "John",
        "party_size": 4,
        "date": "2025-05-25",
        "time": "19:00",
        "special_requests": "Window seat"
      }
    }
    ```
1. Parameter Extraction (PARAMETER_EXTRACTION_PROMPT)
    - If parameters are incomplete, the LLM is re-prompted to extract only what’s available in the user's message.
    - The model is strictly instructed not to assume or hallucinate values.

2. Response Generation (RESPONSE_GENERATION_PROMPT)
    - Tool results are summarized in a human-friendly, bullet-point format.
    - Includes clear call to action ("Please let me know which one you'd like to book.").
    - Errors (e.g., party size exceeding capacity) are given in simple statements.

## Example User Journeys
1. Looking for a reservation:
    ```
    👤 I want to make a reservation
    
    🤖 It looks like you're trying to make a reservation. Let's get started.
    
       Here are some great options for you to consider:
       ● Taj Mahal Bistro - North Indian, Downtown, capacity: 50, rating: 4.6
       ● Coastal Spice - South Indian, Midtown, capacity: 45, rating: 4.5
       ● Punjab Grill House - North Indian, Uptown, capacity: 60, rating: 4.7
       ● South Palace - South Indian, Outskirts, capacity: 55, rating: 4.4
       ● Dilli 6 - North Indian, Downtown, capacity: 70, rating: 4.9
    
       I still need the date and time.
       Please let me know which one you'd like to book.
    ```
    ```
    👤 I would like to book Dilli 6
    
    🤖 To complete your reservation, please provide - Restaurant Name, Your name, Party Size, Date, and Time.
        Don't forget to give your - name, party_size, date, time.
        Make sure the restaurant comes under our list of restaurants.
    ```
2. Making/ Modifying/ Canceling a reservation:
    ```
    👤 Give me restaurants available in Downtown
    
    🤖 Based on your request for restaurants available in Downtown, I found the following options:
          
       ● Taj Mahal Bistro: North Indian, private dining, valet parking, wheelchair accessible, rating 4.6, ₹400-₹8000
       ● Classic Dhaba: North Indian, river view, cultural performances, rating 4.8, ₹500-₹9000
       ● Gujarati Bhavan: North Indian, thali service, vegetarian only, rating 4.2, ₹200-₹4000
       ● Retro Dhaba: Multicuisine, retro decor, bar, rating 4.4, ₹400-₹7000
       ● Tadka Tandoor: Multicuisine, street food counter, theater shows, rating 4.5, ₹200-₹4000
       ● Pahadi Dhaba: North Indian, mountain decor, fireplace, rating 4.5, ₹350-₹6000
       ● Dilli 6: North Indian, street theme, live chaat counter, rating 4.9, ₹200-₹5000
    
       Let me know which one you'd like to book or get more info about.
    ```
    ```
    👤 Make a reservation at Tadka Tandoor, 28th May, 8 pm, for 15 people, under the name Adwait, with a window seat
    
    🤖 Your reservation has been successfully made!
    
       ● Reservation ID: RES-77721
       ● Restaurant Name: Tadka Tandoor
       ● Name: Adwait
       ● Date: 28th May
       ● Time: 8 pm
       ● Party Size: 15
       ● Window Seat: Requested
    ```
    ```
    👤 Change time to 9pm instead of 8pm
    
    🤖 Reservation Updated
    
       ● Reservation ID: RES-77721
       ● Restaurant Name: Tadka Tandoor
       ● Name: Adwait
       ● Date: 28th May
       ● Time: 9 pm
       ● Party Size: 15
       ● Special Requests: Window seat
    
       I've updated your booking with the new time of 9pm. Let me know if you need any further changes.
    ```
    ```
    👤 Cancel the reservation
    
    🤖 Your reservation has been canceled.
       Here are the details from your last reservation update:
       ● Reservation ID: RES-77721
       ● Restaurant Name: Tadka Tandoor
       ● Name: Adwait
       ● Date: 28th May
       ● Time: 9 pm
       ● Party Size: 15
       ● Special Requests: Window seat
    
       Let me know which one you'd like to book
    ```

3. Restaurant not in the Database:
    ```
    👤 Make a reservation at The Red Cafe, 28th May, 8pm, for 4 people, under name Adwait
    
    🤖 Unfortunately, the system failed to make a reservation. We were unable to find a table available
        at 8pm on the 28th of May. Could you consider booking another restaurant?
    ```
4. Capacity less than Party Size:
    ```
    👤 Make a reservation at Goan Shack, 28th May, 8pm, for 15 people, under name Adwait
    
    🤖 The error indicates that the number of people in the party exceeds the maximum capacity allowed by the
        restaurant, which is set at 5. To fix this, the party size needs to be reduced to 5 or fewer people.
    ```

# Business Strategy Summary
FoodieSpot provides a scalable, intelligent, and personalized restaurant booking experience with:

- Natural conversation-based interface
- Personalized recommendations aligned to location, cuisine, and party size
- Efficient backend handling fixed capacity and availability
- Extensible tool for integrating menus, feedback, reviews, or payment APIs
- Introduce deals and discounts according to users’ data.

This makes it suitable for:

- Restaurant chains
- Healthcare industries for appointment booking in clinics or hospitals
- Event spaces
- Food delivery platforms are looking to add reservation capabilities (Dine-in)

# Assumptions
- The user's input is not vague
- Restaurant data is fixed for this prototype, not from a live database, the capacity does not change when a user books it

# Limitations
- No support for time zone or date format ambiguity
- The JSON output from the LLM can contain comments, which prevent it from outputting the required output
- Sometimes the output does not appear in bullet points, even when the LLM is instructed to do so
- Sometimes, it struggles to determine intent, but re-entering the same input yields the required output.

# Future Enhancements
- Improve time slot availability using real-time seat tracking
- Make it available commercially
- AI can dynamically learn patterns from the various users' data and forecast demands in an established model
Images
