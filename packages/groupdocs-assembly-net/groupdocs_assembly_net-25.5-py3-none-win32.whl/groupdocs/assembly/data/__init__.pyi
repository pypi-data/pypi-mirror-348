from typing import List, Optional, Dict, Iterable, Any, overload
import io
import collections.abc
from collections.abc import Sequence
from datetime import datetime
from aspose.pyreflection import Type
import aspose.pycore
import aspose.pydrawing
from uuid import UUID
import groupdocs.assembly
import groupdocs.assembly.data

class CsvDataLoadOptions:
    '''Represents options for parsing CSV data.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of this class with default options.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, has_headers : bool) -> None:
        '''Initializes a new instance of this class with specifying whether CSV data contains column names
        at the first line.'''
        raise NotImplementedError()
    
    @property
    def has_headers(self) -> bool:
        '''Gets a value indicating whether the first line of CSV data contains column names.'''
        raise NotImplementedError()
    
    @has_headers.setter
    def has_headers(self, value : bool) -> None:
        '''Sets a value indicating whether the first line of CSV data contains column names.'''
        raise NotImplementedError()
    
    @property
    def delimiter(self) -> str:
        '''Gets the character to be used as a column delimiter.'''
        raise NotImplementedError()
    
    @delimiter.setter
    def delimiter(self, value : str) -> None:
        '''Sets the character to be used as a column delimiter.'''
        raise NotImplementedError()
    
    @property
    def quote_char(self) -> str:
        '''Gets the character that is used to quote field values.'''
        raise NotImplementedError()
    
    @quote_char.setter
    def quote_char(self, value : str) -> None:
        '''Sets the character that is used to quote field values.'''
        raise NotImplementedError()
    
    @property
    def comment_char(self) -> str:
        '''Gets the character that is used to comment lines of CSV data.'''
        raise NotImplementedError()
    
    @comment_char.setter
    def comment_char(self, value : str) -> None:
        '''Sets the character that is used to comment lines of CSV data.'''
        raise NotImplementedError()
    

class CsvDataSource:
    '''Provides access to data of a CSV file or stream to be used while assembling a document.'''
    
    @overload
    def __init__(self, csv_path : str) -> None:
        '''Creates a new data source with data from a CSV file using default options for parsing CSV data.
        
        :param csv_path: The path to the CSV file to be used as the data source.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, csv_path : str, options : groupdocs.assembly.data.CsvDataLoadOptions) -> None:
        '''Creates a new data source with data from a CSV file using the specified options for parsing CSV data.
        
        :param csv_path: The path to the CSV file to be used as the data source.
        :param options: Options for parsing the CSV data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, csv_stream : io._IOBase) -> None:
        '''Creates a new data source with data from a CSV stream using default options for parsing CSV data.
        
        :param csv_stream: The stream of CSV data to be used as the data source.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, csv_stream : io._IOBase, options : groupdocs.assembly.data.CsvDataLoadOptions) -> None:
        '''Creates a new data source with data from a CSV stream using the specified options for parsing CSV data.
        
        :param csv_stream: The stream of CSV data to be used as the data source.
        :param options: Options for parsing the CSV data.'''
        raise NotImplementedError()
    

