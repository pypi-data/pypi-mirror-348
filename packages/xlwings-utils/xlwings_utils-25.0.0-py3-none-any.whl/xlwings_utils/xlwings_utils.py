#         _            _                                   _    _  _
#  __  __| |__      __(_) _ __    __ _  ___         _   _ | |_ (_)| | ___
#  \ \/ /| |\ \ /\ / /| || '_ \  / _` |/ __|       | | | || __|| || |/ __|
#   >  < | | \ V  V / | || | | || (_| |\__ \       | |_| || |_ | || |\__ \
#  /_/\_\|_|  \_/\_/  |_||_| |_| \__, ||___/ _____  \__,_| \__||_||_||___/
#                                |___/      |_____|

__version__ = "25.0.0"


import dropbox
from pathlib import Path
import os
import sys

dbx = None
Pythonista = sys.platform == "ios"


def dropbox_init(refresh_token=None, app_key=None, app_secret=None):
    """
    dropbox initialize

    This function may to be called prior to using any dropbox function
    to specify the request token, app key and app secret.
    If these are specified as REFRESH_TOKEN, APP_KEY and APP_SECRET
    environment variables, it is no necessary to call dropbox_init().

    Parameters
    ----------
    refresh_token : str
        oauth2 refreshntoken

        if omitted: use the environment variable REFRESH_TOKEN

    app_key : str
        app key

        if omitted: use the environment variable APP_KEY


    app_secret : str
        app secret

        if omitted: use the environment variable APP_SECRET

    Returns
    -------
    -
    """
    global dbx

    if Pythonista:
        # under Pythonista, the environ is updated from the .environ.toml file, if present
        environ_file = Path(os.environ["HOME"]) / "Documents" / ".environ.toml"

        if environ_file.is_file():
            with open(environ_file, "r") as f:
                import toml

                d = toml.load(f)
                os.environ.update(d)

    if refresh_token is None:
        if "REFRESH_TOKEN" in os.environ:
            refresh_token = os.environ["REFRESH_TOKEN"]
        else:
            raise ValueError("no REFRESH_TOKEN found in environment.")
    if app_key is None:
        if "APP_KEY" in os.environ:
            app_key = os.environ["APP_KEY"]
        else:
            raise ValueError("no APP_KEY found in environment.")
    if app_secret is None:
        if "APP_SECRET" in os.environ:
            app_secret = os.environ["APP_SECRET"]
        else:
            raise ValueError("no APP_SECRET found in environment.")

    dbx = dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=app_key, app_secret=app_secret)
    try:
        dbx.files_list_folder(path="")  # just to test proper credentials
    except dropbox.exceptions.AuthError:
        raise ValueError("invalid dropbox credentials")


def _login_dbx():
    if dbx is None:
        dropbox_init()  # use environment


def list_dropbox(path="", recursive=False, show_files=True, show_folders=False):
    """
    list_dropbox

    returns all dropbox files/folders in path

    Parameters
    ----------
    path : str or Pathlib.Path
        path from which to list all files (default: '')

    recursive : bool
        if True, recursively list files. if False (default) no recursion

    show_files : bool
        if True (default), show file entries
        if False, do not show file entries

    show_folders : bool
        if True, show folder entries
        if False (default), do not show folder entries

    Returns
    -------
    files : list

    Note
    ----
    Directory entries are never returned

    Note
    ----
    If REFRESH_TOKEN, APP_KEY and APP_SECRET environment variables are specified,
    it is not necessary to call dropbox_init() prior to any dropbox function.
    """
    _login_dbx()
    out = []
    result = dbx.files_list_folder(path, recursive=recursive)

    for entry in result.entries:
        if show_files and isinstance(entry, dropbox.files.FileMetadata):
            out.append(entry.path_display)
        if show_folders and isinstance(entry, dropbox.files.FolderMetadata):
            out.append(entry.path_display + "/")

    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)
        for entry in result.entries:
            if show_files and isinstance(entry, dropbox.files.FileMetadata):
                out.append(entry.path_display)
            if show_folders and isinstance(entry, dropbox.files.FolderMetadata):
                out.append(entry.path_display + "/")

    return out


def read_dropbox(dropbox_path):
    """
    read_dropbox

    read from dopbox at given path

    Parameters
    ----------
    dropbox_path : str or Pathlib.Path
        path to read from

    Returns
    -------
    contents of the dropbox file : bytes

    Note
    ----
    If REFRESH_TOKEN, APP_KEY and APP_SECRET environment variables are specified,
    it is not necessary to call dropbox_init() prior to any dropbox function.
    """

    _login_dbx()
    metadata, response = dbx.files_download(dropbox_path)
    file_content = response.content
    return file_content


def write_dropbox(dropbox_path, contents):
    _login_dbx()
    """
    write_dropbox
    
    write from dopbox at given path
    
    Parameters
    ----------
    dropbox_path : str or Pathlib.Path
        path to write to

    contents : bytes
        contents to be written
        
    Note
    ----
    If REFRESH_TOKEN, APP_KEY and APP_SECRET environment variables are specified,
    it is not necessary to call dropbox_init() prior to any dropbox function.
    """
    dbx.files_upload(contents, dropbox_path, mode=dropbox.files.WriteMode.overwrite)


