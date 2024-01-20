import json
from os import listdir
from os.path import isfile, join, basename, splitext
import re
import sys


def get_test_info(file_name):
    texts = file_name.split('_')
    return {
        'test_name':  texts[0],
        'topic_name': texts[1]
    }


def get_test_subject(test_name):
    texts = re.split(r'\d+', test_name)
    return texts[0]


def read_test(file_path):
    try:
        with open(file_path, 'r') as file:
            file_basename = basename(file_path)
            test_info = get_test_info(splitext(file_basename)[0])

            return {
                'name': test_info['test_name'],
                'subject': get_test_subject(test_info['test_name']),
                'topic_name': test_info['topic_name'],
                'score': file.read()
            }
    except IOError:
        raise Exception(f'File(path: {file_path}) not found!')
    except Exception as err:
        raise Exception(f'Unexpected {err}, {type(err)}')


def read_all_tests_in_directory(dir_path):
    file_paths = [
        join(dir_path, f)
        for f in listdir(dir_path)
        if isfile(join(dir_path, f))
    ]

    return [
        read_test(fp)
        for fp in file_paths
    ]


def map_test_result_to_user_test_result_json(username, tests_result):
    tests = []

    for tr in tests_result:
        matched_test = next(
            filter(lambda t: t['name'] == tr['name'], tests),
            None
        )

        print(f'next test: {matched_test}')
        if matched_test is None:
            tests.append({
                'name': tr['name'],
                'subject': tr['subject'],
                'topics': [
                    {
                        'name': tr['topic_name'],
                        'score': tr['score'],
                    }
                ]
            })
        else:
            topics = matched_test['topics']
            matched_topic = next(
                filter(lambda t: t['name'] == tr['topic_name'], topics),
                None
            )

            if matched_topic is None:
                topics.append({
                    'name': tr['topic_name'],
                    'score': tr['score'],
                })
            else:
                matched_topic = {
                    'name': tr['topic_name'],
                    'score': tr['score'],
                }

    return json.dumps({
        'username': username,
        'total_score': 0,  # TODO: calculate total score
        'tests': tests
    })


# Run script - python ./scripts/read_data.py <username> <dir_path>
try:
    username = sys.argv[1]
    dir_path = sys.argv[2]
    print(f'Reading files in directory: {dir_path}')

    result = read_all_tests_in_directory(dir_path)
    print(f'\nRead all tests result length: {len(result)}')
    for r in result:
        print(r)

    user_test_result = map_test_result_to_user_test_result_json(
        username,
        result
    )

    print('\nCompleted map to user test result')
    print(f'User test result:\n {user_test_result}')
except Exception as err:
    print(err)
