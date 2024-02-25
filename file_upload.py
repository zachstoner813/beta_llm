def upload_files(client, paths):
    file_ids = []
    for path in paths:
        with open(path, "rb") as file:
            uploaded_file = client.files.create(
                file=file,
                purpose="assistants"
            )
            file_ids.append(uploaded_file.id)
    return file_ids
