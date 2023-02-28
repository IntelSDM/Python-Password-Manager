
from enum import Enum
import re
import json
import os

class Format(Enum):
    Date = 0,
    Time = 1,
    
class Validation:
    '''
    This is a static class and can be referenced like a namespace requiring no instance
    '''
    @staticmethod
    def RangeCheck(minvalue, maxvalue, value):
        if(value >= minvalue and value <= maxvalue):
            return True
        return False
    @staticmethod
    def PresenceCheck(value):
        print(id(value))
        if(id(value) != None and value != None): #id converts value to a pointer and checks if the address isn't null, also checks if value isn't null
            return True
        return False
    @staticmethod
    def LengthCheckStr(value, maxvalue, allowunder):
        '''Prototype function of lengthcheck to allow for it to process strings'''
        allowunder = bool(allowunder)  # cant trust python, lets make sure we get a bool
        if(allowunder):
            if(len(value) <= maxvalue):
                return True
        else:
            if(len(value) == maxvalue):
                return True
        return False
    @staticmethod
    def TypeCheck(data, datatype):
        if(isinstance(data,datatype)): # isinstance returns a bool if the data type matches the data
            return True
        return False
    @staticmethod
    def LengthCheck(value, maxvalue, allowunder):
        if(Validation.TypeCheck(value,str)):
            return Validation.LengthCheckStr(value,maxvalue,allowunder)
        allowunder = bool(allowunder)  # cant trust python, lets make sure we get a bool
        if(allowunder):
            if(value <= maxvalue):
                return True
        else:
            if(value == maxvalue):
                return True
        return False
    
    @staticmethod
    def FormatCheck(data,form):
        if(not Validation.TypeCheck(form,Enum)):
            # we are raising an exception to prevent further execution, This works the same as any error and prevents the application executing unless it is caught. this prevents bad code running and informs the programmer on their misuse
            raise ValueError('Format Enum Not Entrered In FormatCheck')
            return False
        # our string formatchecks
        if(Validation.TypeCheck(data,str)):
            if(form == Format.Date): # Date Check
                pattern = r"^\d{2}/\d{2}/\d{4}$"
                if(re.match(pattern,data)):
                    return True
            if(form == Format.Time): #Time Check
                pattern = r"^\d{2}:\d{2}$"
                if(re.match(pattern,data)):
                    return True
        return False
class Database:
    """
This class is meant to create the database and write and read from/to the database

    """
    def __init__(self, filename: str):
        """
        Initialize the database and create an empty file to store tables.
        """
        self.Filename = filename
        self.Tables = {}
        self.Indices = {}
        self.CreateDatabase()

    def CreateDatabase(self):
        """
        Create a new database file and initialize it with an empty json object.
        """
        if(not os.path.exists(self.Filename)):
            f = open(self.Filename, 'w')
            json.dump({}, f)
            
    def CreateTable(self, name: str, fields: list):
        """
        Create a table with the given name and fields.
        """
        if (name in self.Tables):
            print(f"The table {name} already exists.")
            return
        self.Tables[name] = {'fields': fields, 'rows': []}
        self.Indices[name] = {}
    
    def Insert(self, tablename: str, values: list):
        """
        Insert a row into the table with the given values.
        """
        table = self.Tables[tablename]
        if len(values) != len(table['fields']):
            raise ValueError('Number of values does not match number of fields')
        row = dict(zip(table['fields'], values))
        table['rows'].append(row)
        # Update the indices
        for i, field in enumerate(table['fields']):
            if field not in self.Indices[tablename]:
                self.Indices[tablename][field] = {}
            if values[i] not in self.Indices[tablename][field]:
                self.Indices[tablename][field][values[i]] = []
            self.Indices[tablename][field][values[i]].append(row)

    def DeleteField(self, tableName: str, field: str):
        """Delete the field with the given name from the table with the given name."""
        table = self.Tables[tableName]
        # Remove the field from the fields list
        table['fields'].remove(field)
        # Remove the field from the indices
        del self.Indices[tableName][field]
        # Update the rows in the table
        for row in table['rows']:
            del row[field]
    
    def DeleteTable(self, tableName: str):
        """Delete the table with the given name."""
        del self.Tables[tableName]
        del self.Indices[tableName]

    def DeleteRow(self, tableName: str, row: dict):
        """Delete the row from the table with the given name."""
        table = self.Tables[tableName]
        # Remove the row from the rows list
        table['rows'].remove(row)
        # Update the indices
        for field, value in row.items():
            self.Indices[tableName][field][value].remove(row)

    def UpdateField(self, tableName: str, field: str, newValue: str, row: dict):
        """
        Update the value of the field in the given row in the table with the given name.
        """
        table = self.Tables[tableName]
        # Update the value in the row
        row[field] = newValue
        # Update the index
        oldValue = row[field]
        self.Indices[tableName][field][oldValue].remove(row)
        if newValue not in self.Indices[tableName][field]:
            self.Indices[tableName][field][newValue] = []
        self.Indices[tableName][field][newValue].append(row)

    def UpdateRow(self, tableName: str, row: dict, newValues: dict):
        """
        Update the values in the given row in the table with the given name.
        """
        table = self.Tables[tableName]
        # Update the values in the row
        for field, newValue in newValues.items():
            # Update the index
            oldValue = row[field]
            self.Indices[tableName][field][oldValue].remove(row)
            if newValue not in self.Indices[tableName][field]:
                self.Indices[tableName][field][newValue] = []
            self.Indices[tableName][field][newValue].append(row)
            row[field] = newValue

    def Search(self, table: dict, searchTerms: dict) -> list:
        """
        Search for rows in the given table that match the given search terms.
        """
        results = []
        for row in table['rows']:
            match = True
            for field, value in searchTerms.items():
                if row[field] != value:
                    match = False
                    break
            if match:
                results.append(row)
        if not results:
            return None
        return results

    def Save(self):
        """
        Save the database to the file.
        """
        with open(self.Filename, 'w') as f:
            json.dump({'tables': self.Tables, 'indices': self.Indices}, f)


