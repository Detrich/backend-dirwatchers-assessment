Dirwatcher

This program is a Directory watcher that will continually watch a Specific directory given. It looks for text files within the directory with a specific given extension(.log,.txt...). Inside of the file with the specific extension it will also search for a specific string given as a "magic text" and log when the magic text is found and what line it appears on. 

The first argument in the program will be the polling interval of the program(integer).The second argument will be the extension of the files to search for in the directory(.log,.txt...). The third argument will be the text to search for in the file. The fourth and final argument will be the directory to search in.

USAGE: python dirwatcher.py [-i INTERVAL] [-e EXT] magic path

Examples of the program being ran:
    ```
    python dirwatcher.py -i 1 -e .log hello watchme
    python dirwatcher.py -i 2 -e .log magic-text directory  
    ```