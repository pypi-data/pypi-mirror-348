
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

class BarcodeSettings:
    '''Represents a set of settings controlling barcode generation while assembling a document.'''
    
    @property
    def graphics_unit(self) -> groupdocs.assembly.GraphicsUnit:
        '''Gets a graphics unit used to measure :py:attr:`groupdocs.assembly.BarcodeSettings.base_x_dimension` and :py:attr:`groupdocs.assembly.BarcodeSettings.base_y_dimension`.
        The default value is :py:attr:`groupdocs.assembly.GraphicsUnit.MILLIMETER`.'''
        raise NotImplementedError()
    
    @graphics_unit.setter
    def graphics_unit(self, value : groupdocs.assembly.GraphicsUnit) -> None:
        '''Sets a graphics unit used to measure :py:attr:`groupdocs.assembly.BarcodeSettings.base_x_dimension` and :py:attr:`groupdocs.assembly.BarcodeSettings.base_y_dimension`.
        The default value is :py:attr:`groupdocs.assembly.GraphicsUnit.MILLIMETER`.'''
        raise NotImplementedError()
    
    @property
    def base_x_dimension(self) -> float:
        '''Gets a base x-dimension, that is, the smallest width of the unit of barcode bars and spaces.
        Measured in :py:attr:`groupdocs.assembly.BarcodeSettings.graphics_unit`.'''
        raise NotImplementedError()
    
    @base_x_dimension.setter
    def base_x_dimension(self, value : float) -> None:
        '''Sets a base x-dimension, that is, the smallest width of the unit of barcode bars and spaces.
        Measured in :py:attr:`groupdocs.assembly.BarcodeSettings.graphics_unit`.'''
        raise NotImplementedError()
    
    @property
    def base_y_dimension(self) -> float:
        '''Gets a base y-dimension, that is, the smallest height of the unit of 2D barcode modules.
        Measured in :py:attr:`groupdocs.assembly.BarcodeSettings.graphics_unit`.'''
        raise NotImplementedError()
    
    @base_y_dimension.setter
    def base_y_dimension(self, value : float) -> None:
        '''Sets a base y-dimension, that is, the smallest height of the unit of 2D barcode modules.
        Measured in :py:attr:`groupdocs.assembly.BarcodeSettings.graphics_unit`.'''
        raise NotImplementedError()
    
    @property
    def resolution(self) -> float:
        '''Gets the horizontal and vertical resolution of a barcode image being generated. Measured in dots
        per inch. The default value is 96.'''
        raise NotImplementedError()
    
    @resolution.setter
    def resolution(self, value : float) -> None:
        '''Sets the horizontal and vertical resolution of a barcode image being generated. Measured in dots
        per inch. The default value is 96.'''
        raise NotImplementedError()
    
    @property
    def x_resolution(self) -> float:
        '''Gets the horizontal resolution of a barcode image being generated. Measured in dots per inch.
        The default value is 96.'''
        raise NotImplementedError()
    
    @x_resolution.setter
    def x_resolution(self, value : float) -> None:
        '''Sets the horizontal resolution of a barcode image being generated. Measured in dots per inch.
        The default value is 96.'''
        raise NotImplementedError()
    
    @property
    def y_resolution(self) -> float:
        '''Gets the vertical resolution of a barcode image being generated. Measured in dots per inch.
        The default value is 96.'''
        raise NotImplementedError()
    
    @y_resolution.setter
    def y_resolution(self, value : float) -> None:
        '''Sets the vertical resolution of a barcode image being generated. Measured in dots per inch.
        The default value is 96.'''
        raise NotImplementedError()
    
    @property
    def use_auto_correction(self) -> bool:
        '''Gets a value indicating whether an invalid barcode value should be corrected automatically
        (if possible) to fit the barcode\'s specification or an exception should be thrown to indicate the error.
        The default value is true.'''
        raise NotImplementedError()
    
    @use_auto_correction.setter
    def use_auto_correction(self, value : bool) -> None:
        '''Sets a value indicating whether an invalid barcode value should be corrected automatically
        (if possible) to fit the barcode\'s specification or an exception should be thrown to indicate the error.
        The default value is true.'''
        raise NotImplementedError()
    

