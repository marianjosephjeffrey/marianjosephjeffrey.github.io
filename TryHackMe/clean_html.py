import os

# folder containing your HTML files
folder_path = "/Users/marianjohn/Downloads/Website files/ExportBlock-bf81f63f-d697-4f0c-aa26-9370329cf505-Part-1/TryHackMe - Labs & Progress"

# string to remove
target = "2653eecded538004ba37d4ec5dac5de7"

for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.lower().endswith(".html"):
            file_path = os.path.join(root, filename)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # remove the target string
            new_content = content.replace(target, "")

            # write back only if changed
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Cleaned: {file_path}")

print("Done.")