class DocumentTable:
    '''Provides access to data of a single table (or spreadsheet) located in an external document to be used while
    assembling a document.'''
    
    @overload
    def __init__(self, document_path : str, index_in_document : int) -> None:
        '''Creates a new instance of this class using default :py:class:`groupdocs.assembly.data.DocumentTableOptions`.
        
        :param document_path: The path to a document containing the table to be accessed.
        :param index_in_document: The zero-based index of the table in the document.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document_path : str, index_in_document : int, options : groupdocs.assembly.data.DocumentTableOptions) -> None:
        '''Creates a new instance of this class.
        
        :param document_path: The path to a document containing the table to be accessed.
        :param index_in_document: The zero-based index of the table in the document.
        :param options: A set of options controlling extraction of data from the table. If null, default options are applied.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document_stream : io._IOBase, index_in_document : int) -> None:
        '''Creates a new instance of this class using default :py:class:`groupdocs.assembly.data.DocumentTableOptions`.
        
        :param document_stream: The stream containing a document with the table to be accessed.
        :param index_in_document: The zero-based index of the table in the document.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document_stream : io._IOBase, index_in_document : int, options : groupdocs.assembly.data.DocumentTableOptions) -> None:
        '''Creates a new instance of this class.
        
        :param document_stream: The stream containing a document with the table to be accessed.
        :param index_in_document: The zero-based index of the table in the document.
        :param options: A set of options controlling extraction of data from the table. If null, default options are applied.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the name of this table used to access the table\'s data in a template document passed to
        :py:class:`groupdocs.assembly.DocumentAssembler`.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name of this table used to access the table\'s data in a template document passed to
        :py:class:`groupdocs.assembly.DocumentAssembler`.'''
        raise NotImplementedError()
    
    @property
    def index_in_document(self) -> int:
        '''Gets the original zero-based index of the corresponding table as per the source document.'''
        raise NotImplementedError()
    
    @property
    def columns(self) -> groupdocs.assembly.data.DocumentTableColumnCollection:
        '''Gets the collection of :py:class:`groupdocs.assembly.data.DocumentTableColumn` objects representing columns of
        the corresponding table.'''
        raise NotImplementedError()
    

class DocumentTableCollection:
    '''Represents a read-only collection of :py:class:`groupdocs.assembly.data.DocumentTable` objects of a particular :py:class:`groupdocs.assembly.data.DocumentTableSet`
    instance.'''
    
    @overload
    def contains(self, name : str) -> bool:
        '''Returns a value indicating whether this collection contains a table with the specified name.
        
        :param name: The case-insensitive name of a table to look for.
        :returns: A value indicating whether this collection contains a table with the specified name.'''
        raise NotImplementedError()
    
    @overload
    def contains(self, table : groupdocs.assembly.data.DocumentTable) -> bool:
        '''Returns a value indicating whether this collection contains the specified table.
        
        :param table: A table to look for.
        :returns: A value indicating whether this collection contains the specified table.'''
        raise NotImplementedError()
    
    @overload
    def index_of(self, name : str) -> int:
        '''Returns the index of a table with the specified name within this collection.
        
        :param name: The case-insensitive name of a table to find.
        :returns: The zero-based index of a table with the specified name, or -1 if the table does not exist in this collection.'''
        raise NotImplementedError()
    
    @overload
    def index_of(self, table : groupdocs.assembly.data.DocumentTable) -> int:
        '''Returns the index of the specified table within this collection.
        
        :param table: A table to find.
        :returns: The zero-based index of the specified table, or -1 if the table does not exist in this collection.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the total number of :py:class:`groupdocs.assembly.data.DocumentTable` objects in the collection.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.assembly.data.DocumentTable:
        '''Gets a :py:class:`groupdocs.assembly.data.DocumentTable` instance from the collection at the specified index.'''
        raise NotImplementedError()
    

class DocumentTableColumn:
    '''Represents a single column of a particular :py:class:`groupdocs.assembly.data.DocumentTable` object.'''
    
    @property
    def name(self) -> str:
        '''Gets the name of this column used to access the column\'s data in a template document passed to
        :py:class:`groupdocs.assembly.DocumentAssembler`.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name of this column used to access the column\'s data in a template document passed to
        :py:class:`groupdocs.assembly.DocumentAssembler`.'''
        raise NotImplementedError()
    
    @property
    def index_in_document(self) -> int:
        '''Gets the original zero-based index of the corresponding table column as per the source document.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> Type:
        '''Gets the type of cell values in this column.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : Type) -> None:
        '''Sets the type of cell values in this column.'''
        raise NotImplementedError()
    
    @property
    def allows_null(self) -> bool:
        '''Gets a value indicating whether cells in this column contain null values or not.'''
        raise NotImplementedError()
    