class DataSourceInfo:
    '''Provides information on a single data source object to be used to assemble a document from a template.'''
    
    @overload
    def __init__(self) -> None:
        '''Creates a new instance of this class without any properties specified.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data_source : Any) -> None:
        '''Creates a new instance of this class with the data source object specified.
        
        :param data_source: The data source object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data_source : Any, name : str) -> None:
        '''Creates a new instance of this class with the data source object and its name specified.
        
        :param data_source: The data source object.
        :param name: The name of the data source object to be used to access the data source object in a template document.'''
        raise NotImplementedError()
    
    @property
    def data_source(self) -> Any:
        '''Gets the data source object.'''
        raise NotImplementedError()
    
    @data_source.setter
    def data_source(self, value : Any) -> None:
        '''Sets the data source object.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the name of the data source object to be used to access the data source object in a template document.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name of the data source object to be used to access the data source object in a template document.'''
        raise NotImplementedError()
    

class DocumentAssembler:
    '''Provides routines to populate template documents with data and a set of settings to control these routines.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of this class.'''
        raise NotImplementedError()
    
    @overload
    def assemble_document(self, source_path : str, target_path : str, data_source_infos : List[groupdocs.assembly.DataSourceInfo]) -> bool:
        '''Loads a template document from the specified source path, populates the template document with data from
        the specified single or multiple sources, and stores the result document to the target path using default
        :py:class:`groupdocs.assembly.LoadSaveOptions`.
        
        :param source_path: The path to a template document to be populated with data.
        :param target_path: The path to a result document.
        :param data_source_infos: Provides information on data source objects to be used.
        :returns: A flag indicating whether parsing of the template document was successful. The returned flag makes sense only if
        a value of the :py:attr:`groupdocs.assembly.DocumentAssembler.options` property includes the :py:attr:`groupdocs.assembly.DocumentAssemblyOptions.INLINE_ERROR_MESSAGES`
        option.'''
        raise NotImplementedError()
    
    @overload
    def assemble_document(self, source_path : str, target_path : str, load_save_options : groupdocs.assembly.LoadSaveOptions, data_source_infos : List[groupdocs.assembly.DataSourceInfo]) -> bool:
        '''Loads a template document from the specified source path, populates the template document with data from
        the specified single or multiple sources, and stores the result document to the target path using the given
        :py:class:`groupdocs.assembly.LoadSaveOptions`.
        
        :param source_path: The path to a template document to be populated with data.
        :param target_path: The path to a result document.
        :param load_save_options: Specifies additional options for document loading and saving.
        :param data_source_infos: Provides information on data source objects to be used.
        :returns: A flag indicating whether parsing of the template document was successful. The returned flag makes sense only if
        a value of the :py:attr:`groupdocs.assembly.DocumentAssembler.options` property includes the :py:attr:`groupdocs.assembly.DocumentAssemblyOptions.INLINE_ERROR_MESSAGES`
        option.'''
        raise NotImplementedError()
    
    @overload
    def assemble_document(self, source_stream : io._IOBase, target_stream : io._IOBase, data_source_infos : List[groupdocs.assembly.DataSourceInfo]) -> bool:
        '''Loads a template document from the specified source stream, populates the template document with data from
        the specified single or multiple sources, and stores the result document to the target stream using default
        :py:class:`groupdocs.assembly.LoadSaveOptions`.
        
        :param source_stream: The stream to read a template document from.
        :param target_stream: The stream to write a result document.
        :param data_source_infos: Provides information on data source objects to be used.
        :returns: A flag indicating whether parsing of the template document was successful. The returned flag makes sense only if
        a value of the :py:attr:`groupdocs.assembly.DocumentAssembler.options` property includes the :py:attr:`groupdocs.assembly.DocumentAssemblyOptions.INLINE_ERROR_MESSAGES`
        option.'''
        raise NotImplementedError()
    
    @overload
    def assemble_document(self, source_stream : io._IOBase, target_stream : io._IOBase, load_save_options : groupdocs.assembly.LoadSaveOptions, data_source_infos : List[groupdocs.assembly.DataSourceInfo]) -> bool:
        '''Loads a template document from the specified source stream, populates the template document with data from
        the specified single or multiple sources, and stores the result document to the target stream using the given
        :py:class:`groupdocs.assembly.LoadSaveOptions`.
        
        :param source_stream: The stream to read a template document from.
        :param target_stream: The stream to write a result document.
        :param load_save_options: Specifies additional options for document loading and saving.
        :param data_source_infos: Provides information on data source objects to be used.
        :returns: A flag indicating whether parsing of the template document was successful. The returned flag makes sense only if
        a value of the :py:attr:`groupdocs.assembly.DocumentAssembler.options` property includes the :py:attr:`groupdocs.assembly.DocumentAssemblyOptions.INLINE_ERROR_MESSAGES`
        option.'''
        raise NotImplementedError()
    
    @property
    def options(self) -> groupdocs.assembly.DocumentAssemblyOptions:
        '''Gets a set of flags controlling behavior of this :py:class:`groupdocs.assembly.DocumentAssembler` instance
        while assembling a document.'''
        raise NotImplementedError()
    
    @options.setter
    def options(self, value : groupdocs.assembly.DocumentAssemblyOptions) -> None:
        '''Sets a set of flags controlling behavior of this :py:class:`groupdocs.assembly.DocumentAssembler` instance
        while assembling a document.'''
        raise NotImplementedError()
    
    @property
    def barcode_settings(self) -> groupdocs.assembly.BarcodeSettings:
        '''Gets a set of settings controlling barcode generation while assembling a document.'''
        raise NotImplementedError()
    
    @property
    def known_types(self) -> groupdocs.assembly.KnownTypeSet:
        '''Gets an unordered set (that is, a collection of unique items) containing :py:class:`System.Type` objects
        which fully or partially qualified names can be used within document templates processed by this
        assembler instance to invoke the corresponding types\' static members, perform type casts, etc.'''
        raise NotImplementedError()
    
    @staticmethod
    def set_use_reflection_optimization(value: bool) -> None:
        '''Gets a value indicating whether invocations of custom type members performed via reflection API are
        optimized using dynamic class generation or not. The default value is true.'''
    @property
    def use_reflection_optimization(self) -> bool:
        '''Sets a value indicating whether invocations of custom type members performed via reflection API are
        optimized using dynamic class generation or not. The default value is true.'''
        raise NotImplementedError()


