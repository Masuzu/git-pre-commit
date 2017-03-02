# git-pre-commit

pre-commit hook for Git to reorganize imports and remove trailing spaces

Requires python 2.6+

Copy the contents into your `.git/hooks` folder and update the permissions of the `pre-commit` file to make it executable.
To disable the hook, simply rename the file `pre-commit` by postpending it with an extension suffix for instance.

Supported languages for import organization:
- java
- scala