class DocumentTableColumnCollection:
    '''Represents a read-only collection of :py:class:`groupdocs.assembly.data.DocumentTableColumn` objects of a particular
    :py:class:`groupdocs.assembly.data.DocumentTable` instance.'''
    
    @overload
    def contains(self, name : str) -> bool:
        '''Returns a value indicating whether this collection contains a column with the specified name.
        
        :param name: The case-insensitive name of a column to look for.
        :returns: A value indicating whether this collection contains a column with the specified name.'''
        raise NotImplementedError()
    
    @overload
    def contains(self, column : groupdocs.assembly.data.DocumentTableColumn) -> bool:
        '''Returns a value indicating whether this collection contains the specified column.
        
        :param column: A column to look for.
        :returns: A value indicating whether this collection contains the specified column.'''
        raise NotImplementedError()
    
    @overload
    def index_of(self, name : str) -> int:
        '''Returns the index of a column with the specified name within this collection.
        
        :param name: The case-insensitive name of a column to find.
        :returns: The zero-based index of a column with the specified name, or -1 if the column does not exist in this collection.'''
        raise NotImplementedError()
    
    @overload
    def index_of(self, column : groupdocs.assembly.data.DocumentTableColumn) -> int:
        '''Returns the index of the specified column within this collection.
        
        :param column: A column to find.
        :returns: The zero-based index of the specified column, or -1 if the column does not exist in this collection.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the total number of :py:class:`groupdocs.assembly.data.DocumentTableColumn` objects in the collection.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.assembly.data.DocumentTableColumn:
        '''Gets a :py:class:`groupdocs.assembly.data.DocumentTableColumn` instance from the collection at the specified index.'''
        raise NotImplementedError()
    

class DocumentTableLoadArgs:
    '''Provides data for the :py:func:`groupdocs.assembly.data.IDocumentTableLoadHandler.handle` method.'''
    
    @property
    def table_index(self) -> int:
        '''Gets the zero-based index of the corresponding document table to be loaded.'''
        raise NotImplementedError()
    
    @property
    def is_loaded(self) -> bool:
        '''Gets a value indicating whether the corresponding document table is to be loaded or not.
        The default value is true.'''
        raise NotImplementedError()
    
    @is_loaded.setter
    def is_loaded(self, value : bool) -> None:
        '''Sets a value indicating whether the corresponding document table is to be loaded or not.
        The default value is true.'''
        raise NotImplementedError()
    
    @property
    def options(self) -> groupdocs.assembly.data.DocumentTableOptions:
        '''Gets :py:class:`groupdocs.assembly.data.DocumentTableOptions` to be used while loading the corresponding document table.
        The default value is null, which means that default :py:class:`groupdocs.assembly.data.DocumentTableOptions` are to be applied.'''
        raise NotImplementedError()
    
    @options.setter
    def options(self, value : groupdocs.assembly.data.DocumentTableOptions) -> None:
        '''Sets :py:class:`groupdocs.assembly.data.DocumentTableOptions` to be used while loading the corresponding document table.
        The default value is null, which means that default :py:class:`groupdocs.assembly.data.DocumentTableOptions` are to be applied.'''
        raise NotImplementedError()
    

class DocumentTableOptions:
    '''Provides a set of options to control extraction of data from a document table.'''
    
    def __init__(self) -> None:
        '''Creates a new instance of this class.'''
        raise NotImplementedError()
    
    @property
    def min_row_index(self) -> int:
        '''Gets the smallest zero-based index of a row to be extracted from a document table.
        The default value is negative which means that the smallest row index is not limited.'''
        raise NotImplementedError()
    
    @min_row_index.setter
    def min_row_index(self, value : int) -> None:
        '''Sets the smallest zero-based index of a row to be extracted from a document table.
        The default value is negative which means that the smallest row index is not limited.'''
        raise NotImplementedError()
    
    @property
    def max_row_index(self) -> int:
        '''Gets the largest zero-based index of a row to be extracted from a document table.
        The default value is negative which means that the largest row index is not limited.'''
        raise NotImplementedError()
    
    @max_row_index.setter
    def max_row_index(self, value : int) -> None:
        '''Sets the largest zero-based index of a row to be extracted from a document table.
        The default value is negative which means that the largest row index is not limited.'''
        raise NotImplementedError()
    
    @property
    def min_column_index(self) -> int:
        '''Gets the smallest zero-based index of a column to be extracted from a document table.
        The default value is negative which means that the smallest column index is not limited.'''
        raise NotImplementedError()
    
    @min_column_index.setter
    def min_column_index(self, value : int) -> None:
        '''Sets the smallest zero-based index of a column to be extracted from a document table.
        The default value is negative which means that the smallest column index is not limited.'''
        raise NotImplementedError()
    
    @property
    def max_column_index(self) -> int:
        '''Gets the largest zero-based index of a column to be extracted from a document table.
        The default value is negative which means that the largest column index is not limited.'''
        raise NotImplementedError()
    
    @max_column_index.setter
    def max_column_index(self, value : int) -> None:
        '''Sets the largest zero-based index of a column to be extracted from a document table.
        The default value is negative which means that the largest column index is not limited.'''
        raise NotImplementedError()
    
    @property
    def first_row_contains_column_names(self) -> bool:
        '''Gets a value indicating whether column names are to be obtained from the first
        extracted row of a document table. The default value is false.'''
        raise NotImplementedError()
    
    @first_row_contains_column_names.setter
    def first_row_contains_column_names(self, value : bool) -> None:
        '''Sets a value indicating whether column names are to be obtained from the first
        extracted row of a document table. The default value is false.'''
        raise NotImplementedError()
    

class DocumentTableRelation:
    '''Represents a parent-child relationship between two :py:class:`groupdocs.assembly.data.DocumentTable` objects.'''
    
    @property
    def parent_column(self) -> groupdocs.assembly.data.DocumentTableColumn:
        '''Gets the parent column of this relation.'''
        raise NotImplementedError()
    
    @property
    def child_column(self) -> groupdocs.assembly.data.DocumentTableColumn:
        '''Gets the child column of this relation.'''
        raise NotImplementedError()
    

class DocumentTableRelationCollection:
    '''Represents the collection of :py:class:`groupdocs.assembly.data.DocumentTableRelation` objects of a single :py:class:`groupdocs.assembly.data.DocumentTableSet`
    instance.'''
    
    def add(self, parent_column : groupdocs.assembly.data.DocumentTableColumn, child_column : groupdocs.assembly.data.DocumentTableColumn) -> groupdocs.assembly.data.DocumentTableRelation:
        '''Creates a :py:class:`groupdocs.assembly.data.DocumentTableRelation` object for the specified parent and child columns, and adds it
        to the collection.
        
        :param parent_column: The parent column of the relation.
        :param child_column: The child column of the relation.
        :returns: The created relation.'''
        raise NotImplementedError()
    
    def remove(self, relation : groupdocs.assembly.data.DocumentTableRelation) -> None:
        '''Removes the specified relation from the collection.
        
        :param relation: The relation to remove.'''
        raise NotImplementedError()
    
    def remove_at(self, index : int) -> None:
        '''Removes the relation at the specified index from the collection.
        
        :param index: The index of the relation to remove.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Clears the collection of any relations.'''
        raise NotImplementedError()
    
    def contains(self, relation : groupdocs.assembly.data.DocumentTableRelation) -> bool:
        '''Returns a value indicating whether this collection contains the specified relation.
        
        :param relation: A relation to look for.
        :returns: A value indicating whether this collection contains the specified relation.'''
        raise NotImplementedError()
    
    def index_of(self, relation : groupdocs.assembly.data.DocumentTableRelation) -> int:
        '''Returns the index of the specified relation within this collection.
        
        :param relation: A relation to find.
        :returns: The zero-based index of the specified relation, or -1 if the relation does not exist in this collection.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the total number of :py:class:`groupdocs.assembly.data.DocumentTableRelation` objects in the collection.'''
        raise NotImplementedError()
    
    def __getitem__(self, key : int) -> groupdocs.assembly.data.DocumentTableRelation:
        '''Gets a :py:class:`groupdocs.assembly.data.DocumentTableRelation` instance from the collection at the specified index.'''
        raise NotImplementedError()
    

class DocumentTableSet:
    '''Provides access to data of multiple tables (or spreadsheets) located in an external document to be used while
    assembling a document. Also, enables to define parent-child relations for the document tables thus simplifying
    access to related data within template documents.'''
    
    @overload
    def __init__(self, document_path : str) -> None:
        '''Creates a new instance of this class loading all tables from a document using default
        :py:class:`groupdocs.assembly.data.DocumentTableOptions`.
        
        :param document_path: The path to a document containing tables to be accessed.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document_path : str, load_handler : groupdocs.assembly.data.IDocumentTableLoadHandler) -> None:
        '''Creates a new instance of this class.
        
        :param document_path: The path to a document containing tables to be accessed.
        :param load_handler: An :py:class:`groupdocs.assembly.data.IDocumentTableLoadHandler` implementation controlling how document tables are loaded.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document_stream : io._IOBase) -> None:
        '''Creates a new instance of this class loading all tables from a document using default
        :py:class:`groupdocs.assembly.data.DocumentTableOptions`.
        
        :param document_stream: The stream containing a document with tables to be accessed.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, document_stream : io._IOBase, load_handler : groupdocs.assembly.data.IDocumentTableLoadHandler) -> None:
        '''Creates a new instance of this class.
        
        :param document_stream: The stream containing a document with tables to be accessed.
        :param load_handler: An :py:class:`groupdocs.assembly.data.IDocumentTableLoadHandler` implementation controlling how document tables are loaded.'''
        raise NotImplementedError()
    
    @property
    def tables(self) -> groupdocs.assembly.data.DocumentTableCollection:
        '''Gets the collection of :py:class:`groupdocs.assembly.data.DocumentTable` objects representing tables of this set.'''
        raise NotImplementedError()
    
    @property
    def relations(self) -> groupdocs.assembly.data.DocumentTableRelationCollection:
        '''Gets the collection of parent-child relations defined for document tables of this set.'''
        raise NotImplementedError()
    

