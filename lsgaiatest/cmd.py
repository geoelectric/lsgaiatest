#!/usr/bin/env python

"""List what tests gaiatest would run for a given set of options."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import os

from marionette import BaseMarionetteTestRunner


def format_path(path, args):
    path = os.path.abspath(path)
    return path if args.full_path else path.replace(os.getcwd(), '.')


def print_header(header):
    print '%s:' % header


def print_report(runner, unfound_tests, args):
    if args.run_list:
        print json.dumps(runner.tests, indent=0)
        return

    if args.no_unfound_tests and args.no_run_tests and args.no_skipped_tests:
        print 'All reports suppressed. Nothing to do.'
        return

    if unfound_tests and not args.no_unfound_tests:
        print_header('Would cause an "unfound" error (%d)' % len(unfound_tests))
        for unfound_test in unfound_tests:
            print '  ', format_path(unfound_test['filepath'], args)
        print

    if runner.tests and not args.no_run_tests:
        print_header('Would be run  (%d)' % len(runner.tests))
        for run_test in runner.tests:
            suffix = 'fail' if run_test['expected'] == 'fail' else ''
            print '  ', format_path(run_test['filepath'], args), suffix
        print

    if runner.manifest_skipped_tests and not args.no_skipped_tests:
        print_header('Would be skipped (%d)' % len(runner.manifest_skipped_tests))
        for skip_test in runner.manifest_skipped_tests:
            if args.no_skip_reason:
                reason = ''
            else:
                reason = ': %s' % skip_test['disabled']
            print '  ', format_path(skip_test['path'], args), reason
        print


def add_tests_to_runner(args):
    runner = BaseMarionetteTestRunner(type=args.type, test_tags=args.tags)

    runner._appName = args.app_name
    runner._device = args.device

    for test in args.tests:
        runner.add_test(test)

    unfound_tests = []
    runner_tests = runner.tests[:]
    for run_test in runner_tests:
        if not os.path.exists(run_test['filepath']):
            runner.tests.remove(run_test)
            unfound_tests.append(run_test)

    return runner, unfound_tests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tests',
                        help='A test script, directory, or manifest',
                        metavar='test_file_or_dir',
                        nargs='+')

    arggrp = parser.add_argument_group('Query')
    arggrp.add_argument('--type',
                        help=('The type of test to run, can be a combination of values defined in the manifest file; '
                              'individual values are combined with "+" or "-" characters. For example: "browser+b2g" '
                              'means the set of tests which are compatible with both browser and b2g; "b2g-qemu" means '
                              'the set of tests which are compatible with b2g but do not require an emulator. This '
                              'argument is only used when loading tests from manifest files'))
    arggrp.add_argument('--tag',
                        action='append',
                        dest='tags',
                        help=("Filter out tests which don't have the given tag. Can be used multiple times, in which "
                              'case the test must contain at least one of the given tags.'),
                        metavar='TAG')

    arggrp = parser.add_argument_group('Reports')
    arggrp.add_argument('--run-list',
                        action='store_true',
                        default=False,
                        help=('Omit any headers or extra output and only output a json list of tests that would be '
                              'run. This will override any other reporting options except --full-path. '
                              '(default=%(default)s)'))
    arggrp.add_argument('--no-unfound-tests',
                        action='store_true',
                        default=False,
                        help='Suppress the report about unfound tests (default=%(default)s)')
    arggrp.add_argument('--no-run-tests',
                        action='store_true',
                        default=False,
                        help='Suppress the report about tests that would be run (default=%(default)s)')
    arggrp.add_argument('--no-skipped-tests',
                        action='store_true',
                        default=False,
                        help='Suppress the report about tests that would be skipped (default=%(default)s)')
    arggrp.add_argument('--no-skip-reason',
                        action='store_true',
                        default=False,
                        help='Omit the reason for skipping the test (default=%(default)s)')
    arggrp.add_argument('--full-path',
                        action='store_true',
                        default=False,
                        help='Always output the full path of the test (default=%(default)s)')

    arggrp = parser.add_argument_group('Capabilities')
    arggrp.add_argument('--device',
                        default='flame',
                        help='Device the test runner would detect, such as "flame" or "desktop" (default=%(default)s)')
    arggrp.add_argument('--app_name',
                        default='B2G',
                        help=('Application name the test runner would detect, such as "B2G" or "Firefox"'
                              '(default=%(default)s)'))

    args = parser.parse_args()

    runner, unfound_tests = add_tests_to_runner(args)
    print_report(runner, unfound_tests, args)


if __name__ == '__main__':
    main()