class KnownTypeSet:
    '''Represents an unordered set (that is, a collection of unique items) containing :py:class:`System.Type` objects
    which fully or partially qualified names can be used within document templates to invoke the corresponding
    types\' static members, perform type casts, etc.'''
    
    def add(self, type : Type) -> None:
        raise NotImplementedError()
    
    def remove(self, type : Type) -> None:
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Removes all items from the set.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of items in the set.'''
        raise NotImplementedError()
    

class License:
    '''Provides methods to license the component.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of this class.'''
        raise NotImplementedError()
    
    @overload
    def set_license(self, license_name : str) -> None:
        '''Licenses the component.
        
        :param license_name: Can be a full or short file name.
        Use an empty string to switch to evaluation mode.'''
        raise NotImplementedError()
    
    @overload
    def set_license(self, stream : io._IOBase) -> None:
        '''Licenses the component.
        
        :param stream: A stream that contains the license.'''
        raise NotImplementedError()
    
    @property
    def is_licensed(self) -> bool:
        '''Returns true if a valid license has been applied; false if the component is running in evaluation mode.'''
        raise NotImplementedError()
    

class LoadSaveOptions:
    '''Specifies additional options for loading and saving of a document to be assembled.'''
    
    @overload
    def __init__(self) -> None:
        '''Creates a new instance of this class without any properties specified.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, save_format : groupdocs.assembly.FileFormat) -> None:
        '''Creates a new instance of this class with the specified file format to save an assembled document to.
        
        :param save_format: A file format to save an assembled document to.'''
        raise NotImplementedError()
    
    @property
    def save_format(self) -> groupdocs.assembly.FileFormat:
        '''Gets a file format to save an assembled document to. :py:attr:`groupdocs.assembly.FileFormat.UNSPECIFIED` is the default.'''
        raise NotImplementedError()
    
    @save_format.setter
    def save_format(self, value : groupdocs.assembly.FileFormat) -> None:
        '''Sets a file format to save an assembled document to. :py:attr:`groupdocs.assembly.FileFormat.UNSPECIFIED` is the default.'''
        raise NotImplementedError()
    
    @property
    def resource_load_base_uri(self) -> str:
        '''Gets a base URI to resolve external resource files\' relative URIs to absolute ones while loading an HTML
        template document to be assembled and saved to a non-HTML format. The default value is an empty string.'''
        raise NotImplementedError()
    
    @resource_load_base_uri.setter
    def resource_load_base_uri(self, value : str) -> None:
        '''Sets a base URI to resolve external resource files\' relative URIs to absolute ones while loading an HTML
        template document to be assembled and saved to a non-HTML format. The default value is an empty string.'''
        raise NotImplementedError()
    
    @property
    def resource_save_folder(self) -> str:
        '''Gets a path to a folder to store external resource files while an assembled document loaded from a non-HTML
        format is being saved to HTML. The default value is an empty string.'''
        raise NotImplementedError()
    
    @resource_save_folder.setter
    def resource_save_folder(self, value : str) -> None:
        '''Sets a path to a folder to store external resource files while an assembled document loaded from a non-HTML
        format is being saved to HTML. The default value is an empty string.'''
        raise NotImplementedError()
    

