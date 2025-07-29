def fill_file(file_path, size):
    with open(file_path, "w") as f:
        f.seek(size * 1024 * 1024)
        f.write("a")