class IDocumentTableLoadHandler:
    '''Overrides default loading of :py:class:`groupdocs.assembly.data.DocumentTable` objects while creating a :py:class:`groupdocs.assembly.data.DocumentTableSet`
    instance.'''
    
    def handle(self, args : groupdocs.assembly.data.DocumentTableLoadArgs) -> None:
        '''Overrides default loading of a particular :py:class:`groupdocs.assembly.data.DocumentTable` object while creating
        a :py:class:`groupdocs.assembly.data.DocumentTableSet` instance.'''
        raise NotImplementedError()
    

class JsonDataLoadOptions:
    '''Represents options for parsing JSON data.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of this class with default options.'''
        raise NotImplementedError()
    
    @property
    def simple_value_parse_mode(self) -> groupdocs.assembly.data.JsonSimpleValueParseMode:
        '''Gets a mode for parsing JSON simple values (null, boolean, number, integer, and string)
        while loading JSON. Such a mode does not affect parsing of date-time values. The default is
        :py:attr:`groupdocs.assembly.data.JsonSimpleValueParseMode.LOOSE`.'''
        raise NotImplementedError()
    
    @simple_value_parse_mode.setter
    def simple_value_parse_mode(self, value : groupdocs.assembly.data.JsonSimpleValueParseMode) -> None:
        '''Sets a mode for parsing JSON simple values (null, boolean, number, integer, and string)
        while loading JSON. Such a mode does not affect parsing of date-time values. The default is
        :py:attr:`groupdocs.assembly.data.JsonSimpleValueParseMode.LOOSE`.'''
        raise NotImplementedError()
    
    @property
    def exact_date_time_parse_format(self) -> str:
        '''Gets an exact format for parsing JSON date-time values while loading JSON. The default is **null**.'''
        raise NotImplementedError()
    
    @exact_date_time_parse_format.setter
    def exact_date_time_parse_format(self, value : str) -> None:
        '''Sets an exact format for parsing JSON date-time values while loading JSON. The default is **null**.'''
        raise NotImplementedError()
    
    @property
    def exact_date_time_parse_formats(self) -> Iterable[str]:
        '''Gets exact formats for parsing JSON date-time values while loading JSON. The default is **null**.'''
        raise NotImplementedError()
    
    @exact_date_time_parse_formats.setter
    def exact_date_time_parse_formats(self, value : Iterable[str]) -> None:
        '''Sets exact formats for parsing JSON date-time values while loading JSON. The default is **null**.'''
        raise NotImplementedError()
    
    @property
    def always_generate_root_object(self) -> bool:
        '''Gets a flag indicating whether a generated data source will always contain an object for a JSON root
        element. If a JSON root element contains a single complex property, such an object is not created by default.'''
        raise NotImplementedError()
    
    @always_generate_root_object.setter
    def always_generate_root_object(self, value : bool) -> None:
        '''Sets a flag indicating whether a generated data source will always contain an object for a JSON root
        element. If a JSON root element contains a single complex property, such an object is not created by default.'''
        raise NotImplementedError()
    

