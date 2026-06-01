import json
import re
from typing import List, Dict

class PromptEngineering:
    @staticmethod
    def get_highlighted_code_prompt(highlighted_code: str) -> str:
        return PromptEngineering.generate_analysis_prompt("", highlighted_code)

    @staticmethod
    def get_full_code_prompt(full_code: str) -> str:
        return PromptEngineering.generate_analysis_prompt(full_code, "")

    @staticmethod
    def get_comparison_prompt(highlighted_knowledge: List[Dict], full_code_knowledge: List[Dict]) -> str:
        return PromptEngineering.generate_comparison_prompt(highlighted_knowledge, full_code_knowledge)

    @staticmethod
    def generate_analysis_prompt(full_code: str, highlighted_code: str = "") -> str:
        prompt = f"""You are an expert C++ programming assistant analyzing code for educational purposes.

Your task is to analyze the provided C++ code and identify knowledge points (such as data structures, algorithms, syntax features, or programming concepts).

Full Code:
{full_code}
"""
        if highlighted_code:
            prompt += f"""
Highlighted Code (user is confused about this part):
{highlighted_code}
"""
        prompt += """
Please identify the knowledge points in this code.

Output format in JSON ONLY:
{
    "knowledge_points": [
        {"name": "Point name", "description": "Brief description of this knowledge point"},
        ...
    ]
}

IMPORTANT:
- RESPOND IN CHINESE (Simplified)
- Output ONLY valid JSON, no other text
- Focus on C++ specific concepts like: arrays, pointers, classes, templates, sorting algorithms, data structures, memory management, OOP concepts, STL usage, etc."""

        return prompt

    @staticmethod
    def generate_comparison_prompt(highlighted_knowledge: List[Dict], full_code_knowledge: List[Dict]) -> str:
        highlighted_str = "\n".join([f"- {p['name']}: {p['description']}" for p in highlighted_knowledge])
        full_code_str = "\n".join([f"- {p['name']}: {p['description']}" for p in full_code_knowledge])

        prompt = f"""Compare these two sets of knowledge points and identify relationships.

Highlighted Code Knowledge Points:
{highlighted_str}

Full Code Knowledge Points:
{full_code_str}

Please analyze:
1. Which knowledge points appear in BOTH highlighted and full code? (same_points)
2. Which knowledge points appear ONLY in highlighted code? (highlighted_only)
3. Which knowledge points appear ONLY in full code? (full_code_only)
4. Provide a conclusion about where the user might be confused

Output format in JSON ONLY:
{{
    "same_points": [
        {{"name": "...", "description": "..."}},
        ...
    ],
    "highlighted_only": [
        {{"name": "...", "description": "..."}},
        ...
    ],
    "full_code_only": [
        {{"name": "...", "description": "..."}},
        ...
    ],
    "conclusion": "Comprehensive analysis of where the user has confusion"
}}"""
        return prompt

    @staticmethod
    def parse_knowledge_points(response_content: str) -> List[Dict]:
        try:
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get("knowledge_points", [])
        except Exception:
            pass

        return []

    @staticmethod
    def parse_comparison_result(response_content: str) -> Dict:
        try:
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass

        return {
            "same_points": [],
            "highlighted_only": [],
            "full_code_only": [],
            "conclusion": ""
        }