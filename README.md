# tftpsrv

This repo contains the reversed code for the `tftpsrv` executable from the D-Link DPH-128MS VOIP phones.

## function_graph.py

This is a helper script to create graph images of function calls from the `tftpsrv` disassembly files.

## udp_9999.py

This script will scan a network for D-Link phones running a vulnerable version of the firmware.

## tftpsrv_reverse_shell.py

This script will attempt to connect to a vulnerable D-Link phone and open a reverse shell.
