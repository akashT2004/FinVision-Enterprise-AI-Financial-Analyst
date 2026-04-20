import google.generativeai as genai
import json
import os
from typing import List, Dict, Any
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

class AnalystAgent:
    def __init__(self):
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """
        Dynamically discover an available Gemini model to avoid 404 errors.
        """
        try:
            print("--- FinVision: Discovering available AI models... ---")
            available_models = [m.name for m in genai.list_models() 
                                if 'generateContent' in m.supported_generation_methods]
            
            # Preference order: 1.5-flash, 1.5-pro, 1.0-pro
            preferred = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 
                         'models/gemini-1.5-pro', 'models/gemini-pro']
            
            selected_model = None
            for p in preferred:
                if p in available_models:
                    selected_model = p
                    break
            
            # Fallback to the first available if none of the preferred are found
            if not selected_model and available_models:
                selected_model = available_models[0]
            
            if selected_model:
                self.model = genai.GenerativeModel(selected_model)
                print(f"--- FinVision: Successfully initialized with {selected_model} ---")
            else:
                print("--- FinVision: No generative models found for this API key! ---")
        except Exception as e:
            print(f"--- FinVision: Model discovery failed: {e} ---")

    async def analyze_and_respond(self, query: str, context_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a query and retrieved context, and returns a structured response.
        """
        if not self.model:
            # Try one last-ditch re-initialization
            self._initialize_model()
            if not self.model:
                return {"answer": "AI Engine not initialized. Check API Key.", "has_chart": False, "chart_data": [], "citations": []}

        # Format context for the prompt
        context_text = "\n\n".join([
            f"Source (Doc ID: {c['document_id']}):\n{c['content']}" 
            for c in context_chunks
        ])

        prompt = f"""
        You are 'FinVision', a world-class financial analyst agent.
        
        CONTEXT:
        {context_text}
        
        USER QUERY:
        {query}
        
        TASK:
        1. Answer the query accurately based ONLY on the context provided.
        2. If the data allows for comparison or trend analysis, extract data points for a chart.
        3. STRICT DATA RULES FOR "chart_data":
           - Use ONLY raw numbers (floats or integers). 
           - DO NOT include commas, currency symbols (like $, H, Rs), or units (like "million") in the numeric fields.
           - For single-series, use "value".
           - For multi-series (e.g., Sales vs Profit), use "values" dictionary.
        4. Provide your response in valid JSON format:
           {{
             "answer": "Your detailed analytical answer with citations.",
             "has_chart": true/false,
             "chart_type": "line" | "bar" | "pie",
             "chart_data": [ 
                {{ "label": "2023", "values": {{ "Sales": 242755, "Profit": 53418 }} }} 
             ],
             "citations": [ {{ "doc_id": "...", "content_snippet": "..." }}, ... ]
           }}
        
        Ensure "chart_data" items have numeric values. SET "has_chart" to true only if "chart_data" has valid numeric entries.
        Ensure the output is ONLY the JSON object.
        """

        try:
            # Use async generation if supported, otherwise standard
            response = self.model.generate_content(prompt)
            output_text = response.text.strip()
            
            # Clean possible markdown noise
            if output_text.startswith("```json"):
                output_text = output_text[7:].split("```")[0].strip()
            elif output_text.startswith("```"):
                output_text = output_text[3:].split("```")[0].strip()
                
            data = json.loads(output_text)
            
            # Post-process: Force numeric values in chart_data regardless of nesting
            if data.get("chart_data"):
                import re
                def clean_value(val):
                    if isinstance(val, (int, float)): return val
                    if isinstance(val, str):
                        # Extract first contiguous block of numbers/decimals, ignoring commas and text
                        cleaned = val.replace(',', '')
                        match = re.search(r'-?\d+\.?\d*', cleaned)
                        if match:
                            try: return float(match.group())
                            except: pass
                    return val

                for item in data["chart_data"]:
                    # Clean direct flat values (except 'label')
                    for k, v in item.items():
                        if k not in ["label", "values"]:
                            item[k] = clean_value(v)
                            
                    # Clean nested 'values' dictionary if the AI used it
                    if "values" in item and isinstance(item["values"], dict):
                        for k, v in item["values"].items():
                            item["values"][k] = clean_value(v)
            return data
        except Exception as e:
            print(f"GEMINI ERROR: {str(e)}")
            return {
                "answer": f"Error generating analytical response: {str(e)}",
                "has_chart": False, "chart_data": [], "citations": []
            }

analyst_agent = AnalystAgent()
