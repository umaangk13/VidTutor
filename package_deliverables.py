import os
import zipfile

def package_project(output_filename="VidTutor_Deliverables.zip"):
    files_to_include = [
        "app.py",
        "sarvam_utils.py",
        "youtube_utils.py",
        "requirements.txt",
        "README.md",
        "package_deliverables.py"
    ]
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file}")
            else:
                print(f"Warning: {file} not found.")
                
    print(f"Packaging complete! Created {output_filename}")

if __name__ == "__main__":
    package_project()
