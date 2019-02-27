from sys import platform
import os
from pathlib import Path

def get_settings_path(name, filename=None):
    """Figure out and return the directory where to save and load
    user preferences.
    
    On Linux, a directory `name` in the user's configuration directory is
    returned (usually under ``~/.config``).
    On Windows (including under Cygwin) the `name` directory in the user's
    ``Application Settings`` directory is returned.
    On Mac OS X the `name` directory under ``~/Library/Application Support``
    is returned.
    """
    
    
    if platform == "linux" or platform == "linux2":
        if 'XDG_CONFIG_HOME' in os.environ:
            return Path(os.environ['XDG_CONFIG_HOME'], name)
        else:
            return Path(os.path.expanduser('~/.config/%s' % name))
         
            
    elif platform == "darwin":
        return Path(os.path.expanduser('~/Library/Application Support/%s' % name))
    
    elif platform == "win32":
        if 'APPDATA' in os.environ:
            return Path(os.path.join(os.environ['APPDATA'], name).replace("\\","/"))
        
    else:
        return Path(os.path.expanduser('~/.%s' % name))     
    
    
print(locals())
print(globals)
