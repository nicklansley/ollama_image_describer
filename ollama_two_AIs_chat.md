# Get two AI Assistants Chatting with Ollama API 

## This Python script enables automated chat between two different AI assistants using the Ollama API. 

## Installation
First you need to install Ollama and then download the two AI models you want to use. See: https://ollama.com/

To run the script, you need to have Python 3 installed on your system. You also need to install the requests library, which you can do using pip:

```bash
pip install requests
```

## Usage
Run the script 'ollama_teo_AIs_chat.py' using Python 3. The script will start a loop where each AI assistant takes a turn to respond in the conversation. The conversation keeps repeating until a chat count is reached.

## Code Description
### Main Function
In the script's main body, an initial variable chatting_to_ai_one is declared and set to False.
The script then enters a loop with number of chat turns dictated by number_of_chat_turns.

In each loop iteration, the chatting_to_ai_one Boolean is toggled.

If chatting_to_ai_one is True, the script sends the conversation history of AI assistant 1 to the chat_to_ai() method. 

The response from chat_to_ai() is then appended to the conversation history of both AI assistants
with the 'just responded' AI as the 'assistant' role to itself and the 'user' role to the other AI assistant.

Accordingly, both assistants retain the conversation history and can respond to the last message from the other, since it
sees the role of the other assistant as a 'user' in the latest conversation history entry.

When approaching the end of the chat, the script will send a 'goodbye' message in variable 'ai_final_chat_message' to the AI assistant that is currently chatting.

### chat_to_ai() Function
This function sends a conversation history to the Ollama API and processes the response.

It constructs headers and a payload for the API request, including the model name and the chat messages.

After sending the request, it goes into a loop where it processes each line of the response as the response streams in from the AI. If the response has a 'done' attribute set to True, the function breaks the loop and the conversation ends.
If the request fails, the function prints the status code and response text for debugging.

### Error Handling and Return Values
The function properly handles failed requests, with error messages providing context. When successful, the function returns the response chat, which is the last message received from the Ollama API.
Dependencies
The script requires Python 3 and the requests and json libraries.
License
This project is available under the MIT License.
Contributing
For any improvements or issues, please submit a pull request or create an issue.

## Saved Conversations
As the script runs, it saves the conversation history of both AI assistants in the ai_one_conversation_history and ai_two_conversation_history lists. These lists can be used to analyae the conversation 
flow and responses of the AI assistants.

## Use two different AI models
The script uses the "llama3" model by default. You can have two different models chat by naming them in the 'ai_one_model' and 'ai_two_model' variables.
Bear in mind that two different models will slow down the conversation as each model is loaded in turn.

## Add to the fun!
In the script you will see two lists of strings, ai_one_conversation_history and ai_two_conversation_history. 
These lists contain the conversation history of the two AI assistants. 

Now you can adjust the "system" prompt for each AI to change its character. In the example I have a grump and a happy AI. 

Feel free to add more conversation history to these lists to see how the AI assistants respond to different contexts as they start up.
They will assume they have had this initial conversation already and will continue from where they think they have left off.

'Curved balls' (a cricketing term!) provide a useful diversion to the chat if you find it gets a bit repetitive. Insert curved ball chats into the conversation history 
using dictionary 'curved_ball_chat_messages'. The AI will respond to this as if it is a continuation of the conversation.
I find this useful if 'The Fonz' and 'Yoda' conclude their chat early and start repetitively saying goodbye to each other!


If you provide a large value to variable 'number_of_chat_turns', you can see how the conversation evolves over time. But bear in mind that there is a prompt size limit
that varies by model - I'm owkring on how to detect this and start removing earlier chat rounds when sending the history to the model.