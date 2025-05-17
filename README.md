# Python-Function-Call-Tracker
This is a simple tool (still far from perfect) that can find and map function calls in a project.

## How to use
First, clone the project using
```
git clone https://github.com/mutantmuskrat/Python-Function-Call-Tracker.git
```

The entrypoint is ```calltrack.py```. To run it, use the following syntax:
```
python calltrack.py [absolute path to entrypoint file] [name of entry-point function]
```
### Example
```
python calltrack.py /home/user/calltrack.py main
```
> [!IMPORTANT]
> The path to your code MUST be absolute

This will navigate through the parent directory of the entrypoint file searching for any called functions. For each function found, it will find each function it calls. If the same function is called twice, the system adds the calling function to the "called by" list for that function. At the end, a csv file is generated. You will be prompted to either enter a description of each function in the codebase, or lookup details about a given function.
```
Documentation Engine

Main Menu
1. Enter Function Descriptions
2. Function Lookup





Enter Selection:___
```

If you select "1", you will see a screen like that shown below. You can enter a description of the function by typing. Then type enter to move to be presented with another function. To save your description notes to the csv file, type ```:w``` and press [ENTER]. 
```
Documentation Engine

 ____________________________________________________
| Directions:                                        |
| Type a description of the function, then [ENTER].  |
| To QUIT, type ':q[ENTER]'                          |
| To SAVE, type ':w[ENTER]'                          |
| To SAVE and QUIT, type ':wq[ENTER]'                |
 ----------------------------------------------------

main
        location: /home/user/Documents/calltracker/calltrack.py
        called_by:
                None
        calls:
                make_csv in /home/user/Documents/calltracker/calltrack.py
                save_descriptions in /home/user/Documents/calltracker/calltrack.p

        description:
              User-entered description ... 
```
If you select "2", you can lookup details about a function as shown below. Enter a function's name to see details.
```
Documentation Engine

Function Lookup


Enter Function Name: main
```
Now, you can see details about the function, as shown below.
```
Documentation Engine

Function Lookup

To QUIT, type ':q[ENTER]

main
        location: /home/elf/Documents/calltracker/calltrack.py
        called_by:

        calls:
                make_csv in /home/elf/Documents/calltracker/calltrack.py
                save_descriptions in /home/elf/Documents/calltracker/calltrack.p
        description:
                The entry-point to the program.

Enter Function Name: 
```
To see details about another function, enter its name and press [ENTER]. To quit, type ```:q```.
