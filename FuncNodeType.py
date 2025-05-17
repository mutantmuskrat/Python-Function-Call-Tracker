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
from dataclasses import dataclass

@dataclass
class FuncNodeType:
    '''
    This contains the info for a function that we want to document.
    '''
    name: str
    file: str
    called_by: list
    calls: list
    desc: str
    
    def __init__(self, n: str, f: str, cb = list(), cls = list(), d = ""):
        self.name = n
        self.file = f
        self.called_by = cb
        self.calls = cls
        self.desc = d
