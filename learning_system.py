from code_analyzer import CodeAnalyzer
from knowledge_explainer import KnowledgeExplainer
from exercise_practice import ExercisePractice

def main():
    print("=" * 70)
    print("AI Code Learning Assistant - Complete Learning System")
    print("=" * 70)

    api_key = input("\nPlease enter DeepSeek API Key: ").strip()

    if not api_key:
        print("API Key cannot be empty!")
        return

    code_analyzer = CodeAnalyzer(api_key)
    knowledge_explainer = KnowledgeExplainer(api_key)
    exercise_practice = ExercisePractice(api_key)

    print("\n" + "=" * 70)
    print("PART 1: Code Analysis")
    print("=" * 70)

    print("\n" + "-" * 70)
    print("Please enter the complete code (press Ctrl+D to finish):")
    print("-" * 70)

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
        print("-" * 70)
        highlighted_lines = []
        try:
            while True:
                line = input()
                highlighted_lines.append(line)
        except EOFError:
            pass
        highlighted_code = "\n".join(highlighted_lines)

    print("\n" + "=" * 70)
    print("Starting code analysis...")
    print("=" * 70)

    analysis_result = code_analyzer.analyze_code(full_code, highlighted_code)

    if not analysis_result["success"]:
        print(f"\nAnalysis failed: {analysis_result['error']}")
        return

    if not analysis_result["comparison"]:
        print("\nNo comparison result available.")
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
        return

    print("\n" + "=" * 70)
    print(f"Found {len(same_points)} common knowledge points")
    print("=" * 70)

    for i, point in enumerate(same_points, 1):
        print(f"\n{i}. {point.get('name', '')}")
        print(f"   Description: {point.get('description', '')}")

    print("\n" + "=" * 70)
    print("PART 2: Knowledge Explanation")
    print("=" * 70)

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
            print("Explanations provided for:")
            for exp in explanation_result['explanations']:
                print(f"  - {exp['point']}")
                if 'extended' in exp:
                    print(f"    (with extended information)")
        else:
            print(f"\nError during explanation: {explanation_result['error']}")

    print("\n" + "=" * 70)
    print("PART 3: Practice Exercises")
    print("=" * 70)

    print("\nThis section provides fill-in-the-blank exercises to help you")
    print("practice the knowledge points you just reviewed.")

    for exercise_point in same_points:
        point_name = exercise_point.get('name', '')

        print("\n" + "=" * 70)
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
        print(f"{'='*70}")
        print(f"\nDescription: {exercise.get('description', '')}")
        print(f"\nHints:")
        for i, hint in enumerate(exercise.get('hints', []), 1):
            print(f"  {i}. {hint}")

        print(f"\n{'='*70}")
        print("Exercise (fill in the blanks):")
        print("{'='*70}")
        print(exercise.get('exercise_code', ''))

        wants_to_attempt = input("\nDo you want to attempt this exercise? (yes/no): ").strip().lower()

        if wants_to_attempt != 'yes' and wants_to_attempt != 'y':
            print("\nSkipping exercise.")
            continue

        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            print(f"\n{'='*70}")
            print("Please complete the code (paste your answer, Ctrl+D to finish):")
            print("{'='*70}")

            user_code_lines = []
            try:
                while True:
                    line = input()
                    user_code_lines.append(line)
            except EOFError:
                pass

            user_code = "\n".join(user_code_lines)

            if not user_code.strip():
                print("\nNo code provided.")
                continue

            print("\n[Compiling and running your code...]")

            exec_result = exercise_practice.execute_cpp_code(user_code)

            if exec_result.get('compilation_error'):
                print("\n[X] Compilation Error:")
                print("-" * 70)
                print(exec_result.get('error', 'Unknown error'))
                attempts += 1
                print(f"\nAttempt {attempts}/{max_attempts}")

                if attempts >= max_attempts:
                    print("\nYou've reached the maximum number of attempts.")
                    print("Would you like to see a hint or skip to the next exercise?")

                    hint_request = input("\nType 'hint' for a hint or 'skip' to continue: ").strip().lower()
                    if hint_request == 'hint':
                        if exercise.get('hints'):
                            print("\n[Hint]:")
                            print(f"  {exercise['hints'][0]}")
                        attempts = 0
                    break

                print("\n[Getting AI feedback...]")

                verification = exercise_practice.verify_with_ai(exercise, user_code, exec_result)

                print(f"\n{'='*70}")
                print("AI Feedback:")
                print("{'='*70}")
                print(verification.get('feedback', 'No feedback available.'))

                if verification.get('hints'):
                    print("\nAdditional hints:")
                    for hint in verification['hints']:
                        print(f"  - {hint}")

                retry = input("\nTry again? (yes/no): ").strip().lower()
                if retry != 'yes' and retry != 'y':
                    break

                continue

            elif not exec_result.get('success'):
                print("\n[X] Runtime Error:")
                print("-" * 70)
                print(exec_result.get('error', 'Unknown error'))
                attempts += 1
                print(f"\nAttempt {attempts}/{max_attempts}")

                if attempts >= max_attempts:
                    print("\nYou've reached the maximum number of attempts.")

                    hint_request = input("\nType 'hint' for a hint or 'skip' to continue: ").strip().lower()
                    if hint_request == 'hint':
                        if exercise.get('hints'):
                            print("\n[Hint]:")
                            print(f"  {exercise['hints'][0]}")
                        attempts = 0
                    break

                print("\n[Getting AI feedback...]")

                verification = exercise_practice.verify_with_ai(exercise, user_code, exec_result)

                print(f"\n{'='*70}")
                print("AI Feedback:")
                print("{'='*70}")
                print(verification.get('feedback', 'No feedback available.'))

                retry = input("\nTry again? (yes/no): ").strip().lower()
                if retry != 'yes' and retry != 'y':
                    break

                continue

            else:
                print("\n[AI is verifying your answer...]")

                verification = exercise_practice.verify_with_ai(exercise, user_code, exec_result)

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

                    retry = input("\nTry again? (yes/no): ").strip().lower()
                    if retry != 'yes' and retry != 'y':
                        break

    print("\n" + "=" * 70)
    print("Learning Session Complete!")
    print("=" * 70)
    print("\nConclusion from analysis:")
    print(comparison.get("conclusion", ""))

if __name__ == "__main__":
    main()