class Metered:
    '''Provides methods to work with metered licensing.'''
    
    def __init__(self) -> None:
        '''Creates a new instance of this class.'''
        raise NotImplementedError()
    
    def set_metered_key(self, public_key : str, private_key : str) -> None:
        '''Enables metered licensing for the component by specifying appropriate public and private metered keys.
        
        :param public_key: The public metered key.
        :param private_key: The private metered key.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_consumption_quantity() -> float:
        '''Returns the currently consumed number of megabytes.
        
        :returns: The currently consumed number of megabytes.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_consumption_credit() -> float:
        '''Returns the currently consumed number of credits.
        
        :returns: The currently consumed number of credits.'''
        raise NotImplementedError()
    

class DocumentAssemblyOptions:
    '''Specifies options controlling behavior of :py:class:`groupdocs.assembly.DocumentAssembler` while assembling a document.'''
    
    NONE : DocumentAssemblyOptions
    '''Specifies default options.'''
    ALLOW_MISSING_MEMBERS : DocumentAssemblyOptions
    '''Specifies that missing object members should be treated as null literals by the assembler. This option
    affects only access to instance (that is, non-static) object members and extension methods. If this
    option is not set, the assembler throws an exception when encounters a missing object member.'''
    UPDATE_FIELDS_AND_FORMULAS : DocumentAssemblyOptions
    '''Specifies that fields of result Word Processing documents and formulas of result Spreadsheet documents
    should be updated by the assembler.'''
    REMOVE_EMPTY_PARAGRAPHS : DocumentAssemblyOptions
    '''Specifies that the assembler should remove paragraphs becoming empty after template syntax tags are
    removed or replaced with empty values.'''
    INLINE_ERROR_MESSAGES : DocumentAssemblyOptions
    '''Specifies that the assembler should inline template syntax error messages into output documents.
    If this option is not set, the assembler throws an exception when encounters a syntax error.'''
    USE_SPREADSHEET_DATA_TYPES : DocumentAssemblyOptions
    '''Relates to Spreadsheet documents only. Specifies that evaluated expression results should be mapped to
    corresponding Spreadsheet data types, which also affects their default formatting within cells. If this
    option is not set, expression results are always written as strings by the assembler. This option has
    no effect when expression results are formatted using template syntax - expression results are always
    written as strings then as well.'''

