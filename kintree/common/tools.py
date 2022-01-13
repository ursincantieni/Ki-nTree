import builtins
import json
import os
from shutil import copyfile


# CUSTOM PRINT METHOD
class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Overload print function with custom pretty-print


def cprint(*args, **kwargs):
    # Check if silent is set
    try:
        silent = kwargs.pop('silent')
    except:
        silent = False
    if not silent:
        if type(args[0]) is dict:
            return builtins.print(json.dumps(*args, **kwargs, indent=4, sort_keys=True))
        else:
            try:
                args = list(args)
                if 'warning' in args[0].lower():
                    args[0] = f'{pcolors.WARNING}{args[0]}{pcolors.ENDC}'
                elif 'error' in args[0].lower():
                    args[0] = f'{pcolors.ERROR}{args[0]}{pcolors.ENDC}'
                elif 'fail' in args[0].lower():
                    args[0] = f'{pcolors.ERROR}{args[0]}{pcolors.ENDC}'
                elif 'success' in args[0].lower():
                    args[0] = f'{pcolors.OKGREEN}{args[0]}{pcolors.ENDC}'
                elif 'pass' in args[0].lower():
                    args[0] = f'{pcolors.OKGREEN}{args[0]}{pcolors.ENDC}'
                elif 'main' in args[0].lower():
                    args[0] = f'{pcolors.HEADER}{args[0]}{pcolors.ENDC}'
                elif 'skipping' in args[0].lower():
                    args[0] = f'{pcolors.BOLD}{args[0]}{pcolors.ENDC}'
                args = tuple(args)
            except:
                pass
            return builtins.print(*args, **kwargs, flush=True)
###


def create_library(library_path: str, symbol: str, template_lib: str):
    ''' Create library files if they don\'t exist '''

    if not os.path.exists(library_path):
        os.mkdir(library_path)
    new_lib_file = os.path.join(library_path, symbol + '.lib')
    new_dcm_file = new_lib_file.replace('.lib', '.dcm')
    template_dcm = template_lib.replace('.lib', '.dcm')
    if not os.path.exists(new_lib_file):
        copyfile(template_lib, new_lib_file)
    if not os.path.exists(new_dcm_file):
        copyfile(template_dcm, new_dcm_file)


def download_image(image_url: str, image_full_path: str, silent=False) -> str:
    ''' Standard method to download image URL to local file '''
    import socket
    import urllib.request

    if not image_url:
        if not silent:
            cprint('[INFO]\tError: Missing image URL')
        return False

    def download(url, enable_headers=False):
        timeout = 3  # in seconds
        # Set default timeout for download socket
        socket.setdefaulttimeout(timeout)
        if enable_headers:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
        try:
            (image_filename, headers) = urllib.request.urlretrieve(url, filename=image_full_path)
        except socket.timeout:
            cprint(f'[INFO]\tWarning: Image download socket timed out ({timeout}s)', silent=silent)
            return None
        except urllib.error.HTTPError:
            cprint('[INFO]\tWarning: Image download failed (HTTP Error)', silent=silent)
            return None
        except urllib.error.URLError:
            cprint('[INFO]\tWarning: Image download failed (URL Error)', silent=silent)
            return None
        return image_filename
    
    # Try without headers
    image = download(image_url)

    if not image:
        # Try with headers
        image = download(image_url, enable_headers=True)

    # Still nothing
    if not image:
        return False

    return True
