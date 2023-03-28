import os.path
import subprocess
from subprocess import STDOUT, PIPE

project_path = 'C:/Users/adria/IdeaProjects/CPJITSDP'
java_path = 'C:/Users/adria/.jdks/openjdk-19/bin/java'
datasets = range(10)
experiments = ['ExpAIO', 'ExpFilter', 'ExpOPAIO', 'ExpOPFilter']
average_data = []
java_class_path = f'{project_path}/bin;' \
            f'{project_path}/lib/joda-time-2.9.9.jar;' \
            f'{project_path}/lib/Jama-1.0.3.jar;' \
            f'{project_path}/lib/meka-1.9.1.jar;' \
            f'{project_path}/lib/jcommon-1.0.23.jar;' \
            f'{project_path}/lib/jfreechart-1.0.19.jar;' \
            f'{project_path}/lib/commons-lang3-3.7.jar;' \
            f'{project_path}/lib/sizeofag-1.0.0.jar;' \
            f'{project_path}/lib/weka.jar;' \
            f'{project_path}/lib/commons-math3-3.6.1_2.jar;' \
            f'{project_path}/lib/fcms-widgets-0.0.13.jar;' \
            f'{project_path}/lib/jclasslocator-0.0.12.jar;' \
            f'{project_path}/lib/jshell-scripting-0.0.2.jar'


def run_java(java_file, dataset):
    cmd = [java_path, '-cp', java_class_path, java_file, dataset, '0', '20', '0.99', '90', '100;0.4;10;12;1.5;3']
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = process.communicate()
    return stdout.decode()


def extract_data(res):
    data = []

    res = [s for s in res.splitlines() if s != '']
    data_start_idx = res.index('Results*******')
    res = res[data_start_idx + 2: data_start_idx + 6]
    for result in res:
        data.append(float(result.split(':')[1].replace(',', '.')))

    return data


def run_all_datasets_for_one_exp(exp):
    results = []
    for i in datasets:
        outcome = run_java(f'cpjitsdpexperiment.{experiments[exp]}', str(i))
        data = extract_data(outcome)
        print(data)
        results.append(data)
    print(results)


if __name__ == '__main__':
    outcome = run_java(f'cpjitsdpexperiment.{experiments[3]}', '0')
    print(outcome)
    print(extract_data(outcome))
