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
'''
This module generates a list of all builtin functions and methods
(most at least) for use in parsing python programs for naive static
analysis.
'''
import builtins
import types


def isSomeCrazyException(type_name: str) -> bool:
    obj = getattr(builtins, type_name, None)
    return isinstance(obj, type) and issubclass(obj, BaseException)

def isCallable(type_name: str, parent: any) -> bool:
    return callable(getattr(parent, type_name, None))

builtinfunclist: set = set()

for b in dir(builtins):
    if isCallable(b, builtins) and not isSomeCrazyException(b):
        builtinfunclist.add(b)
    properties: list[str] = dir(getattr(builtins, b))
    for p in properties: 
        if isCallable(p, getattr(builtins, b)) and not isSomeCrazyException(p):
            builtinfunclist.add(p) 
