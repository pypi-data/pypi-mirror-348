#@+leo-ver=5-thin
#@+node:ekr.20250426044445.1: * @button backup
"""
Back up this .leo file.

os.environ['LEO_BACKUP'] must be the path to an existing (writable) directory.
"""
c.backup_helper(sub_dir='ekr-cache')
#@-leo