class FileFormat:
    '''Specifies the format of a file.'''
    
    UNSPECIFIED : FileFormat
    '''Specifies an unset value. The default.'''
    DOC : FileFormat
    '''Specifies the Microsoft Word 97 - 2007 Binary Document format.'''
    DOT : FileFormat
    '''Specifies the Microsoft Word 97 - 2007 Binary Template format.'''
    DOCX : FileFormat
    '''Specifies the Office Open XML WordprocessingML Document (macro-free) format.'''
    DOCM : FileFormat
    '''Specifies the Office Open XML WordprocessingML Macro-Enabled Document format.'''
    DOTX : FileFormat
    '''Specifies the Office Open XML WordprocessingML Template (macro-free) format.'''
    DOTM : FileFormat
    '''Specifies the Office Open XML WordprocessingML Macro-Enabled Template format.'''
    FLAT_OPC : FileFormat
    '''Specifies the Office Open XML WordprocessingML format stored in a flat XML file instead of a ZIP package.'''
    FLAT_OPC_MACRO_ENABLED : FileFormat
    '''Specifies the Office Open XML WordprocessingML Macro-Enabled Document format stored in a flat XML file
    instead of a ZIP package.'''
    FLAT_OPC_TEMPLATE : FileFormat
    '''Specifies the Office Open XML WordprocessingML Template (macro-free) format stored in a flat XML file
    instead of a ZIP package.'''
    FLAT_OPC_TEMPLATE_MACRO_ENABLED : FileFormat
    '''Specifies the Office Open XML WordprocessingML Macro-Enabled Template format stored in a flat XML file
    instead of a ZIP package.'''
    WORD_ML : FileFormat
    '''Specifies the Microsoft Word 2003 WordprocessingML format.'''
    ODT : FileFormat
    '''Specifies the ODF Text Document format.'''
    OTT : FileFormat
    '''Specifies the ODF Text Document Template format.'''
    XLS : FileFormat
    '''Specifies the Microsoft Excel 97 - 2007 Binary Workbook format.'''
    XLSX : FileFormat
    '''Specifies the Office Open XML SpreadsheetML Workbook (macro-free) format.'''
    XLSM : FileFormat
    '''Specifies the Office Open XML SpreadsheetML Macro-Enabled Workbook format.'''
    XLTX : FileFormat
    '''Specifies the Office Open XML SpreadsheetML Template (macro-free) format.'''
    XLTM : FileFormat
    '''Specifies the Office Open XML SpreadsheetML Macro-Enabled Template format.'''
    XLAM : FileFormat
    '''Specifies the Office Open XML SpreadsheetML Macro-Enabled Add-in format.'''
    XLSB : FileFormat
    '''Specifies the Microsoft Excel 2007 Macro-Enabled Binary File format.'''
    SPREADSHEET_ML : FileFormat
    '''Specifies the Microsoft Excel 2003 SpreadsheetML format.'''
    ODS : FileFormat
    '''Specifies the ODF Spreadsheet format.'''
    PPT : FileFormat
    '''Specifies the Microsoft PowerPoint 97 - 2007 Binary Presentation format.'''
    PPS : FileFormat
    '''Specifies the Microsoft PowerPoint 97 - 2007 Binary Slide Show format.'''
    PPTX : FileFormat
    '''Specifies the Office Open XML PresentationML Presentation (macro-free) format.'''
    PPTM : FileFormat
    '''Specifies the Office Open XML PresentationML Macro-Enabled Presentation format.'''
    PPSX : FileFormat
    '''Specifies the Office Open XML PresentationML Slide Show (macro-free) format.'''
    PPSM : FileFormat
    '''Specifies the Office Open XML PresentationML Macro-Enabled Slide Show format.'''
    POTX : FileFormat
    '''Specifies the Office Open XML PresentationML Template (macro-free) format.'''
    POTM : FileFormat
    '''Specifies the Office Open XML PresentationML Macro-Enabled Template format.'''
    ODP : FileFormat
    '''Specifies the ODF Presentation format.'''
    MSG_ASCII : FileFormat
    '''Specifies the Microsoft Outlook Message (MSG) format using ASCII character encoding.'''
    MSG_UNICODE : FileFormat
    '''Specifies the Microsoft Outlook Message (MSG) format using Unicode character encoding.'''
    EML : FileFormat
    '''Specifies the MIME standard format.'''
    EMLX : FileFormat
    '''Specifies the Apple Mail.app program file format.'''
    RTF : FileFormat
    '''Specifies the RTF format.'''
    TEXT : FileFormat
    '''Specifies the plain text format.'''
    XML : FileFormat
    '''Specifies the XML format of a general form.'''
    XAML : FileFormat
    '''Specifies the Extensible Application Markup Language (XAML) format.'''
    XAML_PACKAGE : FileFormat
    '''Specifies the Extensible Application Markup Language (XAML) package format.'''
    HTML : FileFormat
    '''Specifies the HTML format.'''
    MHTML : FileFormat
    '''Specifies the MHTML (Web archive) format.'''
    XPS : FileFormat
    '''Specifies the XPS (XML Paper Specification) format.'''
    OPEN_XPS : FileFormat
    '''Specifies the OpenXPS (Ecma-388) format.'''
    PDF : FileFormat
    '''Specifies the PDF (Adobe Portable Document) format.'''
    EPUB : FileFormat
    '''Specifies the IDPF EPUB format.'''
    PS : FileFormat
    '''Specifies the PS (PostScript) format.'''
    PCL : FileFormat
    '''Specifies the PCL (Printer Control Language) format.'''
    SVG : FileFormat
    '''Specifies the SVG (Scalable Vector Graphics) format.'''
    TIFF : FileFormat
    '''Specifies the TIFF format.'''
    MARKDOWN : FileFormat
    '''Specifies the Markdown format.'''
    POT : FileFormat
    '''Specifies the Microsoft PowerPoint 97 - 2007 Binary Template format.'''
    OTP : FileFormat
    '''Specifies the ODF Presentation Template format.'''
    XLT : FileFormat
    '''Specifies the Microsoft Excel 97 - 2007 Binary Template format.'''

class GraphicsUnit:
    
    WORLD : GraphicsUnit
    '''Specifies the world coordinate system unit as the unit of measure.'''
    DISPLAY : GraphicsUnit
    '''Specifies the unit of measure of the display device. Typically pixels for video displays, and 1/100 inch for printers.'''
    PIXEL : GraphicsUnit
    '''Specifies a device pixel as the unit of measure.'''
    POINT : GraphicsUnit
    '''Specifies a printer\'s point (1/72 inch) as the unit of measure.'''
    INCH : GraphicsUnit
    '''Specifies the inch as the unit of measure.'''
    DOCUMENT : GraphicsUnit
    '''Specifies the document unit (1/300 inch) as the unit of measure.'''
    MILLIMETER : GraphicsUnit
    '''Specifies the millimeter as the unit of measure.'''