def list_local(path, recursive=False, show_files=True, show_folders=False):
    """
    list_local

    returns all local files/folders in path

    Parameters
    ----------
    path : str or Pathlib.Path
        path from which to list all files (default: '')

    recursive : bool
        if True, recursively list files. if False (default) no recursion

    show_files : bool
        if True (default), show file entries
        if False, do not show file entries

    show_folders : bool
        if True, show folder entries
        if False (default), do not show folder entries

    Returns
    -------
    files, relative to path : list
    """
    path = Path(path)

    result = []
    for entry in path.iterdir():
        if entry.is_file():
            if show_files:
                result.append(str(entry))
        elif entry.is_dir():
            if show_folders:
                result.append(str(entry) + "/")
            if recursive:
                result.extend(list_local(entry, recursive=recursive, show_files=show_files, show_folders=show_folders))
    return result


def write_local(path, contents):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)


def read_local(path):
    path = Path(path)
    with open(path, "rb") as f:
        contents = f.read()
    return contents


class block:
    """
    block is 2 dimensional data structure with 1 as lowest index (like xlwings range)

    Parameters
    ----------
    number_of_rows : int
        number of rows

    number_of_columns : int
        number of columns

    Returns
    -------
    block
    """

    def __init__(self, value=None, *, number_of_rows=None, number_of_columns=None, column_like=False):
        self.dict = {}
        self.column_like = column_like
        if value is None:
            if number_of_rows is None:
                number_of_rows = 1
            if number_of_columns is None:
                number_of_columns = 1
            self.number_of_rows = number_of_rows
            self.number_of_columns = number_of_columns

        else:
            if isinstance(value, block):
                value = value.value
            self.value = value
            if number_of_rows is not None:
                self.number_of_rows = number_of_rows
            if number_of_columns is not None:
                self.number_of_columns = number_of_columns

    @property
    def value(self):
        return [[self.dict.get((row, column)) for column in range(1, self.number_of_columns + 1)] for row in range(1, self.number_of_rows + 1)]

    @value.setter
    def value(self, value):
        if not isinstance(value, list):
            value = [[value]]
        if not isinstance(value[0], list):
            if self.column_like:
                value = [[item] for item in value]
            else:
                value = [value]

        self.number_of_rows = len(value)
        self._number_of_columns = 0

        for row, row_contents in enumerate(value, 1):
            for column, item in enumerate(row_contents, 1):
                if item is not None:
                    self.dict[row, column] = item
                    self._number_of_columns = max(self.number_of_columns, column)

    def __setitem__(self, row_column, value):
        row, column = row_column
        if row < 1 or row > self.number_of_rows:
            raise IndexError(f"row must be between 1 and {self.number_of_rows} not {row}")
        if column < 1 or column > self.number_of_columns:
            raise IndexError(f"column must be between 1 and {self.number_of_columns} not {column}")
        self.dict[row, column] = value

    def __getitem__(self, row_column):
        row, column = row_column
        if row < 1 or row > self.number_of_rows:
            raise IndexError(f"row must be between 1 and {self.number_of_rows} not {row}")
        if column < 1 or column > self.number_of_columns:
            raise IndexError(f"column must be between 1 and {self.number_of_columns} not {column}")
        return self.dict.get((row, column))

    def minimized(self):
        return block(self, number_of_rows=self.highest_used_row_number, number_of_columns=self.highest_used_column_number)

    @property
    def number_of_rows(self):
        return self._number_of_rows

    @number_of_rows.setter
    def number_of_rows(self, value):
        if value < 1:
            raise ValueError(f"number_of_rows should be >=1, not {value}")
        self._number_of_rows = value
        for row, column in list(self.dict):
            if row > self._number_of_rows:
                del self.dict[row, column]

    @property
    def number_of_columns(self):
        return self._number_of_columns

    @number_of_columns.setter
    def number_of_columns(self, value):
        if value < 1:
            raise ValueError(f"number_of_columns should be >=1, not {value}")
        self._number_of_columns = value
        for row, column in list(self.dict):
            if column > self._number_of_columns:
                del self.dict[row, column]

    @property
    def highest_used_row_number(self):
        if self.dict:
            return max(row for (row, column) in self.dict)
        else:
            return 1

    @property
    def highest_used_column_number(self):
        if self.dict:
            return max(column for (row, column) in self.dict)
        else:
            return 1

    def __repr__(self):
        return f"block({self.value})"



class _capture:
    """
    specifies how to capture stdout

    Parameters
    ----------
    include_print : bool
        if True (default), the output is also printed out as normal

        if False, no output is printed

    Note
    ----
    Use this function as a context manager, like ::

        with capture_stdout():
            ...
    """

    def __init__(self):
        self.stdout = sys.stdout
        self._include_print = False
        self._buffer=[]

    def __enter__(self):
        sys.stdout = self

    def __exit__(self, exc_type, exc_value, tb):
        sys.stdout = self.stdout

    def write(self, data):
        self._buffer.append(data)
        if self._include_print:
            self.stdout.write(data)

    def flush(self):
        if self._include_print:
            self.stdout.flush()
        self._buffer.append("\n")
        

    @property
    def value(self):
        result=self.value_keep
        self.clear()
        return result
        
        
    @property
    def value_keep(self):
        result= [[line] for line in self.str_keep.splitlines()]
        return result
        
    @property
    def str(self):
        result = self.str_keep
        self._buffer.clear()
        return result        
        
    @property
    def str_keep(self):
        result = "".join(self._buffer)
        return result        
        
    def clear(self):
        self._buffer.clear()
        
        
    @property
    def include_print(self):
        return self._include_print
        
    @include_print.setter
    def include_print(self, value):
        self._include_print=value
        


def reset():
    capture.include_print=False
    capture.clear()
    
capture=_capture()


if __name__ == "__main__":
    ...
