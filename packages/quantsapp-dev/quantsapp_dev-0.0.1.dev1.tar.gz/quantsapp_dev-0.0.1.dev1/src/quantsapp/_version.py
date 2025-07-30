
"""
Module to expose more detailed version info for the installed `quantsapp`
"""

version: str = '0.0.1'
# version = '0.0.0.dev1+githash.fedcba987'
# version = '0.0.0.a1'  # Alpha
# version = '0.0.0.b1'  # Beta
# version = '0.0.0.rc1'  # Release candidate
__version__: str = version
full_version: str = version

# git_revision = "7be8c1f9133516fe20fd076f9bdfe23d9f537874"
release = 'dev' not in version and '+' not in version
short_version = version.split("+")[0]



# if __name__ == '__main__':
#     print(f"This module ({__file__}) is not supposed to invoke directly")