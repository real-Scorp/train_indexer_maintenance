import os

def concatenate_code_files(directory='.', output_file='combined_code.txt', 
                            extensions=None, ignore_patterns=None):
    """
    Concatenate code files from a specified directory into a single file.
    
    :param directory: Directory to search for code files (default: current directory)
    :param output_file: Name of the output file to write concatenated code
    :param extensions: List of file extensions to include (e.g. ['.py', '.js'])
    :param ignore_patterns: List of patterns to ignore in filenames
    """
    # Default extensions if not specified
    if extensions is None:
        extensions = ['.py', '.js', '.cpp', '.c', '.java', '.html', '.css', '.txt', 
                      '.rb', '.php', '.go', '.rs', '.swift', '.kt', '.scala']
    
    # Default ignore patterns
    if ignore_patterns is None:
        ignore_patterns = ['venv', 'node_modules', '.git', '__pycache__', 
                           'build', 'dist', '.env']

    # Normalize directory path
    directory = os.path.abspath(directory)
    
    # Prepare output file path
    output_path = os.path.join(directory, output_file)
    
    # Collect all matching files
    code_files = []
    for root, dirs, files in os.walk(directory):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not any(ignore in d for ignore in ignore_patterns)]
        
        for file in files:
            # Check file extension
            if any(file.endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)
                
                # Ignore files in ignored directories
                if not any(ignore in full_path for ignore in ignore_patterns):
                    code_files.append(full_path)
    
    # Sort files for consistent output
    code_files.sort()
    
    # Write concatenated code
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for filepath in code_files:
            # Write separator with relative path
            relative_path = os.path.relpath(filepath, directory)
            outfile.write(f"\n{'='*80}\n")
            outfile.write(f"FILE: {relative_path}\n")
            outfile.write(f"{'='*80}\n")
            
            # Write file contents
            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')
            except Exception as e:
                outfile.write(f"\n[ERROR reading file: {e}]\n\n")
    
    print(f"Concatenated {len(code_files)} files into {output_file}")
    print(f"Output file location: {output_path}")

# Example usage
if __name__ == '__main__':
    # Basic usage
    concatenate_code_files()
    
    # Custom usage examples:
    # concatenate_code_files(directory='/path/to/your/project')
    # concatenate_code_files(extensions=['.py', '.js'])
    # concatenate_code_files(ignore_patterns=['test', 'docs'])