# Zephyr tracecompass scripts

## Installing TraceCompass with scripting modules

Go in Eclipse downloads and find the latest TraceCompass tar.gz with all the incubator features included, for instance [here](https://www.eclipse.org/downloads/download.php?file=/tracecompass.incubator/master/rcp/trace-compass-0.9.0-20240508-0458-linux.gtk.x86_64.tar.gz&mirror_id=1285).

You can also download TraceCompass and try adding the modules:
* Scripting
* Scripting Python

### Python scripts

By default, executing Python scripts fails with: "Could not setup Python engine".

Go to:

    Preferences -> Python Scripting (using Py4J)

And change the Python location from "python" to your Python path, for instance "/usr/bin/python3".

## Importing the module

    File -> Open Trace -> zephyr_thread_states.py

Then open the trace, and run the script with:

    Run As... -> Ease Script

For this script, Py4J fails with "An error occurred while calling o15.getQuarkAbsoluteAndAdd", but succeeds with Jython.

    Run As... -> Run Configuration -> Jython
