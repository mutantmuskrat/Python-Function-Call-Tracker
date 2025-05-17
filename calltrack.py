'''
    This is part of the Python-Function-Call-Tracker program.
    This program can track all the function call relations in your
    Python programs.
    Copyright (C) 2025  Noah Meng

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
    Contact the Developer by Email:
        muskratmutated@gmail.com
'''
import sys
import os
from dataclasses import dataclass
from listfunc import *
from FuncNodeType import FuncNodeType
import csv
import curses
import ast

def build_tree(path: str, entry_function: str, func_list: list[FuncNodeType] = list(), parent:list = []):
    print("Searching "+entry_function +"()...")
    for func in func_list:
        if func.name == entry_function and func.file == path:
            print("Function already discovered")
            func.called_by.append(parent)
            return func_list

    func_txt = openfunction(entry_function, path)
    if func_txt is None:
        return func_list
    called_list = findcalledfunc(func_txt)
    # Check to see if any functions are being used under a local alias.
    renames = list()
    with open(path, "r") as f:
        renames = findfuncrenames(f.read())
    
    rename_calls = list()
    for call in called_list:
        for r in renames:
            if call == r[2]:
                called_list.remove(call)
                rename_calls.append(r)
        if call == entry_function:
            called_list.remove(call)
    # Find function name and source file for every called function.
    called_funcs = list()
    for call in called_list:
        func_call_info = findfuncdef(call, os.path.dirname(path))
        if None not in func_call_info:
            called_funcs.append(func_call_info)
    for rename in rename_calls:
        try:
            f = open(findimportfile(rename[0], os.path.dirname(path)))
            called_funcs.append([rename[1], os.path.join(os.path.dirname(path), rename[0]+ ".py")])
        except:
            pass

    func_list.append(FuncNodeType(entry_function, path, [parent], called_funcs))
    
    for func in called_funcs:
        func_list = build_tree(func[1], func[0], func_list, [entry_function, path])

    return func_list

def make_csv(path: str, entry_function: str):
    func_nodes = build_tree(path, entry_function)
    with open(f"output_{os.path.basename(path)}_{entry_function}.csv", "w") as csv_file:
        # Create CSV Header
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name','File','Called_By','Calls','Description'])
        for node in func_nodes:
            csv_writer.writerow([node.name, node.file, node.called_by, node.calls])

def save_descriptions(filename: str, descriptions: list):
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        final_out = list()
        i = 0
        for row in list(csv_reader):
            row = list(row)
            if len(row) < 5 and i < len(descriptions):
                row.append(descriptions[i])
                final_out.append(row)
                i += 1
            else:
                final_out.append(row)
    with open(filename, "w") as f:
        csv_writer = csv.writer(f)
        for row in final_out:
            csv_writer.writerow(row)

