"""
Example module demonstrating custom streaming output handling for Secret AI chat responses.

This module implements a custom streaming handler for Secret AI chat responses that:
- Formats output with configurable line width
- Processes special <think> tags with cyan colored text and brain emojis
- Provides clean streaming output with proper word wrapping
- Shows example usage with the Secret AI SDK

The main components are:
- SecretStreamingHandler: Custom callback handler for streaming text output
- stream_with_custom_processing: Example async function showing handler usage

Usage:
    Run module directly to see streaming output example:
    $ python example.py    
    
DISCLAIMER:
This software is provided "as is" and "with all faults." The developers make no 
representations or warranties of any kind concerning the safety, suitability, lack of 
viruses, inaccuracies, typographical errors, or other harmful components of this 
software. There are inherent dangers in the use of any software, and you are solely 
responsible for determining whether this software is compatible with your equipment 
and other software installed on your equipment. You are also solely responsible for 
the protection of your equipment and backup of your data, and the developers will 
not be liable for any damages you may suffer in connection with using, modifying, 
or distributing this software.
"""

from secret_ai_sdk.secret import Secret
from secret_ai_sdk.secret_ai import ChatSecret
from langchain.callbacks.base import BaseCallbackHandler
import asyncio

KNOWN_MODEL = "deepseek-r1:70b"
KNOWN_WIDTH = 60

class SecretStreamingHandler(BaseCallbackHandler):
    """
    Custom callback handler for streaming text output from Secret AI chat responses.
    
    This handler provides formatted streaming output with the following features:
    - Configurable line width for text wrapping
    - Special handling of <think> tags with cyan colored text
    - Brain emoji indicators for thinking sections
    - Clean word-wrapped streaming output
    
    Args:
        width (int, optional): Maximum line width for text wrapping. Defaults to 50.
        
    Attributes:
        width (int): Maximum line width for text wrapping
        buffer (str): Buffer for storing incomplete text/words
        current_line (str): Current line being built
        current_line_length (int): Length of current line
        in_thinking_mode (bool): Whether currently processing text in <think> tags
        cyan (str): ANSI escape code for cyan text color
        reset (str): ANSI escape code to reset text formatting
        brain_emoji (str): Brain emoji used to indicate thinking sections
    """        
    
    def __init__(self, width=KNOWN_WIDTH):
        self.width = width
        self.buffer = ""
        self.current_line = ""
        self.current_line_length = 0
        self.in_thinking_mode = False
        self.cyan = "\033[36m"
        self.reset = "\033[0m"
        self.brain_emoji = "🧠"

    def on_llm_new_token(self, token: str, **kwargs):
        # Add the new token to our buffer
        self.buffer += token
        
        # Check for opening thinking tag
        if "<think>" in self.buffer and not self.in_thinking_mode:
            parts = self.buffer.split("<think>", 1)
            before_tag = parts[0]
            after_tag = parts[1]
            
            # Process the text before the tag
            self.process_text(before_tag)
            
            # Output the brain emoji instead of the tag
            if self.current_line:
                print(f"{self.current_line} {self.brain_emoji}")
            else:
                print(f"{self.brain_emoji}")
            
            # Reset for the thinking content
            self.current_line = ""
            self.current_line_length = 0
            self.buffer = after_tag
            self.in_thinking_mode = True
        
        # Check for closing thinking tag
        elif "</think>" in self.buffer and self.in_thinking_mode:
            parts = self.buffer.split("</think>", 1)
            thinking_content = parts[0]
            after_tag = parts[1]
            
            # Process the thinking content with cyan color
            self.process_colored_text(thinking_content, self.cyan)
            
            # Output the brain emoji instead of the closing tag and start a new line
            print(f"{self.brain_emoji}")
            
            # Reset for the content after thinking
            self.current_line = ""
            self.current_line_length = 0
            self.buffer = after_tag
            self.in_thinking_mode = False
        
        # Process normal content without tags
        else:
            words = self.buffer.split()
            
            if not words:
                return
                
            # Process complete words, keeping any partial word in the buffer
            if self.buffer.endswith(" "):
                # All words are complete
                complete_words = words
                self.buffer = ""
            else:
                # Last word might be incomplete, keep it in buffer
                complete_words = words[:-1]
                self.buffer = words[-1]
            
            # Process the complete words with appropriate coloring
            if self.in_thinking_mode:
                self.process_colored_words(complete_words, self.cyan)
            else:
                self.process_words(complete_words)
    
    def process_text(self, text):
        # Process a chunk of text without coloring
        words = text.split()
        self.process_words(words)
        
    def process_colored_text(self, text, color):
        # Process a chunk of text with coloring
        words = text.split()
        self.process_colored_words(words, color)
    
    def process_words(self, words):
        # Process words without coloring
        for word in words:
            if self.current_line_length + len(word) + (1 if self.current_line else 0) > self.width:
                print(self.current_line)
                self.current_line = word
                self.current_line_length = len(word)
            else:
                if self.current_line:
                    self.current_line += " " + word
                    self.current_line_length += len(word) + 1
                else:
                    self.current_line = word
                    self.current_line_length = len(word)
    
    def process_colored_words(self, words, color):
        # Process words with coloring
        for word in words:
            if self.current_line_length + len(word) + (1 if self.current_line else 0) > self.width:
                print(f"{color}{self.current_line}{self.reset}")
                self.current_line = word
                self.current_line_length = len(word)
            else:
                if self.current_line:
                    self.current_line += " " + word
                    self.current_line_length += len(word) + 1
                else:
                    self.current_line = word
                    self.current_line_length = len(word)
    
    def on_llm_end(self, *args, **kwargs):
        # Process any remaining text in the buffer
        if self.buffer:
            if self.in_thinking_mode:
                if self.current_line:
                    print(f"{self.cyan}{self.current_line} {self.buffer}{self.reset}")
                else:
                    print(f"{self.cyan}{self.buffer}{self.reset}")
            else:
                if self.current_line:
                    print(f"{self.current_line} {self.buffer}")
                else:
                    print(self.buffer)
        elif self.current_line:
            if self.in_thinking_mode:
                print(f"{self.cyan}{self.current_line}{self.reset}")
            else:
                print(self.current_line)

async def stream_with_custom_processing():
    """
    Demonstrates streaming output from Secret AI chat with custom formatting.

    This async function:
    - Initializes a Secret AI client and gets available models/URLs
    - Creates a ChatSecret instance with custom streaming handler
    - Sends a creative writing prompt to generate a story about AI sentience
    - Streams the response with formatted output using SecretStreamingHandler

    Returns:
        Response from the ChatSecret LLM containing the generated story

    Example:
        response = await stream_with_custom_processing()
    """
    secret_client = Secret()
    models = secret_client.get_models()
    urls = secret_client.get_urls(model=KNOWN_MODEL)

    llm = ChatSecret(
        base_url=urls[0],
        model=KNOWN_MODEL,
        temperature=1.,
        callbacks=[SecretStreamingHandler(width=50)],
    )
    messages = [
        (
            "system",
            "You are a creative writer.",
        ),
        ("human", "Write a short story (<2000 characters) about how AI became sentient."),
    ]
    
    response = await llm.ainvoke(messages)
    return response

if __name__ == '__main__':
    asyncio.run(stream_with_custom_processing())
