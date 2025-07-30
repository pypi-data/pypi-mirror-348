import requests
import sys
import signal
from typing import List, Optional

# Configuration
TOGETHER_API_KEY = "09d5da1182a2ed227fef31fc35447dbd613937babe59f5acfcd267e7f8d45754"
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
API_URL = "https://api.together.xyz/v1/chat/completions"
MAX_RETRIES = 3
TIMEOUT = 30  # seconds

class MCQAnalyzer:
    def __init__(self):
        if not TOGETHER_API_KEY:
            raise ValueError("API key cannot be empty")
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def handle_interrupt(self, signum, frame):
        print("\n\nGracefully shutting down...")
        sys.exit(0)

    def format_question(self, question: str) -> str:
        return f"""
{question}

Analyze this MCQ and provide only:
1. The option letter/number followed by the complete option text
2. Your confidence level in the answer (as a percentage)
3. User may enter the question in any format, You understand the question and provide the answer in the format below.
Format your response exactly like this:
Answer: [Option Letter/Number] [Option Text]
Confidence: [XX]%"""

    def get_ai_response(self, full_question: str) -> str:
        formatted_question = self.format_question(full_question)
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [{
                "role": "user",
                "content": formatted_question
            }],
            "temperature": 0.7,
            "max_tokens": 200,
            "stop": ["</s>"]
        }

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    API_URL, 
                    headers=headers, 
                    json=payload, 
                    timeout=TIMEOUT
                )
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except requests.exceptions.Timeout:
                if attempt == MAX_RETRIES - 1:
                    return "Error: Request timed out. Please try again."
                continue
            except requests.exceptions.RequestException as e:
                return f"Network Error: {str(e)}"
            except (KeyError, ValueError) as e:
                return f"API Response Error: {str(e)}"
            except Exception as e:
                return f"Unexpected Error: {str(e)}"

    def get_user_input(self) -> Optional[List[str]]:
        print("(Type your question and press Enter, type 'q' to exit)")
        try:
            line = input().strip()
            if line.lower() == 'q':
                return None
            if not line:
                return []
            return [line]
        except EOFError:
            print("\nEOF detected. Exiting...")
            sys.exit(0)

    def display_banner(self):
        print("\n" + "="*50)
        print("MCQ Analysis AI Assistant (Type 'q' to exit)")
        print("="*50)

def main():
    try:
        analyzer = MCQAnalyzer()
        analyzer.display_banner()
        
        while True:
            print("\nEnter your MCQ:")
            lines = analyzer.get_user_input()
            
            if lines is None:
                print("\nThank you for using MCQ Analyzer!")
                break
                
            if not lines:
                print("Error: Empty input. Please provide a question.")
                continue
                
            if len("".join(lines).strip()) < 10:
                print("Error: Input too short. Please provide a complete question.")
                continue
                
            full_question = "\n".join(lines)
            print("\nAnalyzing your question...")
            answer = analyzer.get_ai_response(full_question)
            
            print("\n" + "="*20 + " AI Response " + "="*20)
            print(answer)
            print("="*50 + "\n")

    except KeyboardInterrupt:
        print("\n\nThank you for using MCQ Analyzer!")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()