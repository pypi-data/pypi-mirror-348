## Includes:
Better Serato USB export. Beats Serato's sync by putting all files in 1 folder (without duplicates) and only copying changed files, unlike Serato's sync which takes forever and creates many duplicate file locations

**Currently designed for Python 3.12+. If you would like backwards compatibility with an older version, please reach out!**

# Installation

```cmd
pip install serato-usb-export
```

# Examples

**NOTE: replaces existing crates on flash drive! (but does not delete existing track files) (TODO: ability to merge with existing)**

```cmd
>>> serato_usb_export --drive E --crate_matcher *house* *techno* --root_crate="Dave USB"
```

_This is a wrapper of my [serato-tools](https://github.com/bvandercar-vt/serato-tools) package. Please open issues and contriute there._