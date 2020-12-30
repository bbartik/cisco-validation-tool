# cisco-validation-tool

This tool was meant to help validate some Cisco ISE specific configurations. It uses a file called "golden.ini" where you can put global or interface "golden" parameters. The script than uses CiscoConfParse to search for the golden lines and report whether they are found or not.

## Usage

```
$ python config-validator.py
```

## Output

Output is written to a CSV file where you can sort and filter using Excel or some other editor.

## Future

- Add netmiko support (Currently just searcges local dir for conf files)
- Add option to create a Cisco config script to add in the "not founds"