def main():
    if len(sys.argv) < 3:
        print("Usage:\npython", sys.argv[0], "[path to code directory]", "[entry function]")
    elif len(sys.argv) == 3:
        if f"output_{os.path.basename(sys.argv[1])}_{sys.argv[2]}.csv" in os.listdir():
            answer = input("Remap Code Structure?")
            if str(answer).lower() == "y":    
                make_csv(sys.argv[1], sys.argv[2])
        else:
            make_csv(sys.argv[1], sys.argv[2])
    stdscr = curses.initscr()
    screen = curses.newpad(2000, 2000)
    curses.echo()
    Exit : bool = False
    screen.clear()
    while not Exit:
        stdscr.addstr(0,0, "Documentation Engine")
        stdscr.addstr(2,0, "Main Menu")
        stdscr.addstr(3,0, "1. Enter Function Descriptions")
        stdscr.addstr(4,0, "2. Function Lookup")
        stdscr.addstr(10,0, "Enter Selection:___")
        stdscr.move(10,17)
        stdscr.refresh()

        option = stdscr.getkey()
        if (option == "1" or option == "2"):
            Exit = True
    Exit = False
    try:
        if option == "1":
            descriptions: list = list()
            with open(f"output_{os.path.basename(sys.argv[1])}_{sys.argv[2]}.csv", "r") as f:
                csv_read = csv.reader(f)
                for row in csv_read:
                    if len(row) < 5:
                        screen.clear()
                        screen.addstr(0,0, "Documentation Engine")
                        screen.addstr(2,0, " ____________________________________________________")
                        screen.addstr(3,0, "| Directions:                                        |")
                        screen.addstr(4,0, "| Type a description of the function, then [ENTER].  |")
                        screen.addstr(5,0, "| To QUIT, type ':q[ENTER]'                          |")
                        screen.addstr(6,0, "| To SAVE, type ':w[ENTER]'                          |")
                        screen.addstr(7,0, "| To SAVE and QUIT, type ':wq[ENTER]'                |")
                        screen.addstr(8,0, " ----------------------------------------------------")
                        screen.addstr(10,0, f"{row[0]}")
                        screen.addstr(11,0, f"\tlocation: {row[1]}")
                        screen.addstr(12,0, "\tcalled_by:")
                        screen.addstr(13,0, "\t\tNone")
                        scrpos: int = 13
                        for item in ast.literal_eval(row[2]):
                            if len(item) == 2:
                                screen.addstr(scrpos, 0, f"\t\t{item[0]} in {item[1]}")
                            scrpos += 1
                        screen.addstr(scrpos, 0, "\tcalls:")
                        scrpos += 1
                        screen.addstr(scrpos, 0, "\t\tNone")
                        for item in ast.literal_eval(row[3]):
                            if len(item) == 2:
                                screen.addstr(scrpos, 0, f"\t\t{item[0]} in {item[1]}")
                            scrpos += 1
                        scrpos += 1
                        screen.addstr(scrpos, 0, "\tdescription:")
                        win_y, win_x = stdscr.getmaxyx()
                        screen.refresh(0,0,0,0,win_y - 1, win_x - 1)
                        scrpos += 1
                        input_box = curses.newwin(50, win_x - 17, scrpos, 16)
                        input_box.refresh()
                        descriptions.append(input_box.getstr().decode("utf-8"))
                        #descriptions.append(stdscr.getstr(scrpos + 1, 16).decode(stdscr.encoding))
                        if ":w" == descriptions[-1]:
                            save_descriptions(f"output_{os.path.basename(sys.argv[1])}_{sys.argv[2]}.csv", descriptions[:-1])
                        elif ":q" == descriptions[-1]:
                            break
                        elif ":wq" == descriptions[-1]:
                            break
                        win_y, win_x = stdscr.getmaxyx()
                        screen.refresh(0,0,0,0,win_y - 1, win_x - 1)
                if descriptions[-1] != ":q":
                    save_descriptions(f"output_{os.path.basename(sys.argv[1])}_{sys.argv[2]}.csv", descriptions[:-1])


        elif option == "2":
            screen.clear()
            screen.addstr(0,0, "Documentation Engine")
            screen.addstr(2,0, "Function Lookup")
            scrpos: int = 5
            while not Exit:
                screen.addstr(scrpos,0, "Enter Function Name: ")
                win_y, win_x = stdscr.getmaxyx()
                screen.refresh(0,0,0,0,win_y - 1, win_x - 1)
                
                input_box = curses.newwin(1, win_x - 17, scrpos, 21)
                input_box.refresh()
                func_name = input_box.getstr().decode("utf-8")
 
                if func_name != ":q":
                    with open(f"output_{os.path.basename(sys.argv[1])}_{sys.argv[2]}.csv", "r") as f:
                        csv_reader = csv.reader(f)
                        for line in csv_reader:
                            if line[0] == func_name:
                                screen.clear()
                                screen.addstr(0,0, "Documentation Engine")
                                screen.addstr(2,0, "Function Lookup")
                                screen.addstr(4,0, "To QUIT, type ':q[ENTER]")
                                screen.addstr(6, 0, line[0])
                                screen.addstr(7, 0, f"\tlocation: {line[1]}")
                                screen.addstr(8, 0, "\tcalled_by:")
                                scrpos = 9
                                for item in ast.literal_eval(line[2]):
                                    if len(item) == 2:
                                        screen.addstr(scrpos, 0, f"\t\t{item[0]} in {item[1]}")
                                    scrpos += 1
                                screen.addstr(scrpos,0, "\tcalls:")
                                scrpos += 1
                                for item in ast.literal_eval(line[3]):
                                    if len(item) == 2:
                                        screen.addstr(scrpos, 0, f"\t\t{item[0]} in {item[1]}")
                                    scrpos += 1
                                screen.addstr(scrpos,0, "\tdescription:")
                                scrpos += 1
    
                                if len(line) == 5:
                                    screen.addstr(scrpos,0, f"\t\t{line[4]}")
                                else:
                                    screen.addstr(scrpos,0,"\t\tNone")
                                scrpos += 2
                                break
                
                else:
                    Exit = True

        curses.echo()
        curses.endwin()
    except Exception as e:
        curses.echo()
        curses.endwin()
        
if __name__ == "__main__":
    main()