class JsonDataSource:
    '''Provides access to data of a JSON file or stream to be used while assembling a document.'''
    
    @overload
    def __init__(self, json_path : str) -> None:
        '''Creates a new data source with data from a JSON file using default options for parsing JSON data.
        
        :param json_path: The path to the JSON file to be used as the data source.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, json_path : str, options : groupdocs.assembly.data.JsonDataLoadOptions) -> None:
        '''Creates a new data source with data from a JSON file using the specified options for parsing JSON data.
        
        :param json_path: The path to the JSON file to be used as the data source.
        :param options: Options for parsing JSON data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, json_stream : io._IOBase) -> None:
        '''Creates a new data source with data from a JSON stream using default options for parsing JSON data.
        
        :param json_stream: The stream of JSON data to be used as the data source.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, json_stream : io._IOBase, options : groupdocs.assembly.data.JsonDataLoadOptions) -> None:
        '''Creates a new data source with data from a JSON stream using the specified options for parsing JSON data.
        
        :param json_stream: The stream of JSON data to be used as the data source.
        :param options: Options for parsing JSON data.'''
        raise NotImplementedError()
    

class XmlDataLoadOptions:
    '''Represents options for XML data loading.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of this class with default options.'''
        raise NotImplementedError()
    
    @property
    def always_generate_root_object(self) -> bool:
        '''Gets a flag indicating whether a generated data source will always contain an object for an XML root
        element. If an XML root element has no attributes and all its child elements have same names, such an object
        is not created by default.'''
        raise NotImplementedError()
    
    @always_generate_root_object.setter
    def always_generate_root_object(self, value : bool) -> None:
        '''Sets a flag indicating whether a generated data source will always contain an object for an XML root
        element. If an XML root element has no attributes and all its child elements have same names, such an object
        is not created by default.'''
        raise NotImplementedError()
    

class XmlDataSource:
    '''Provides access to data of an XML file or stream to be used while assembling a document.'''
    
    @overload
    def __init__(self, xml_path : str) -> None:
        '''Creates a new data source with data from an XML file using default options for XML data loading.
        
        :param xml_path: The path to the XML file to be used as the data source.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_stream : io._IOBase) -> None:
        '''Creates a new data source with data from an XML stream using default options for XML data loading.
        
        :param xml_stream: The stream of XML data to be used as the data source.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_path : str, xml_schema_path : str) -> None:
        '''Creates a new data source with data from an XML file using an XML Schema Definition file. Default options
        are used for XML data loading.
        
        :param xml_path: The path to the XML file to be used as the data source.
        :param xml_schema_path: The path to the XML Schema Definition file that provides schema for the XML
        file.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_stream : io._IOBase, xml_schema_stream : io._IOBase) -> None:
        '''Creates a new data source with data from an XML stream using an XML Schema Definition stream. Default options
        are used for XML data loading.
        
        :param xml_stream: The stream of XML data to be used as the data source.
        :param xml_schema_stream: The stream of XML Schema Definition that provides schema for the XML data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_path : str, options : groupdocs.assembly.data.XmlDataLoadOptions) -> None:
        '''Creates a new data source with data from an XML file using the specified options for XML data loading.
        
        :param xml_path: The path to the XML file to be used as the data source.
        :param options: Options for XML data loading.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_stream : io._IOBase, options : groupdocs.assembly.data.XmlDataLoadOptions) -> None:
        '''Creates a new data source with data from an XML stream using the specified options for XML data loading.
        
        :param xml_stream: The stream of XML data to be used as the data source.
        :param options: Options for XML data loading.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_path : str, xml_schema_path : str, options : groupdocs.assembly.data.XmlDataLoadOptions) -> None:
        '''Creates a new data source with data from an XML file using an XML Schema Definition file. The specified
        options are used for XML data loading.
        
        :param xml_path: The path to the XML file to be used as the data source.
        :param xml_schema_path: The path to the XML Schema Definition file that provides schema for the XML
        file.
        :param options: Options for XML data loading.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, xml_stream : io._IOBase, xml_schema_stream : io._IOBase, options : groupdocs.assembly.data.XmlDataLoadOptions) -> None:
        '''Creates a new data source with data from an XML stream using an XML Schema Definition stream. The specified
        options are used for XML data loading.
        
        :param xml_stream: The stream of XML data to be used as the data source.
        :param xml_schema_stream: The stream of XML Schema Definition that provides schema for the XML data.
        :param options: Options for XML data loading.'''
        raise NotImplementedError()
    

class JsonSimpleValueParseMode:
    '''Specifies a mode for parsing JSON simple values (null, boolean, number, integer, and string) while loading JSON.
    Such a mode does not affect parsing of date-time values.'''
    
    LOOSE : JsonSimpleValueParseMode
    '''Specifies the mode where types of JSON simple values are determined upon parsing of their string representations.
    For example, the type of \'prop\' from the JSON snippet \'{ prop: "123" }\' is determined as integer in this mode.'''
    STRICT : JsonSimpleValueParseMode
    '''Specifies the mode where types of JSON simple values are determined from JSON notation itself.
    For example, the type of \'prop\' from the JSON snippet \'{ prop: "123" }\' is determined as string in this mode.'''

