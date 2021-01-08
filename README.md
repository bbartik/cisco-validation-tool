# cisco-validation-tool

This tool was meant to help validate some Cisco ISE specific configurations. It uses a file called "golden.ini" where you can put global or interface "golden" parameters. The script than uses ciscoconfparse to search for the golden lines and report whether they are found or not.

## Usage

Enter device hostname or IPs in devices.txt

Get the configs and store in ./configs:
```
$ python config-getter.py
```

Validate the configuration:
```
$ python config-validator.py
```

## Outputs

Output is written to a file named "validation.csv" where you can sort and filter using Excel or some other editor. 

<img src="images/image1.jpg"></img>

Config snippets for updating devices are written to ./updates/[devicename].conf

## Filter interfaces

In the script you can filter the interface. Below we are only getting the 12th-13th interfaces which happen to be g1/0/12-13.

```
    # FILTER INTERFACE LIST
    #interface_list = [i.text for i in interfaces]
    interface_list = [i.text for i in interfaces][12:14]
```

