import os
import sys
from pathlib import Path
from sovereign_control.interface import SovereignInterface
from sovereign_control.llm import LLMEngine
from sovereign_control.security import SecurityManager

class SovereignLLM:
    def __init__(self):
        self.base_path = Path(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
        self.interface = SovereignInterface()
        self.llm_engine = LLMEngine()
        self.security = SecurityManager()
        
    def initialize(self):
        """Initialize all components"""
        try:
            # Initialize security first
            self.security.initialize()
            
            # Initialize LLM engine
            self.llm_engine.load_models()
            
            # Start interface
            self.interface.setup(
                llm_engine=self.llm_engine,
                security=self.security
            )
            
            print("Sovereign LLM initialized successfully")
            return True
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            return False
    
    def run(self):
        """Run the Sovereign LLM system"""
        if self.initialize():
            try:
                # Start the system
                print("Starting Sovereign LLM...")
                self.interface.run()
            except Exception as e:
                print(f"Runtime error: {str(e)}")
                sys.exit(1)
        else:
            print("Failed to initialize Sovereign LLM")
            sys.exit(1)

def main():
    sovereign = SovereignLLM()
    sovereign.run()

if __name__ == "__main__":
    main() 