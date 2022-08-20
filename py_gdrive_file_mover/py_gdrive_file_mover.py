# SPDX-FileCopyrightText: 2022 Daniele Tentoni <daniele.tentoni.1996@gmail.com>
#
# SPDX-License-Identifier: MIT

import os
import sys
import click

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def auth():
    """
    Execute the authentication on GDrive apis.
    """
    creds = None
    SCOPES = [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://www.googleapis.com/auth/drive",
    ]
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(
                f"You are in {os.path.curdir} {os.path.abspath(os.path.curdir)} {os.path.join(os.path.abspath(os.path.curdir), 'credentials.json')}"
            )
            if not os.path.exists(
                os.path.join(os.path.abspath(os.path.curdir), "credentials.json")
            ):
                print("Missing credentials.json file")

            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def search_file(filters, *args, **kwargs):
    """
    Search file in drive location.

    :param verbose: Make this function more verbose
    :type verbose: bool

    Took code from: https://developers.google.com/drive/api/guides/search-files
    """
    # creds, _ = google.auth.default()
    creds = auth()
    verbose = kwargs.get("verbose", False)

    try:
        service = build("drive", "v3", credentials=creds)
        files = []
        page_token = None
        while True:
            queries = []
            # Add this if you wanna filter only folders
            # queries.append("mimeType='application/vnd.google-apps.folder'")
            if verbose:
                print(f"You are using {filters}[{type(filters)}] for filter")

            if isinstance(filters, str):
                if verbose:
                    print(f"You are filtering only for {filters}")

                queries.append(f"name contains '{filters}'")
            else:
                name_queries = []
                for filter in filters:
                    if verbose:
                        print(f"You are filtering even for {filter}")

                    name_queries.append(f"name contains '{filter}'")

                queries.append(" or ".join(name_queries))

            query = " and ".join(queries)
            if verbose:
                print(f"Try to use {query} as filter")

            response = (
                service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, parents)",
                    pageToken=page_token,
                )
                .execute()
            )
            for file in response.get("files", []):
                name = file.get("name")
                id = file.get("id")
                print(f"Name: {name}, ID: {id}, parents: {file.get('parents')}")

            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None

    return files


def move_file_to_folder(real_file_id, real_folder_id, *args, **kwargs):
    """
    Move specified file to specified folder.

    Took code from: https://developers.google.com/drive/api/guides/folder#move_files_between_folders

    :param real_file_id: Id of the file to move
    :type real_file_id: str
    :param real_folder_id: Id of the folder
    :type real_folder_id: str

    :todo: Implement OAuth2 in the application.
    """
    # creds, _ = google.auth.default()
    creds = auth()
    noop = kwargs.get("noop", False)

    try:
        service = build("drive", "v3", credentials=creds)
        file = service.files().get(fileId=real_file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))
        if not noop:
            file = (
                service.files()
                .update(
                    fileId=real_file_id,
                    addParents=real_folder_id,
                    removeParents=previous_parents,
                    fields="id, parents",
                )
                .execute()
            )
        else:
            file = (
                service.files()
                .update(
                    fileId=real_file_id,
                    fields="id, parents",
                )
                .execute()
            )

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("parents")


@click.command()
@click.option(
    "-v", "--verbose", "verbose", help="print more output", is_flag=True, default=False
)
@click.option(
    "--no-op",
    "noop",
    help="execute program without making any operation",
    is_flag=True,
    default=False,
)
@click.argument("files", nargs=-1)
@click.argument("folder", nargs=1)
def move(files, folder, verbose: bool, noop: bool):
    """
    Move files from their current position to folder given.

    FILES is the list of arguments containing path of files to move.
    FOLDER is the folder where place files.

    :param files: Files to move. You can move any file you want giving their absolute path in your Google Drive account. You can use the special char * to move every file inside a given path.
    :type files: str
    :param folder: Folder to reach. Only one folder is allowed.
    :param folder: str
    """
    expanded_list = search_file(files, verbose=verbose)
    target_object = search_file(folder, verbose=verbose)
    if not noop:
        click.echo(
            f"Move many files to another position {files} {folder} {expanded_list}"
        )
        move_file_to_folder(
            expanded_list[0].get("id"), target_object[0].get("id"), verbose=verbose
        )
    else:
        print(
            f"Object {expanded_list[0].get('name')} should has been moved to {target_object[0].get('name')}, but noop"
        )


if __name__ == "__main__":
    move(sys.argv[1:])
