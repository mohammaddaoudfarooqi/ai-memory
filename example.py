from memory import AIMemory
"""
Module: test.py
Description:
    This module demonstrates the usage of the AIMemory class to manage conversation
    memory in both asynchronous and synchronous manners. Messages from a user and responses
    from an AI are sent to a backend server, and the responses are retrieved and stored in JSON
    files.

Usage:
    1. Asynchronous Usage:
        - Iterates over a list of messages and sends them to the server using asynchronous
          HTTP POST requests via the 'apost' method.
        - Retrieves memory based on a query via the 'aget' method and saves the result in
          'response_asynchronous.json'.
        - Closes the AI Memory connection after operations are completed.

    2. Synchronous Usage:
        - Iterates over the same list of messages and sends them using synchronous HTTP POST
          requests via the 'post' method.
        - Retrieves memory using the 'get' method and saves the result in 'response_synchronous.json'.
        - Note: This synchronous section requires an appropriate event loop context, as it uses 'await'.

Global Variables:
    - ai_memory: Singleton instance of AIMemory configured with the base URL.
    - USER_ID: A unique string to represent the user (email address).
    - CONVERSATION_ID: Identifier for the conversation session.
    - messages: List of dictionaries, where each dictionary contains:
        - type: The message type (e.g., "human" or "ai").
        - text: The content of the message.

Notes:
    - The module assumes that the backend server is available at the specified base URL (http://0.0.0.0:8182).
    - The detailed travel recommendation text demonstrates handling multi-line strings and JSON payloads.
    - The code is structured to showcase both asynchronous and synchronous paradigms for educational purposes.
"""
import asyncio
import json

# Create an instance (only one will ever exist due to the singleton pattern)
ai_memory = AIMemory(base_url="http://0.0.0.0:8182")

USER_ID = "mohammaddaoud.farooqi@mongodb.com"
CONVERSATION_ID = "conversation_1"

messages = [
        {"type": "human", "text": "Hello."},
        {"type": "ai", "text": "Hello, how can I help you?"},
        {"type": "human", "text": "Recommend places to visit in India."},
        {
            "type": "ai",
            "text": "Let me provide you with a comprehensive guide to some of the most remarkable places to visit in India:\\n\\n1. Agra, Uttar Pradesh\\n- Home to the iconic Taj Mahal, one of the Seven Wonders of the World\\n- Features multiple UNESCO World Heritage Sites\\n- Showcases magnificent Mughal architecture\\n\\n2. Darjeeling, West Bengal\\n- Famous for its stunning mountain views and sunrise vistas\\n- Known for its world-renowned tea plantations\\n- Offers a perfect blend of natural beauty and colonial charm\\n\\n3. Hampi, Karnataka\\n- UNESCO World Heritage Site\\n- Features 500+ ancient monuments and temples\\n- Rich in historical significance with beautiful architecture\\n- Perfect for history enthusiasts and photographers\\n\\n4. Goa\\n- Popular beach destination\\n- Known for its Portuguese architecture\\n- Vibrant nightlife and water sports\\n- Beautiful beaches and churches\\n\\n5. Varanasi\\n- One of the oldest living cities in the world\\n- Spiritual capital of India\\n- Famous for its ghats along the River Ganges\\n- Rich in cultural and religious significance\\n\\n6. Kerala Region (including Munnar, Alleppey, and Kochi)\\n- Known for its backwaters and houseboats\\n- Beautiful tea plantations\\n- Ayurvedic treatments and spa resorts\\n- Rich cultural heritage\\n\\n7. Rajasthan Circuit (including Jaipur, Udaipur, Jodhpur, and Jaisalmer)\\n- Known for magnificent palaces and forts\\n- Rich cultural heritage and desert experiences\\n- Colorful markets and traditional crafts\\n- Royal heritage hotels\\n\\n8. Ladakh Region\\n- Stunning high-altitude desert landscape\\n- Buddhist monasteries and culture\\n- Adventure sports and trekking opportunities\\n- Unique wildlife viewing\\n\\n9. Wildlife Destinations:\\n- Kanha National Park - Famous for Bengal tigers\\n- Kaziranga National Park - Home to one-horned rhinoceros\\n- Jim Corbett National Park - Rich biodiversity\\n- Ranthambore National Park - Tiger reserve\\n\\n10. Hill Stations:\\n- Shimla - Former summer capital of British India\\n- Manali - Adventure sports and honeymoon destination\\n- Kodaikanal - Beautiful lakes and waterfalls\\n- Mussoorie - Queen of Hill Stations\\n\\nBest Time to Visit:\\nThe best time to visit India varies by region, but generally:\\n- October to March is the most pleasant season for most parts of India\\n- Monsoon season (July to September) is beautiful for visiting hill stations\\n- Summer (April to June) is good for visiting high-altitude areas like Ladakh\\n\\nTips:\\n- Plan your itinerary based on the season\\n- Consider the vast distances between destinations\\n- Respect local customs and dress codes\\n- Try the diverse local cuisines\\n- Book accommodations in advance during peak seasons",
        },
    ]
# Asynchronous Execution
async def main():
    for message in messages:
        payload = {"type": message["type"], "text": message["text"]}
        response = await ai_memory.apost(f"/conversation/{USER_ID}/{CONVERSATION_ID}", data=payload)
        print("Add Message Response:", response)

    response = await ai_memory.aget("/retrieve_memory/", {
        "user_id": USER_ID,
        "text": "Recommend places to visit in India.",
    })
    print("Response:", response)
    #save the json respinse to file
    with open('response_asynchronous.json', 'w') as f:
        json.dump(response, f)
    await ai_memory.close()

asyncio.run(main())


# Synchronous Execution (For Demonstration Only – Requires an Event Loop such as being called from a Fast API.)
for message in messages:
    payload = {"type": message["type"], "text": message["text"]}
    response = ai_memory.post(f"/conversation/{USER_ID}/{CONVERSATION_ID}", data=payload)
    print("Add Message Response:", response)


response = ai_memory.get("/retrieve_memory/", {
        "user_id": USER_ID,
        "text": "Recommend places to visit in India.",
    })
print("Response:", response)
#save the json respinse to file
with open('response_synchronous.json', 'w') as f:
    json.dump(response, f)



