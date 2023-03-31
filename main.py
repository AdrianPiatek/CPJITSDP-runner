import datetime
import subprocess
from subprocess import STDOUT, PIPE

project_path = 'C:/Users/adria/IdeaProjects/CPJITSDP'
java_path = 'C:/Users/adria/.jdks/openjdk-19/bin/java'
number_of_tests = 1
arrId = '0'
ens = '20'
theta = '0.99'
waitingTime = '90'
filterParams = '500;50;0.7;500'
# /*** Use only for ORB ***/
paramsORB = '100;0.4;10;12;1.5;3'
datasetsName = ["tomcat", "JGroups", "spring-integration", "camel", "brackets",
                "nova", "fabric8", "neutron", "npm", "BroadleafCommerce"]
# experiments = ['ExpAIO', 'ExpFilter', 'ExpOPAIO', 'ExpOPFilter']
experiments = ['ExpAIO', 'ExpFilter', 'ExpOPAIO']
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


def create_cmd_command(exp, dataset):
    command = [java_path, '-cp', java_class_path, f'cpjitsdpexperiment.{exp}', dataset, arrId, ens, theta, waitingTime]
    if exp == 'ExpFilter':
        command.append(filterParams)
    if exp == 'ExpFilter' or exp == 'ExpOPAIO':
        command.append(paramsORB)
    return command


def run_java(java_file, dataset):
    cmd = create_cmd_command(java_file, dataset)
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


def write_to_file(data, exp_name, dataset):
    string_to_save = f'exp_name: {exp_name} Dataset: {dataset} ' \
                     f'test number: {number_of_tests} timestamp: {datetime.datetime.now()} \n' \
                     f'Average Recall(0): {data[0]} \n' \
                     f'Average Recall(1): {data[1]} \n' \
                     f'Average Diff_recalls: {data[2]} \n' \
                     f'Average Gmean between recalls: {data[3]} \n\n'
    f = open("results.txt", "a")
    f.write(string_to_save)
    f.close()


def run_tests(exp, dataset):
    results = [0, 0, 0, 0]
    for _ in range(number_of_tests):
        data = run_java(exp, str(dataset))
        data = extract_data(data)
        print(data)
        results = [res + val for res, val in zip(results, data)]
    results = [res / number_of_tests for res in results]
    write_to_file(results, exp, datasetsName[dataset])


if __name__ == '__main__':
    for experiment in experiments:
        for datasets in datasetsName:
            run_tests(experiment, datasets)
