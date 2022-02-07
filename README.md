**CACHEPACKER** is a program to pack files in a folder into a file cache for use in the game The Beginner's Guide. It is meant to be used with the [CACHERIPPER](https://github.com/gamingwithevets/tbg-cachepacker) tool.

# Requirements
Again, only Python is required, but you can compile the program into an executable for people without Python.

# Usage
```
tbg_cachepacker.py [-h, --help] [-e, --export FILENAME] [-d, --disablelog] [-o, --overwrite] [-n, --newexport] [-p, --packcont] [-a, --autoexit] filecache_path [filecache_path ...]
```
## Parameters
| Parameter | Description |
|--|--|
| filecache_path | Directories to pack into the file cache. Paths with drive letters aren't supported at the moment. |
| -e, --export FILENAME | File cache name. Default is `filecache.bin`. |
| -d, --disablelog | Disable logging. The program has no log function at the moment, so this is useless. |
| -o, --overwrite | Overwrites the export file with the filename specified in `-e, --export` even if it exists.  |
| -n, --newexport | Prompts you to enter a new export file name if a file with the old name exists. |
| -p, --packcont | If only 1 folder is selected, packs its contents without asking. |
| -a, --autoexit | Skips the two Enter presses required to exit the program. |

# Examples
To pack files in the `files` and `files2` folder respectively, type:
```
python tbg_cachepacker.py files files2
```

To pack files in the `mmm` folder into `mmm.cache`, type:
```
python tbg_cachepacker.py mmm -e mmm.cache
```

# Planned Features
Here's a list of planned features for CACHEPACKER:
- Exiting takes 10 Enter presses without `-a, --autoexit`
- Compatibility with paths with drive letters
