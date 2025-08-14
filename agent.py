import json
from typing import Generator
from together import Together
from prompts import *
from tools import ToolRegistry
from restaurant_db import RestaurantDB
import os
import re

class ReservationAgent:
    def __init__(self):
        # self.client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
        self.tools = ToolRegistry()
        self.db = RestaurantDB()
        self.register_tools()
        self.conversation_history = []
    
    def register_tools(self):
        # available tools
        self.tools.register_tool(
            name="find_restaurants",
            description="Find restaurants matching given criteria",
            parameters={
                "cuisine": {"type": "string", "description": "Type of cuisine preferred"},
                "location": {"type": "string", "description": "Preferred neighborhood or area"},
                "party_size": {"type": "integer", "description": "Number of people in the party"},
                "date": {"type": "string", "description": "Date of reservation in YYYY-MM-DD format"},
                "time": {"type": "string", "description": "Time of reservation in HH:MM format"},
                "amenities": {"type": "string", "description": "Desired amenities (outdoor, bar, etc.)"}
            },
            function=self.db.find_restaurants
        )
        
        self.tools.register_tool(
            name="make_reservation",
            description="Make a restaurant reservation",
            parameters={
                "restaurant_id": {"type": "integer", "description": "ID of the restaurant"},
                "name": {"type": "string", "description": "Name for the reservation"},
                "party_size": {"type": "integer", "description": "Number of people in the party"},
                "date": {"type": "string", "description": "Date of reservation in YYYY-MM-DD format"},
                "time": {"type": "string", "description": "Time of reservation in HH:MM format"},
                "special_requests": {"type": "string", "description": "Any special requests"}
            },
            function=self.db.make_reservation
        )
        
        self.tools.register_tool(
            name="modify_reservation",
            description="Modify an existing reservation",
            parameters={
                "reservation_id": {"type": "string", "description": "ID of the reservation"},
                "updates": {"type": "object", "description": "Fields to update (e.g., date, time, party_size)"}
            },
            function=self.db.modify_reservation
        )

        self.tools.register_tool(
            name="cancel_reservation",
            description="Cancel an existing reservation",
            parameters={
                "reservation_id": {"type": "string", "description": "ID of the reservation to cancel"}
            },
            function=self.db.cancel_reservation
        )

    
    def process_message(self, user_input: str) -> Generator[str, None, None]:

        """
            Handles the full processing pipeline for a user message:
            1. Appends input to conversation history
            2. Uses LLM to detect user intent
            3. Extracts necessary parameters (if needed)
            4. Calls appropriate tool function (e.g., make_reservation)
            5. Streams response back to UI
        """
        if not user_input.strip():
            yield "Sorry, I didn't catch that. Please enter your reservation request again."
            return

        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Get restaurant list for the prompt
        restaurants = self.db.find_restaurants()
        restaurants_list = "\n".join(
            f"{r['id']}: {r['name']} ({r['cuisine']}, {r['location']})"
            for r in restaurants
        )
                
        # Determine intent
        intent_prompt = INTENT_PROMPT.format(
            conversation_history=json.dumps(self.conversation_history[-5:], indent=2),
            tools_description=self.tools.get_tools_description(),
            restaurants_list=restaurants_list
        )
        
        intent_response = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[{"role": "user", "content": intent_prompt}],
            temperature=0.2,
            max_tokens=500
        )
        
        intent_data = self._parse_response(intent_response.choices[0].message.content)
        if "error" in intent_data:
            yield ("Error determining intent, Please enter your request again or try rephrasing it.")
            return
        
        # Extract parameters if needed
        if intent_data.get("needs_parameters"):
            extraction_prompt = PARAMETER_EXTRACTION_PROMPT.format(
                user_input=user_input,
                intent=intent_data["intent"],
                parameters=intent_data.get("parameters", ""),
                restaurants_list=restaurants_list
            )
            
            extraction_response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.2,
                max_tokens=500
            )
            
            # Parse extracted parameters
            extracted_params = self._parse_response(extraction_response.choices[0].message.content)

            # Resolve restaurant name to ID if needed
            if intent_data.get("intent") == "make_reservation":
                if "restaurant_name" in extracted_params and "restaurant_id" not in extracted_params:
                    restaurant_matches = self.db.find_restaurants()
                    match = next(
                        (r for r in restaurant_matches if r["name"].lower() == extracted_params["restaurant_name"].lower()),
                        None
                    )
                    if match:
                        extracted_params["restaurant_id"] = match["id"]
                    else:
                        formatted_restaurants = "\n".join(
                            f"- **{r['name']}** ({r['cuisine']}, {r['location']}) — "
                            f"Capacity: {r['capacity']}, Rating: {r['rating']}, Price: {r.get('price_range', 'N/A') or 'N/A'}"
                            for r in restaurant_matches
                        )
                        yield f""" Sorry, we couldn't find any restaurant named **{extracted_params['restaurant_name']}** in our system.

                            Here are some restaurants you can choose from:

                            {formatted_restaurants}

                            Please let me know which one you'd like to book."""
                        return

                intent_data["parameters"] = extracted_params
        
        # Execute tool if applicable
        tool_response = None
        if intent_data.get("tool_to_use"):
            tool_name = intent_data["tool_to_use"]
            tool_params = intent_data.get("parameters", {})

            # Add validation before executing the tool
            if tool_name == "make_reservation":
                missing_fields = []
                for field in ["name", "party_size", "date", "time"]:
                    if not tool_params.get(field) or str(tool_params[field]).strip() in ["", "0"]:
                        missing_fields.append(field)
                
                if missing_fields:
                    yield f"To complete your reservation, please provide - Restaurant Name, Your name, Party Size, Date, and Time. Don't forget to give your - {', '.join(missing_fields)}. Make sure the restaurant comes under our list of restaurants."
                    return
        
            if "restaurant_id" in tool_params and isinstance(tool_params["restaurant_id"], str):
                # Avoiding hallucination
                tool_params["restaurant_name"] = tool_params.pop("restaurant_id")


            if tool_name == "make_reservation":
                if "restaurant_id" in tool_params and isinstance(tool_params["restaurant_id"], str):
                    restaurant_name = tool_params.pop("restaurant_id")
                    matches = self.db.find_restaurants()
                    match = next((r for r in matches if r["name"].lower() == restaurant_name.lower()), None)
                    if match:
                        tool_params["restaurant_id"] = match["id"]
                    else:
                        yield f"Sorry, I couldn't find a restaurant named '{restaurant_name}'"
                        return
            
            try:
                tool_response = self.tools.execute_tool(tool_name, tool_params)
            except Exception as e:
                tool_response = f"Error executing tool: {str(e)}"

            if isinstance(tool_response, dict) and not tool_response.get("success", True):
                error_prompt = ERROR_PROMPT.format(
                    error_message=tool_response.get("error", "An unknown error occurred")
                )
                error_response = self.client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                    messages=[{"role": "user", "content": error_prompt}],
                    temperature=0.7,
                    max_tokens=500
                )
                error_text = error_response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": error_text})
                yield error_text
                return

        # Generate final response
        response_prompt = RESPONSE_GENERATION_PROMPT.format(
            user_input=user_input,
            intent=intent_data.get("intent", ""),
            tool_response=str(tool_response) if tool_response else "No tool response",
            conversation_history=json.dumps(self.conversation_history[-3:], indent=2)
        )
        
        full_response = ""
        stream = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[{"role": "user", "content": response_prompt}],
            temperature=0.7,
            max_tokens=1000,
            stream=True
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content
        
        self.conversation_history.append({"role": "assistant", "content": full_response})
    
    def _parse_response(self, response_text: str) -> dict:

        # find a valid JSON block
        match = re.search(r"```json\s*({[\s\S]*?})\s*```", response_text, re.DOTALL)
        if not match:
            match = re.search(r"{[\s\S]*}", response_text)

        if not match:
            return {"error": "Could not parse response"}

        json_str = match.group(1) if match.lastindex else match.group(0)

        try:
            json_str = re.sub(r",\s*}", "}", json_str)
            json_str = re.sub(r",\s*\]", "]", json_str)
            parsed = json.loads(json_str)
            return parsed
        except Exception as e:
            return {"error": "Could not parse response"}
