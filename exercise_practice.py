from typing import List, Dict
import subprocess
import tempfile
import os
from deepseek_api import DeepSeekAPI

class ExercisePractice:
    def __init__(self, api_key: str, proxy=None, verify_ssl=True):
        self.api = DeepSeekAPI(api_key, proxy=proxy, verify_ssl=verify_ssl)

    def generate_fill_blank_exercise(self, knowledge_point: str, code_context: str = "") -> dict:
        prompt = f"""Create a C++ fill-in-the-blank exercise for this knowledge point:
- Topic: {knowledge_point}

IMPORTANT: Generate a NEW, ORIGINAL exercise. Do NOT copy or heavily borrow from any existing code provided by the user. Create something fresh that tests understanding.

REQUIREMENTS:
1. Generate a NEW, ORIGINAL C++ code example (different from user's code)
2. Hide EXACTLY 1 ESSENTIAL part using >>>[FILL_HERE]<<< as the placeholder
3. The blank MUST be the KEY concept that user needs to understand
4. Focus on testing deep understanding, NOT trivial syntax
5. Use clear, simple code that highlights the core concept

Output format in JSON ONLY:
{{
    "title": "Descriptive exercise title",
    "description": "Fill in the >>>[FILL_HERE]<<< placeholder in the code",
    "exercise_code": "The code with >>>[FILL_HERE]<<< marked clearly",
    "blanks_count": 1,
    "expected_output": "What the program should output (if applicable)",
    "hints": ["Hint 1 about the concept", "Hint 2 about how to approach"]
}}

CRITICAL:
- Use >>>[FILL_HERE]<<< as the placeholder (with arrows for visibility)
- Generate FRESH, ORIGINAL code (do not copy from user's code)
- The [FILL_HERE] should be in a NOTABLE, VISIBLE location
- Do NOT include solution code
- Make hints helpful but not revealing the answer
- Output ONLY valid C++ code without markdown tags
- RESPOND IN CHINESE (Simplified)"""

        response = self.api.chat_completion([
            {"role": "user", "content": prompt}
        ])
        content = self.api.extract_content(response)

        if content:
            import json
            import re
            try:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    data.pop('complete_code', None)
                    return data
            except json.JSONDecodeError:
                pass

        return {}

    def verify_answer_only(self, exercise: dict, exercise_code: str, user_answer: str) -> dict:
        prompt = f"""You are verifying a student's answer for a C++ fill-in-the-blank exercise.

Exercise Title: {exercise.get('title', '')}
Exercise Description: {exercise.get('description', '')}

Original exercise code (with >>>[FILL_HERE]<<< placeholder):
{exercise_code}

Student's answer (what they filled in for >>>[FILL_HERE]<<<):
{user_answer}

Please analyze:
1. Is the answer syntactically correct C++ code?
2. Does it fit logically in the [FILL_HERE] position?
3. Is it the correct solution for the exercise?
4. If wrong, give helpful hints WITHOUT revealing the answer

Output format:
{{
    "correct": true/false,
    "feedback": "Your feedback to the student",
    "hints": ["hint 1", "hint 2"]
}}

IMPORTANT:
- Do NOT compile or run code
- Focus on logical correctness of the answer
- Give hints that guide but don't give away the answer
- RESPOND IN CHINESE (Simplified)"""

        response = self.api.chat_completion([
            {"role": "user", "content": prompt}
        ])
        content = self.api.extract_content(response)

        if content:
            import json
            import re
            try:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            "correct": False,
            "feedback": "Unable to verify. Please check your answer manually.",
            "hints": []
        }

    def execute_cpp_code(self, code: str) -> dict:
        result = {
            "success": False,
            "output": "",
            "error": "",
            "compilation_error": False
        }

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                cpp_file = os.path.join(tmpdir, "exercise.cpp")
                exe_file = os.path.join(tmpdir, "exercise.exe")

                with open(cpp_file, 'w', encoding='utf-8') as f:
                    f.write(code)

                compile_result = subprocess.run(
                    ['g++', '-std=c++17', '-o', exe_file, cpp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if compile_result.returncode != 0:
                    result["compilation_error"] = True
                    result["error"] = compile_result.stderr
                    return result

                run_result = subprocess.run(
                    [exe_file],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if run_result.returncode != 0:
                    result["error"] = run_result.stderr
                else:
                    result["success"] = True
                    result["output"] = run_result.stdout

        except subprocess.TimeoutExpired:
            result["error"] = "Execution timeout"
        except Exception as e:
            result["error"] = str(e)

        return result

    def verify_with_ai(self, exercise: dict, user_code: str, execution_result: dict) -> dict:
        prompt = f"""You are grading a student's fill-in-the-blank exercise answer.

Exercise Title: {exercise.get('title', '')}
Exercise Description: {exercise.get('description', '')}
Expected Output: {exercise.get('expected_output', 'No specific output expected')}

Student's submitted code:
{user_code}

Execution result:
- Compiled successfully: {not execution_result.get('compilation_error', False)}
- Runtime success: {execution_result.get('success', False)}
- Actual output: {execution_result.get('output', 'No output')}
- Error message: {execution_result.get('error', 'None')}

Please verify:
1. Compiles and runs without errors
2. Produces correct output (if expected)
3. Fills in the blank with appropriate code
4. Uses correct syntax

IMPORTANT: Do NOT reveal solution. Focus on:
- What is correct
- What needs to be fixed (without giving away answer)
- Hints to guide them

Output format:
{{
    "correct": true/false,
    "feedback": "Your feedback to student (NO CODE SPOILERS)",
    "hints": ["additional hint if needed"]
}}

IMPORTANT: RESPOND IN CHINESE (Simplified)"""

        response = self.api.chat_completion([
            {"role": "user", "content": prompt}
        ])
        content = self.api.extract_content(response)

        if content:
            import json
            import re
            try:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            "correct": execution_result.get('success', False),
            "feedback": "Unable to verify. Please check your code manually.",
            "hints": []
        }

def main():
    print("=" * 70)
    print("AI Code Learning Assistant - Exercise Practice Module")
    print("=" * 70)

    api_key = input("\nPlease enter DeepSeek API Key: ").strip()

    if not api_key:
        print("API Key cannot be empty!")
        return

    practice = ExercisePractice(api_key)

    print("\n" + "-" * 70)
    print("Sample exercise generation for 'C++ Templates'")
    print("-" * 70)

    result = practice.generate_fill_blank_exercise(
        "C++ Templates",
        "template<class T> class Stack { ... };"
    )

    if result:
        print(f"\nTitle: {result.get('title', '')}")
        print(f"Description: {result.get('description', '')}")
        print(f"\nBlanks count: {result.get('blanks_count', 0)}")
        print(f"\nHints:")
        for i, hint in enumerate(result.get('hints', []), 1):
            print(f"  {i}. {hint}")
        print(f"\nExercise code (with blanks):")
        print("-" * 70)
        print(result.get('exercise_code', ''))
    else:
        print("\nFailed to generate exercise.")

if __name__ == "__main__":
    main()