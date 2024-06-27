import os
import io

class DirWalker:
    def process_directory(
        self,
        dir_path: str,
        summary_file: io.TextIOWrapper,
        prefix: str = '',
    ) -> None:
        entries = os.listdir(dir_path)

        entries = [
            e for e in entries if (
                e != '.venv'
                and e != '__pycache__'
                and e != '.ipython'
                and e != '.profile'
                and e != '.bash_logout'
                and e != '.bashrc'
                and e != '.config'
                and e != '.cache'
                and e != '.local'
            )
        ]

        hidden_dirs = [
            d for d in entries
            if os.path.isdir(os.path.join(dir_path, d))
            and d.startswith('.')
        ]
        regular_dirs = [
            d for d in entries
            if os.path.isdir(os.path.join(dir_path, d))
            and not d.startswith('.')
        ]
        files = [
            f for f in entries
            if os.path.isfile(os.path.join(dir_path, f))
        ]

        hidden_dirs.sort()
        regular_dirs.sort()
        files.sort()

        sorted_entries = hidden_dirs + regular_dirs + files
        for i, entry in enumerate(sorted_entries):
            path = os.path.join(dir_path, entry)
            is_last = (i == len(sorted_entries) - 1)

            if os.path.isdir(path):
                self.process_subdirectory(
                    path,
                    entry,
                    prefix,
                    is_last,
                    summary_file,
                )
            else:
                self.write_file_entry(
                    entry,
                    is_last,
                    prefix,
                    summary_file,
                    dir_path
                )

    def process_subdirectory(
        self,
        path: str,
        entry: str,
        prefix: str,
        is_last: bool,
        summary_file: io.TextIOWrapper,
    ) -> None:
        connector = '├──' if not is_last else '└──'
        new_prefix = '│   ' if not is_last else '    '
        
        summary_file.write(f'{prefix}{connector} {entry}\n')
        self.process_directory(path, summary_file, prefix=(prefix + new_prefix))

    def write_file_entry(
        self,
        file_name: str,
        is_last: bool,
        prefix: str,
        summary_file: io.TextIOWrapper,
        dir_path: str
    ) -> None:
        connector = '├──' if not is_last else '└──'
        summary_file.write(f'{prefix}{connector} {file_name}\n')
        
        try:
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                for i, line in enumerate(file):
                    if i < 100:
                        summary_file.write(f'{prefix}    {line}')
                    else:
                        break
                summary_file.write(f'{prefix}    ...\n')  # Indicate more content is available
        except Exception as e:
            summary_file.write(f'{prefix}    [Error reading file: {e}]\n')

# Initialize DirWalker and write summary to a file
dir_walker = DirWalker()
summary_file_path = 'summary.txt'  # Updated path to write in accessible directory
with open(summary_file_path, 'w') as summary_file:
    summary_file.write('Project Directory Structure:\n')
    dir_walker.process_directory(os.getcwd(), summary_file)

# Read and print the summary to verify the output
with open(summary_file_path, 'r') as summary_file:
    summary_content = summary_file.read()

# Output a portion of the summary to verify correctness
print(summary_content[:2000])  # Print first 2000 characters to check the update without overloading the output