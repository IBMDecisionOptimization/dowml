""""Send a CPLEX file to WML and solve it.

For now, just accepts a path and sends that, assuming that's a model
The code is mostly based on
https://dataplatform.cloud.ibm.com/exchange/public/entry/view/50fa9246181026cd7ae2a5bc7e4ac7bd"""
import argparse
import logging
import pprint

import ibm_watson_machine_learning

from dowmlclient import DOWMLClient


def main():
    parser = argparse.ArgumentParser(description='Send a CPLEX model for solving on WML')
    parser.add_argument(metavar='model', dest='model',
                        help='Name of the model to solve')
    parser.add_argument('--wml-cred-file',
                        help='Name of the file from which to read WML credentials. '
                             'If not specified, credentials are read from an environment variable')
    args = parser.parse_args()

    logging.basicConfig(force=True, format='%(asctime)s %(message)s', level=logging.INFO)

    client = DOWMLClient(args.wml_cred_file)
    client.solve(args.model)


def test():
    logging.basicConfig(force=True, format='%(asctime)s %(message)s', level=logging.INFO)
    c = DOWMLClient('xavier-wml-cred.txt')
    client = c._get_or_make_client()
    result = client.software_specifications._href_definitions.get_sw_specs_href()
    pprint.pprint(result)


if __name__ == '__main__':
    test()
