import json
from deepseek_api import DeepSeekAPI
from prompt_engineering import PromptEngineering

class CodeAnalyzer:
    def __init__(self, api_key: str, proxy=None, verify_ssl=True):
        self.api = DeepSeekAPI(api_key, proxy=proxy, verify_ssl=verify_ssl)
        self.prompt_engineering = PromptEngineering()

    def analyze_code(self, full_code: str, highlighted_code: str = "") -> dict:
        result = {
            "success": False,
            "highlighted_knowledge": [],
            "full_code_knowledge": [],
            "comparison": {},
            "error": ""
        }

        if highlighted_code and highlighted_code.strip():
            print("[Step 1] Analyzing highlighted code knowledge points...")
            highlighted_prompt = self.prompt_engineering.get_highlighted_code_prompt(highlighted_code)
            print(f"  -> Prompt generated ({len(highlighted_prompt)} chars)")
            print("  -> Sending request to API...")
            response1 = self.api.chat_completion([
                {"role": "user", "content": highlighted_prompt}
            ])
            print("  -> Response received")
            content1 = self.api.extract_content(response1)

            if content1:
                result["highlighted_knowledge"] = self.prompt_engineering.parse_knowledge_points(content1)
                print(f"  -> Found {len(result['highlighted_knowledge'])} knowledge points")
            else:
                error_info = response1.get("error", "Unknown error")
                print(f"  -> API Error: {error_info}")
                result["error"] = f"Failed to analyze highlighted code: {error_info}"
                return result

        print("[Step 2] Analyzing full code knowledge points...")
        full_code_prompt = self.prompt_engineering.get_full_code_prompt(full_code)
        response2 = self.api.chat_completion([
            {"role": "user", "content": full_code_prompt}
        ])
        content2 = self.api.extract_content(response2)

        if content2:
            result["full_code_knowledge"] = self.prompt_engineering.parse_knowledge_points(content2)
            print(f"  -> Found {len(result['full_code_knowledge'])} knowledge points")
        else:
            error_info = response2.get("error", "Unknown error")
            print(f"  -> API Error: {error_info}")
            result["error"] = f"Failed to analyze full code: {error_info}"
            return result

        if highlighted_code and highlighted_code.strip() and result["highlighted_knowledge"]:
            print("[Step 3] Comparing analysis results...")
            comparison_prompt = self.prompt_engineering.get_comparison_prompt(
                result["highlighted_knowledge"],
                result["full_code_knowledge"]
            )
            response3 = self.api.chat_completion([
                {"role": "user", "content": comparison_prompt}
            ])
            content3 = self.api.extract_content(response3)

            if content3:
                result["comparison"] = self.prompt_engineering.parse_comparison_result(content3)
                print("  -> Comparison complete")
            else:
                error_info = response3.get("error", "Unknown error")
                print(f"  -> API Error: {error_info}")
                result["error"] = f"Failed to compare results: {error_info}"
                return result

        result["success"] = True
        return result

def main():
    print("=" * 60)
    print("AI Code Learning Assistant - Knowledge Point Analyzer")
    print("=" * 60)

    api_key = input("\nPlease enter DeepSeek API Key: ").strip()

    if not api_key:
        print("API Key cannot be empty!")
        return

    analyzer = CodeAnalyzer(api_key)

    print("\n" + "-" * 60)
    print("Please enter the complete code (press Ctrl+D to finish):")
    print("-" * 60)

    full_code_lines = []
    try:
        while True:
            line = input()
            full_code_lines.append(line)
    except EOFError:
        pass

    full_code = "\n".join(full_code_lines)

    highlighted_code = ""
    has_highlight = input("\nDo you have highlighted code? (y/n): ").strip().lower()
    if has_highlight == 'y':
        print("\nPlease enter the highlighted code (press Ctrl+D to finish):")
        print("-" * 60)
        highlighted_lines = []
        try:
            while True:
                line = input()
                highlighted_lines.append(line)
        except EOFError:
            pass
        highlighted_code = "\n".join(highlighted_lines)

    print("\n" + "=" * 60)
    print("Starting analysis...")
    print("=" * 60)

    result = analyzer.analyze_code(full_code, highlighted_code)

    if result["success"]:
        print("\n" + "=" * 60)
        print("Analysis Results")
        print("=" * 60)

        if result["highlighted_knowledge"]:
            print("\n[Highlighted Code Knowledge Points]")
            for i, kp in enumerate(result["highlighted_knowledge"], 1):
                print(f"  {i}. {kp.get('name', '')}")
                print(f"     Category: {kp.get('category', '')}")
                print(f"     Description: {kp.get('description', '')}")

        if result["full_code_knowledge"]:
            print("\n[Full Code Knowledge Points]")
            for i, kp in enumerate(result["full_code_knowledge"], 1):
                print(f"  {i}. {kp.get('name', '')}")
                print(f"     Category: {kp.get('category', '')}")
                print(f"     Description: {kp.get('description', '')}")

        if result["comparison"]:
            comp = result["comparison"]
            print("\n[Comparison Results]")
            print(f"\nSame knowledge points: {len(comp.get('same_points', []))}")
            for item in comp.get('same_points', []):
                print(f"  - {item.get('name', '')}")

            print(f"\nHighlighted-only knowledge points: {len(comp.get('highlighted_only', []))}")
            for item in comp.get('highlighted_only', []):
                print(f"  - {item.get('name', '')}")

            print(f"\nFull-code-only knowledge points: {len(comp.get('full_code_only', []))}")
            for item in comp.get('full_code_only', []):
                print(f"  - {item.get('name', '')}")

            if comp.get('conclusion'):
                print(f"\n[Analysis Conclusion]")
                print(f"  {comp['conclusion']}")
    else:
        print(f"\nAnalysis failed: {result['error']}")

if __name__ == "__main__":
    main()