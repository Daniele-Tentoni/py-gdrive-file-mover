''''''''''''''''''''''
Py GDrive File Mover
''''''''''''''''''''''
""""""""""""""""""""""""""""""""""
My personal GDrive file utility.
""""""""""""""""""""""""""""""""""

Remember that you need a Credentials file from GDrive to use this utility. The CLI expose only one command to move one or more file from his/their current location to another. Advice and suggestions are welcome.

Purpouse
''''''''''''''''''''

In my summer holiday mornings I was bored and I thought that this could be a very small project to make before return to work. No other purposes, I don't think I will use this so much often, but sometimes I would move files around in my GDrive storage for some reason. Use this tool only if you know what are you doing and to what files are you giving access.

How to use
''''''''''

First at all, you need to authenticate with yuor account. First time you execute the program, you will be asked to give your authorization to manipulate your files on Google Drive. than, you can move files around as your pleasure using the following command::

    $ python py_gdrive_file_mover/py_gdrive_file_mover.py Prova111 Test111

Use `--help` option to see more info about possibility of this command.

If you want to use this utility as a cronjob, add to your repository the necessary credentials.json and token.json (make the repo private) and use the cronjob github action to run your software. Remember that you have only 2000 minutes for Github Actions for Free Github Plan Users.

How to contribute
''''''''''''''''''

Open issues and pull request, but since this is a very useless project, don't expect I spend more than half hour a week on it to respond to isses or review pull requests.

License
''''''''

I've used REUSE to add license to this project, look at LICENSES folder for them and to https://reuse.software for more info about that tool.
