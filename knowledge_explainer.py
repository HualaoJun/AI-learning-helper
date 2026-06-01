from typing import List, Dict
from deepseek_api import DeepSeekAPI

class KnowledgeExplainer:
    def __init__(self, api_key: str, proxy=None, verify_ssl=True):
        self.api = DeepSeekAPI(api_key, proxy=proxy, verify_ssl=verify_ssl)

    def ask_familiarity(self, point_name: str) -> str:
        question_prompt = f"""You are a programming teacher. Ask the student if they are familiar with the following concept:
- Name: {point_name}

Use 1-2 sentences to briefly describe what this concept is.
End with asking if they are familiar (yes/no).

IMPORTANT: Respond in Chinese (Simplified)."""

        response = self.api.chat_completion([
            {"role": "user", "content": question_prompt}
        ])
        return self.api.extract_content(response)

    def explain_concept(self, point_name: str, code_context: str = "") -> str:
        explanation_prompt = f"""You are a patient programming teacher. Please explain the following programming concept:
- Name: {point_name}

User code context:
{code_context}

Please provide:
1. A clear explanation (2-3 paragraphs)
2. The most common use cases
3. A simple code example
4. Related syntax or variations

Be educational and beginner-friendly.
IMPORTANT: Respond in Chinese (Simplified)."""

        response = self.api.chat_completion([
            {"role": "user", "content": explanation_prompt}
        ])
        return self.api.extract_content(response)

    def ask_extended_usage(self, point_name: str) -> str:
        more_prompt = f"""For the concept "{point_name}", do you want to learn more about:
1. Extended usage scenarios
2. Common pitfalls and how to avoid them
3. Advanced variations

If you want more info, answer "yes" or "more", otherwise answer "skip".
IMPORTANT: Respond in Chinese (Simplified)."""

        response = self.api.chat_completion([
            {"role": "user", "content": more_prompt}
        ])
        return self.api.extract_content(response)

    def explain_extended(self, point_name: str) -> str:
        extended_prompt = f"""Please provide extended information about the concept "{point_name}" including:
1. Extended usage scenarios
2. Common pitfalls and how to avoid them
3. Advanced variations and alternative approaches
4. Performance considerations

Be comprehensive but clear.
IMPORTANT: Respond in Chinese (Simplified)."""

        response = self.api.chat_completion([
            {"role": "user", "content": extended_prompt}
        ])
        return self.api.extract_content(response)

    def explain_knowledge_points(self, same_points: List[Dict], code_context: str = "") -> dict:
        result = {
            "success": False,
            "explanations": [],
            "user_choices": {},
            "error": ""
        }

        if not same_points:
            print("No knowledge points to explain.")
            result["success"] = True
            return result

        print(f"\n[Step 4] Checking knowledge point familiarity for {len(same_points)} points...")

        explanations = []
        user_choices = {}

        for i, point in enumerate(same_points, 1):
            point_name = point.get('name', '')
            print(f"\n{'='*60}")
            print(f"Knowledge Point {i}/{len(same_points)}: {point_name}")
            print(f"{'='*60}")

            content = self.ask_familiarity(point_name)

            if content:
                print(f"\nAI: {content}")

                user_answer = input("\nYour answer (yes/no): ").strip().lower()

                if user_answer in ['no', 'n']:
                    print("\n[Explaining this knowledge point...]")

                    exp_content = self.explain_concept(point_name, code_context)

                    if exp_content:
                        explanations.append({
                            "point": point_name,
                            "explanation": exp_content
                        })
                        print(f"\n{'='*60}")
                        print(f"EXPLANATION: {point_name}")
                        print(f"{'='*60}")
                        print(exp_content)
                        print(f"{'='*60}\n")

                        more_content = self.ask_extended_usage(point_name)

                        if more_content:
                            print(f"\nAI: {more_content}")

                            user_wants_more = input("\nDo you want more details? (more/skip): ").strip().lower()

                            if user_wants_more.startswith('more') or user_wants_more in ['m', 'yes', 'y']:
                                ext_content = self.explain_extended(point_name)

                                if ext_content:
                                    explanations[-1]["extended"] = ext_content
                                    print(f"\n{'='*60}")
                                    print(f"EXTENDED EXPLANATION: {point_name}")
                                    print(f"{'='*60}")
                                    print(ext_content)
                                    print(f"{'='*60}\n")
                        else:
                            user_choices[point_name] = "explained_no_extended"
                    else:
                        result["error"] = f"Failed to explain: {point_name}"
                        return result
                else:
                    print(f"\n[Skipping: {point_name}]")
                    user_choices[point_name] = "familiar"

        result["explanations"] = explanations
        result["user_choices"] = user_choices
        result["success"] = True
        return result

def main():
    print("=" * 60)
    print("AI Code Learning Assistant - Knowledge Explainer")
    print("=" * 60)

    api_key = input("\nPlease enter DeepSeek API Key: ").strip()

    if not api_key:
        print("API Key cannot be empty!")
        return

    explainer = KnowledgeExplainer(api_key)

    print("\n" + "-" * 60)
    print("Sample same_points from previous analysis:")
    print("-" * 60)

    sample_points = [
        {"name": "C++ Templates", "description": "Generic programming in C++"},
        {"name": "STL Vector", "description": "Dynamic array container"}
    ]

    for point in sample_points:
        print(f"- {point['name']}: {point['description']}")

    code_context = """#include <vector>
template<class T>
class Stack {
    std::vector<T> data;
public:
    void push(const T& item) { data.push_back(item); }
};"""

    print("\n" + "-" * 60)
    print("Code context for this session:")
    print("-" * 60)
    print(code_context)

    print("\n" + "=" * 60)
    print("Starting knowledge explanation...")
    print("=" * 60)

    result = explainer.explain_knowledge_points(sample_points, code_context)

    if result["success"]:
        print("\n" + "=" * 60)
        print("Session Summary")
        print("=" * 60)
        print(f"Total points reviewed: {len(sample_points)}")
        print(f"Explained: {len(result['explanations'])}")
        print(f"Skipped (familiar): {sum(1 for v in result['user_choices'].values() if v == 'familiar')}")
    else:
        print(f"\nError: {result['error']}")

if __name__ == "__main__":
    main()