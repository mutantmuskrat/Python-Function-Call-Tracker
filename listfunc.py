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
import re
import os
from builtinfunclist import builtinfunclist

def listfuncnames(file_text: str) -> list[str]:
    function_names : list[str] = list()
    lines: list[str] = file_text.splitlines()

    for line in lines:
        if "def" in line:
            split_line: str = line.split("def") # Checking if this keyword is commented out
            if("#" not in split_line[0]):
                if (line[:3] == "def" or "def " in line):
                    func_name: str = split_line[1].split("(")[0]
                else:
                    continue
                function_names.append(func_name.strip())
    return function_names

def splitfunc(file_text: str) -> list[str]:
    function_text : list[str] = list()
    lines: list[str] = file_text.split("\n")
    indent: int = 0
    infunc: bool = False
    for i, line in enumerate(lines):
        if line[:3] == "def" or "def " in line and indent > getindentlevel(line):
            function_text.append(line)
            indent = getindentlevel(lines[i+1])
            infunc = True
        elif getindentlevel(line) < indent and line.strip() != "":
            infunc = False
        elif len(function_text) and getindentlevel(line) >= indent and infunc:
            function_text[-1] += str("\n" + line)
            
    return function_text

def openfunction(name: str, file: str) -> str:
    with open(file, "r") as f:
        for function in splitfunc(f.read()):
            if name == getfuncnamefromdef(getfirstline(function)).strip():
                return function
    return None

def getindentlevel(line: str) -> int:
    level: int = 0
    for char in line:
        if char == " ":
            level += 1
        if char == "\t":
            level += 4
        else:
            break
    return level

def getfirstline(textin: str) -> str:
    return textin.splitlines()[0]

def getfuncnamefromdef(line: str):
    split_line: str = line.split("def") # Checking if this keyword is commented out
    if (line[:3] == "def" or "def " in line):
        func_name: str = split_line[1].split("(")[0]
    return func_name.strip()

def findcalledfunc(function_text: str) -> list[str]:
    # remove the first line of the function so that the function does not detect its own 
    # function definition.
    index: int = function_text.index("\n")
    function_text = function_text[index:]
    # The regular expression below finds the word behind any opening and closing parenthesis.
    function_calls: list[str] = re.findall(r"(\w+?)\s*\((?:[^\)]*?)\)", function_text)
    # Now, we filter to remove any references to builtin functions.
    func_set: list = list()
    for func_call in function_calls:
        if func_call not in builtinfunclist and func_call not in func_set:
            func_set.append(func_call)
    return func_set

# Find the function definition of a function.
def findfuncdef(func_name: str, code_dir: str) ->list[str]:
    result : list = [None, None]
    for sub_dir in os.listdir(code_dir):
        if os.path.isdir(os.path.join(code_dir, sub_dir)):
            result = findfuncdef(func_name, os.path.join(code_dir, sub_dir))
            if None not in result:
                break
        elif re.search(r"(?:.*)\.py\b", sub_dir):
            f = open(os.path.join(code_dir, sub_dir))
            if func_name in listfuncnames(f.read()):
                f.close()
                result = [func_name, os.path.join(code_dir, sub_dir)]
                break
    return result

# Finds all calls to a given function.
def findfunccalls(func: str, code_dir: str, finds: list = list()):
    for filename in os.listdir(code_dir):
        if os.path.isdir(os.path.join(code_dir, filename)):
            finds = findfunccalls(func, os.path.join(code_dir, filename), finds)
        elif re.search(r"(?:.*)\.py\b", filename):
            f = open(os.path.join(code_dir,filename))
            for function in splitfunc(f.read()):
                if func in findcalledfunc(function):
                    finds.append([getfuncnamefromdef(getfirstline(function)), os.path.join(code_dir, filename)])
            f.close()
    return finds


def findfuncrenames(text: str) -> list[str]:
    return re.findall(r"(?:from\s)(.*:?)(?:\simport\s)(.*:?)(?:\sas\s)(.*:?)", text)

def findimportfile(import_name: str, code_dir: str) -> str:
    path_to_file = code_dir
    path = import_name.split(".")
    for name in path:
        path_to_file = os.path.join(path_to_file, name)
    return path_to_file + ".py"
