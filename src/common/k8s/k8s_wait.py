#!/usr/bin/env python3

import argparse
import subprocess
import json
import time
import sys


def k8s_getter(k8s_object_type, k8s_object_name, verbose=False):
    # Example command to query: "kubectl get deployment.app flask-injection-wrapper-deployment -o json"
    k8s_cmd = ['kubectl', 'get', k8s_object_type, k8s_object_name, '-o', 'json'],
    if verbose:
        print("k8s_command:")
        print(json.dumps(k8s_cmd, indent=4))

    try:
        k8s_get = subprocess.run(
            ['kubectl', 'get', k8s_object_type, k8s_object_name, '-o', 'json'],
            check=True, capture_output=True
        )
        k8s_get_stdout = k8s_get.stdout.decode('utf-8').strip()
        return json.loads(k8s_get_stdout)
    except subprocess.SubprocessError as e:
        if 'NotFound' in str(e.stderr):
            return {'NotFound': True}
        else:
            raise e


def wait_until(k8s_type: str, k8s_name: str, condition_test, timeout: int, verbose=False):
    while timeout >= 0:
        k8s_status_json = k8s_getter(k8s_type, k8s_name, verbose)
        try:
            if condition_test(k8s_status_json):
                return True
        except KeyError:
            pass
        print(f"Waiting for object {k8s_name} of type {k8s_type} for {timeout}s ...")
        time.sleep(1)
        timeout = timeout - 1
    return False


def parse_args():
    arg_parse = argparse.ArgumentParser(usage="Generic k8s lifecycle event waiter")
    arg_parse.add_argument("--timeout", type=int, required=False, default=120, dest="timeout")
    arg_parse.add_argument("--type", type=str, required=True, dest="k8s_type",
                           help="Name of the k8s element type to query (e.g. cool-pod-14)")
    arg_parse.add_argument("--name", type=str, required=True, dest="k8s_name",
                           help="Name of the k8s element name to query (e.g. pod)")
    arg_parse.add_argument("--abstract-state", type=str, required=True, dest="abstract_state",
                           help="Name of the abstract state (e.g. ready, gone)")
    arg_parse.add_argument("--verbose", required=False, dest="verbose", action="store_true",
                           help="Chatty output on stdout.")
    arg_parse.add_argument("--output", type=str, required=False, default="unix_return", dest="output")
    return arg_parse.parse_args()


def deployment_ready(json_status):
    return (json_status['status']['availableReplicas']) > 0

def deployment_torndown(json_status):
    return 'NotFound' in json_status


def build_condition_table():
    build_table = {}
    build_table['deployment.app'] = {
        'deployed': deployment_ready,
        'torndown': deployment_torndown
    }
    return build_table


def main():
    parsed_args = parse_args()

    condition_table = build_condition_table()

    if parsed_args.k8s_type in condition_table and parsed_args.abstract_state in condition_table[parsed_args.k8s_type]:
        print(f"Waiting for {parsed_args.abstract_state} state of k8s object {parsed_args.k8s_type} named {parsed_args.k8s_name}")
        if wait_until(parsed_args.k8s_type, parsed_args.k8s_name,
                      condition_table[parsed_args.k8s_type][parsed_args.abstract_state],
                      parsed_args.timeout, parsed_args.verbose):
            print(
                f"Found {parsed_args.abstract_state} state of k8s object {parsed_args.k8s_type} named {parsed_args.k8s_name}")
            return  # Exit normally
        else:
            print(f"ERROR: Time out {parsed_args.abstract_state} of k8s object {parsed_args.k8s_type} named {parsed_args.k8s_name}")
            sys.exit(1)
    else:
        print(f"ERROR: No condition test for {parsed_args.abstract_state} of k8s object {parsed_args.type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
