# lsgaiatest
List what tests gaiatest would run for a given set of options.

Install with:

    python setup.py install

```
$ lsgaiatest --help
usage: lsgaiatest [-h] [--type TYPE] [--tag TAG] [--run-list]
                  [--no-unfound-tests] [--no-run-tests] [--no-skipped-tests]
                  [--no-skip-reason] [--full-path] [--device DEVICE]
                  [--app_name APP_NAME]
                  test_file_or_dir [test_file_or_dir ...]

List what tests gaiatest would run for a given set of options.

positional arguments:
  test_file_or_dir     A test script, directory, or manifest

optional arguments:
  -h, --help           show this help message and exit

Query:
  --type TYPE          The type of test to run, can be a combination of values
                       defined in the manifest file; individual values are
                       combined with "+" or "-" characters. For example:
                       "browser+b2g" means the set of tests which are
                       compatible with both browser and b2g; "b2g-qemu" means
                       the set of tests which are compatible with b2g but do
                       not require an emulator. This argument is only used
                       when loading tests from manifest files
  --tag TAG            Filter out tests which don't have the given tag. Can be
                       used multiple times, in which case the test must
                       contain at least one of the given tags.

Reports:
  --run-list           Omit any headers or extra output and only output a json
                       list of tests that would be run. This will override any
                       other reporting options except --full-path.
                       (default=False)
  --no-unfound-tests   Suppress the report about unfound tests (default=False)
  --no-run-tests       Suppress the report about tests that would be run
                       (default=False)
  --no-skipped-tests   Suppress the report about tests that would be skipped
                       (default=False)
  --no-skip-reason     Omit the reason for skipping the test (default=False)
  --full-path          Always output the full path of the test (default=False)

Capabilities:
  --device DEVICE      Device the test runner would detect, such as "flame" or
                       "desktop" (default=flame)
  --app_name APP_NAME  Application name the test runner would detect, such as
                       "B2G" or "Firefox"(default=B2G)
```

