from db import build_call_str

run_cases = [("usp_NoParameters", 0, "{CALL usp_NoParameters}"), 
             ("usp_OneParameter", 1, "{CALL usp_OneParameter (?)}"),
             ("usp_TwoParameters", 2, "{CALL usp_TwoParameters (?,?)}"),
             ("usp_ThreeParameters", 3, "{CALL usp_ThreeParameters (?,?,?)}")]

def test(procname, param_count, expected_output):
    print("---------------------------------")
    print(f"Inputs: {procname}")
    print(f"Expecting: {expected_output}")
    result = build_call_str(procname, param_count)
    if result == expected_output:
        print(f"Actual: {result}")
        print("Pass")
        return True
    print(f"Actual: {result}")
    print("Fail")
    return False


def main():
    passed = 0
    failed = 0
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
        else:
            failed += 1
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")

test_cases = run_cases

main()

