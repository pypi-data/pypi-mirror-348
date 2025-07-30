import paths

run_cases = [
    ('', ''),
    ('my_file', 'my_file'),
    ('my_file.txt', 'my_file'),
    ('parent/my_file.sql', 'my_file'),
    ('multiple/parent/dirs/my_file.sql', 'my_file'),
    ('parent/my_file', 'my_file'),
    ('my_file.', 'my_file'),
]


def test(file_path, expected_output):
    print('---------------------------------')
    print(f'Inputs: {file_path}')
    print(f'Expecting: {expected_output}')
    result = paths.file_name(file_path)
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
