import argparse
import json
import datetime


def get_main_contents():
    with open('structure.json') as f:
        d = json.load(f)
        contents_main = d['contents']
        return contents_main


def get_level1_dirs(contents):
    dirs_lv_1 = []
    for content in contents:
        if 'contents' in content:
            dirs_lv_1.append(content['name'])
    return dirs_lv_1


def get_ls_l_content(contents, args, dir_main):
    """
    :param contents: The complete json
    :param args: -l -t -r --filter==<choice> path
    :param dir_main: Contains the directory names in the home directory
    :return: data according to the conditions in the arguments

    """
    data = []
    sub_folders_data = [content for content in contents if content['name'] in dir_main]
    for content in contents:
        if content['name'] != '.gitignore':
            dt_time = datetime.datetime.fromtimestamp(content.get('time_modified')).strftime('%Y-%b-%d %H:%M')
            month = dt_time[0:11].split('-')[1]
            day = dt_time[0:11].split('-')[2]
            hr_min = dt_time.split(' ')[1]
            data.append([content['permissions'], str(content['size']), month, day, hr_min, content['name'],
                         content['time_modified']])

    # Subtask 7: Handle Paths (5 points)
    if args.path and args.path != '.':
        dir_name = args.path.split('/')[0]
        file_name = args.path.split('/')[1] if len(args.path.split('/')) == 2 else None
        if dir_name in dir_main and file_name is not None:
            for dt in sub_folders_data:
                if dt['name'] == dir_name:
                    for content in dt['contents']:
                        if file_name == content['name']:
                            data = []
                            dt_time = datetime.datetime.fromtimestamp(content.get('time_modified')).strftime(
                                '%Y-%b-%d %H:%M')
                            month = dt_time[0:11].split('-')[1]
                            day = dt_time[0:11].split('-')[2]
                            hr_min = dt_time.split(' ')[1]
                            data.append(
                                [content['permissions'], str(content['size']), month, day, hr_min, "./" + dir_name +
                                 '/' + file_name, content['time_modified']])
                            return [dt[0:-1] for dt in data]
            return f"error: cannot access '{'./' + dir_name + '/' + file_name}': No such file or directory"
        elif dir_name in dir_main and file_name is None:
            for dt in sub_folders_data:
                data = []
                if dt['name'] == dir_name:
                    for content in dt['contents']:
                        dt_time = datetime.datetime.fromtimestamp(content.get('time_modified')).strftime(
                            '%Y-%b-%d %H:%M')
                        month = dt_time[0:11].split('-')[1]
                        day = dt_time[0:11].split('-')[2]
                        hr_min = dt_time.split(' ')[1]
                        data.append(
                            [content['permissions'], str(content['size']), month, day, hr_min, content['name'],
                             content['time_modified']])
                    return [dt[0:-1] for dt in data][::-1]
        return f"error: cannot access '{dir_name}': No such file or directory"

    # Subtask 6: ls -l -r -t --filter=<option>
    if args.filter:
        filter_data = []
        if args.filter == 'dir':
            for dt in data:
                if dt[5] in dir_main:
                    filter_data.append(dt)
        elif args.filter == 'file':
            for dt in data:
                if dt[5] not in dir_main:
                    filter_data.append(dt)
        else:
            return f"error: {args.filter} is not a valid filter criteria. Available filters are 'dir' and 'file'"
        data = filter_data

    # Subtask 5: ls -l -r -t
    if args.t:
        data = sorted(data, key=lambda x: x[6])

    # Subtask 4: ls -l -r
    if args.r:
        data = data[::-1]

    return [dt[0:-1] for dt in data]


class Commandline:
    def __init__(self):
        self.contents_main = get_main_contents()
        self.dir_main = get_level1_dirs(self.contents_main)

    def ls_cmd(self, args):
        for content in self.contents_main:
            # Subtask 2: ls -A
            if args.A:
                print(content['name'], end=" ")

            # Subtask 1: ls
            elif content['name'][0] != '.':
                print(content['name'], end=" ")

    def ls_l_cmd(self, args):
        contents = get_ls_l_content(self.contents_main, args, self.dir_main)
        if isinstance(contents, list):
            for content in contents:
                print(" ".join(content))
        else:
            print(contents)


def main():
    parser = argparse.ArgumentParser(description='List directory contents in ls style.')
    parser.add_argument('-A', action='store_true', help='List all entries including those starting with .')
    parser.add_argument('-l', action='store_true', help='Use a long listing format. Prints more information')
    parser.add_argument('-r', action='store_true', help='Reverse the order of the output')
    parser.add_argument('-t', action='store_true', help='Sort by modification time, newest first')
    parser.add_argument('--filter', help='Filter output by file or directory. choices=["file", "dir"]')
    parser.add_argument('path', nargs='?', default='.',
                        help='Directory path or file to list (default: current directory)')
    args = parser.parse_args()

    cmd_line = Commandline()
    if (args and not args.l) or args.A:
        cmd_line.ls_cmd(args)
    elif args.l:
        cmd_line.ls_l_cmd(args)


if __name__ == "__main__":
    main()
