import os

def list_files(root_dir):
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            print(file_path)
            files.append(file_path)
    return files

def delete_zone_identifier_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('Zone.Identifier'):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    print("Listing all files:")
    list_files(project_root)
    answer = input("\nDo you want to delete files ending with 'Zone.Identifier'? (yes/no): ").strip().lower()
    if answer == "yes":
        print("\nDeleting files ending with 'Zone.Identifier':")
        delete_zone_identifier_files(project_root)
    else:
        print("\nNo files were deleted.")