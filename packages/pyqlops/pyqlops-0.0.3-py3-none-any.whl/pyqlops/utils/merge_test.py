from helpers import merge

run_cases = [
    (None, {'arg1': 1}, {'arg1': 1}),
    ({'arg0': 0}, {'arg1': 1}, {'arg0': 0, 'arg1': 1}),
]


def test(a, b, expected_output):
    print('---------------------------------')
    print(f'Inputs: {a, b}')
    print(f'Expecting: {expected_output}')
    result = merge(a, b)
    if result == expected_output:
        print(f'Actual: {result}')
        print('Pass')
        return True
    print(f'Actual: {result}')
    print('Fail')
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
        print('============= PASS ==============')
    else:
        print('============= FAIL ==============')


test_cases = run_cases

main()
