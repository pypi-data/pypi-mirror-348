import glob
import os


def last_segment(path: str):
    *_, last = path.split('/')
    return last


def file_name_with_ext(path: str):
    return last_segment(path)


def file_ext(path: str):
    last = last_segment(path)
    parts = last.split('.')
    if len(parts) == 1:
        return ''
    return parts[-1:]


def file_name(path: str):
    last = last_segment(path)
    parts = last.split('.')
    if len(parts) == 1:
        return last
    return parts[:-1][0]


def parent_dirs(path: str):
    *dirs, _ = path.split('/')
    return '/'.join(dirs)


def path_without_ext(path: str):
    return f'{parent_dirs(path)}/{file_name(path)}'


def paths_with_filename(file_name: str, base_path=''):
    base_path = (os.path.expanduser(base_path))
    path = f'{base_path}/**/{file_name}.sql'
    files = glob.glob(path, recursive=True)
    return files
