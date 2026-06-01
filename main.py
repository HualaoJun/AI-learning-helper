from code_analyzer import CodeAnalyzer
from knowledge_explainer import KnowledgeExplainer
from exercise_practice import ExercisePractice
import os

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def read_code_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.strip().startswith('#'):
            lines = content.strip().split('\n')
            for i, line in enumerate(lines):
                if not line.strip().startswith('#') and line.strip():
                    return '\n'.join(lines[i:])
            return ""
        return content
    return ""

def reset_input_files(script_dir):
    code_input_path = os.path.join(script_dir, "code_input.txt")
    highlight_path = os.path.join(script_dir, "highlight_input.txt")

    with open(code_input_path, 'w', encoding='utf-8') as f:
        f.write("# Paste your complete code here (delete this line after pasting)\n\n")

    with open(highlight_path, 'w', encoding='utf-8') as f:
        f.write("# Paste your highlighted (confusing) code here\n# If no highlighted code, leave this file empty or delete all content above\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print_header("AI Code Learning Assistant - Complete Learning System")

    print("\n" + "-" * 70)
    print("STEP 1: Edit the following files first:")
    print("  1. code_input.txt - Paste your complete code here")
    print("  2. highlight_input.txt - Paste highlighted code (optional)")
    print("-" * 70)
    input("\nPress Enter after you have edited the files...")

    full_code_file = os.path.join(script_dir, "code_input.txt")
    highlighted_file = os.path.join(script_dir, "highlight_input.txt")

    full_code = read_code_from_file(full_code_file)
    highlighted_code = read_code_from_file(highlighted_file)

    if not full_code:
        print("\nError: No code found in code_input.txt!")
        print("Please paste your code into that file and run again.")
        input("\nPress Enter to exit...")
        return

    api_key = input("\nPlease enter DeepSeek API Key: ").strip()

    if not api_key:
        print("API Key cannot be empty!")
        return

    print("\nNetwork settings (press Enter to skip):")
    proxy = input("  Proxy server (e.g., http://127.0.0.1:8080): ").strip()
    verify_ssl = input("  Verify SSL certificate? (yes/no, default: yes): ").strip().lower()
    verify_ssl = verify_ssl != 'no'

    code_analyzer = CodeAnalyzer(api_key, proxy=proxy if proxy else None, verify_ssl=verify_ssl)
    knowledge_explainer = KnowledgeExplainer(api_key, proxy=proxy if proxy else None, verify_ssl=verify_ssl)
    exercise_practice = ExercisePractice(api_key, proxy=proxy if proxy else None, verify_ssl=verify_ssl)

    print_header("PART 1: Code Analysis")
    print("\nCode loaded successfully!")
    print(f"Full code length: {len(full_code)} characters")
    if highlighted_code:
        print(f"Highlighted code length: {len(highlighted_code)} characters")

    print_header("Starting code analysis...")

    analysis_result = code_analyzer.analyze_code(full_code, highlighted_code)

    if not analysis_result["success"]:
        print(f"\nAnalysis failed: {analysis_result['error']}")
        input("\nPress Enter to exit...")
        return

    if not analysis_result["comparison"]:
        print("\nNo comparison result available.")
        input("\nPress Enter to exit...")
        return

    comparison = analysis_result["comparison"]
    same_points = comparison.get("same_points", [])

    if not same_points:
        print("\nNo common knowledge points found between highlighted and full code.")
        print("\nAnalysis results:")
        print(f"- Highlighted code points: {len(analysis_result['highlighted_knowledge'])}")
        print(f"- Full code points: {len(analysis_result['full_code_knowledge'])}")
        print("\nConclusion from analysis:")
        print(comparison.get("conclusion", ""))

        print("\n" + "-" * 70)
        print("Resetting input files...")
        reset_input_files(script_dir)
        print("Files have been reset.")

        input("\nPress Enter to exit...")
        return

    print(f"\nFound {len(same_points)} common knowledge points")
    print("=" * 70)

    for i, point in enumerate(same_points, 1):
        print(f"\n{i}. {point.get('name', '')}")
        print(f"   Description: {point.get('description', '')}")

    print_header("PART 2: Knowledge Explanation")

    print("\nNow we will go through each knowledge point.")
    print("For each point, you will be asked if you're familiar with it.")
    print("If not familiar, you will receive an explanation.")

    proceed = input("\nProceed with explanations? (yes/no): ").strip().lower()
    if proceed != 'yes' and proceed != 'y':
        print("\nSkipping explanations.")
    else:
        explanation_result = knowledge_explainer.explain_knowledge_points(same_points, full_code)

        if explanation_result["success"]:
            print("\n" + "-" * 70)
            print("Explanations summary:")
            explained_count = len(explanation_result['explanations'])
            familiar_count = sum(1 for v in explanation_result['user_choices'].values() if v == 'familiar')
            print(f"  - Explained: {explained_count}")
            print(f"  - Already familiar: {familiar_count}")
        else:
            print(f"\nError during explanation: {explanation_result['error']}")

    print_header("PART 3: Practice Exercises")

    print("\nThis section provides fill-in-the-blank exercises.")
    print("Exercises will be generated based on the knowledge points analyzed.")

    for exercise_point in same_points:
        point_name = exercise_point.get('name', '')

        print(f"\n{'='*70}")
        print(f"Practice for: {point_name}")
        print("=" * 70)

        wants_exercise = input("\nDo you want an exercise for this concept? (yes/no): ").strip().lower()

        if wants_exercise != 'yes' and wants_exercise != 'y':
            print(f"\nSkipping exercise for: {point_name}")
            continue

        print("\n[Generating exercise...]")
        exercise = exercise_practice.generate_fill_blank_exercise(point_name, full_code)

        if not exercise:
            print(f"\nFailed to generate exercise for: {point_name}")
            continue

        print(f"\n{'='*70}")
        print(f"Title: {exercise.get('title', 'Untitled Exercise')}")
        print("=" * 70)
        print(f"\nDescription: {exercise.get('description', '')}")
        print(f"\nHints:")
        for i, hint in enumerate(exercise.get('hints', []), 1):
            print(f"  {i}. {hint}")

        print(f"\n{'='*70}")
        print("Exercise (fill in the blank):")
        print("=" * 70)
        print(exercise.get('exercise_code', ''))

        print(f"\n{'='*70}")
        print("Please fill in the >>>[FILL_HERE]<<< placeholder:")
        print("=" * 70)
        print("(Type 'skip' to skip this exercise)")

        max_attempts = 3
        attempts = 0
        exercise_code = exercise.get('exercise_code', '')

        while attempts < max_attempts:
            user_answer = input("\nYour answer: ").strip()

            if user_answer.lower() == 'skip':
                print("\nSkipping exercise.")
                break

            if not user_answer:
                print("\nNo answer provided.")
                continue

            print("\n[AI is analyzing your answer...]")
            verification = exercise_practice.verify_answer_only(exercise, exercise_code, user_answer)

            if verification.get('correct'):
                print("\n" + "=" * 70)
                print("[V] CORRECT! Great job!")
                print("=" * 70)
                print("\nFeedback:")
                print(verification.get('feedback', ''))

                more_exercises = input("\nDo you want more exercises? (yes/no): ").strip().lower()
                if more_exercises != 'yes' and more_exercises != 'y':
                    break
            else:
                print("\n[X] Not quite right.")
                print("-" * 70)
                print(verification.get('feedback', 'Check your implementation.'))

                if verification.get('hints'):
                    print("\nHints:")
                    for hint in verification['hints']:
                        print(f"  - {hint}")

                attempts += 1
                if attempts < max_attempts:
                    print(f"\nAttempt {attempts}/{max_attempts}")
                    retry = input("\nTry again? (yes/no): ").strip().lower()
                    if retry != 'yes' and retry != 'y':
                        break
                else:
                    print("\nYou've reached the maximum number of attempts.")
                    hint_request = input("\nType 'hint' for a hint or 'skip' to continue: ").strip().lower()
                    if hint_request == 'hint':
                        if exercise.get('hints'):
                            print("\n[Hint]:")
                            print(f"  {exercise['hints'][0]}")
                    break

    print_header("Learning Session Complete!")
    print("\nConclusion from analysis:")
    print(comparison.get("conclusion", ""))

    print("\n" + "-" * 70)
    print("Resetting input files...")
    reset_input_files(script_dir)
    print("Files have been reset.")

    print("\nThank you for using AI Code Learning Assistant!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()