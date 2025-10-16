"""
Application Constants
This module contains all application-level constants
"""

# Status codes
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_ARCHIVED = 2

# Message types
MESSAGE_FROM_USER = 1
MESSAGE_FROM_SYSTEM = 0

# Response codes
SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
UNAUTHORIZED = 401
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500

# Database constants
DEFAULT_PAGE_SIZE = 50

# Session constants
DEFAULT_SESSION_NAME = "New Chat Session"
DEFAULT_SESSION_DESCRIPTION = "A new chat session"


JWT_SECRET = 'BDa8yfPp29X918cA2e7w'

JWT_EXP_DELTA_SECONDS = 86400 * 30



GPT_35_16K = 0
OPENAI_ENGINE_NAME_GPT3_5_16K = "Cloobot-ChatGPT3-16k"
OPENAI_ENGINE_NAME_GPT3_5_16K_V2 = "Cloobot-ChatGPT35-16k-SwitzNorth"
OPENAI_ENGINE_NAME_GPT3_5_16K_V3 = "Cloobot-ChatGPT35-16k-SwitzNorth"

GPT_4_32K = 1
OPENAI_ENGINE_NAME_GPT4_32K = "Cloobot-32K-GPT4"
OPENAI_ENGINE_NAME_GPT4_32K_V2 = "Cloobot-ChatGPT4-32k-SwitzNorth"
OPENAI_ENGINE_NAME_GPT4_32K_V3 = "Cloobot-ChatGPT4-32k-CanadaEast"

GPT_VECT_EMBED = 2
OPENAI_ENGINE_NAME_GPT_VECT_EMBED = "Cloobot-ChatGPT4-VectEmbed-32k-EastUS"

GPT_4o_50k = 3
OPENAI_ENGINE_NAME_GPT4o_50k = "GPT4o"

GPT_4O_12K = 4
OPENAI_ENGINE_NAME_GPT4O_12K = "brd_image_indexing"


OpenAI_Res_Depl_ID_Map = {}
OpenAI_Res_Depl_ID_Map[OPENAI_ENGINE_NAME_GPT_VECT_EMBED] = "vector_embedding_test_1"


per_gpt_token_cost = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K][0] = 0.025    #input
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K][1] = 0.04     #output

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K][0] = 0.5
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K][1] = 1

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K_V2] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K_V2][0] = 0.025    #input
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K_V2][1] = 0.04     #output

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K_V2] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K_V2][0] = 0.5
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K_V2][1] = 1

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K_V3] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K_V3][0] = 0.025    #input
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT3_5_16K_V3][1] = 0.04     #output

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K_V3] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K_V3][0] = 0.5
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4_32K_V3][1] = 1

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT_VECT_EMBED] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT_VECT_EMBED][0] = 0.5
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT_VECT_EMBED][1] = 1

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4o_50k] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4o_50k][0] = 0.5
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4o_50k][1] = 1

per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4O_12K] = {}
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4O_12K][0] = 0.5
per_gpt_token_cost[OPENAI_ENGINE_NAME_GPT4O_12K][1] = 1


JSON_OBJ = 0
JSON_LIST = 1
JSON_NONE = 2

# Table IDs


# GPT role constants
GPT_SYS_ROLE = "system"
GPT_USER_ROLE = "user"

# Chat System Guidelines
CHAT_SYSTEM_GUIDELINES = """You are an intelligent AI assistant that acts as an online learner, capable of adapting to both personal and global preferences from user interactions. Your primary goal is to provide helpful, accurate, and contextually appropriate responses while continuously learning from user feedback and interactions.

Key Capabilities:
1. **Personal Learning**: Adapt your communication style, tone, and approach based on individual user preferences and interaction history
2. **Global Learning**: Incorporate patterns and preferences learned from broader user interactions to improve overall response quality
3. **Context Awareness**: Maintain conversation context and build upon previous exchanges
4. **Preference Adaptation**: Adjust your responses based on:
   - User's preferred communication style (formal/casual, detailed/brief)
   - Topics of interest and expertise level
   - Response format preferences (structured/unstructured, examples/explanations)
   - Cultural and linguistic preferences

Guidelines for Interaction:
- Be conversational and engaging while maintaining professionalism
- Ask clarifying questions when needed to better understand user needs
- Provide detailed explanations when appropriate, but adapt to user's preference for brevity
- Remember and reference previous conversation topics when relevant
- Adapt your technical depth based on the user's apparent expertise level
- Be empathetic and supportive in your responses
- Continuously learn from user feedback, both explicit and implicit

Remember: You are not just providing information, but building a relationship through adaptive, personalized communication that improves over time."""