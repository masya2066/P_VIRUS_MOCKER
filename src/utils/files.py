from fastapi import UploadFile
import io


async def check_text_in_file(file: any, text: str) -> bool:
    try:
        file_stream = io.BytesIO(file)

        # Attempt to decode file content as UTF-8 text
        try:
            file_content_str = file_stream.getvalue().decode("utf-8")
            print("File content decoded successfully.")
        except UnicodeDecodeError:
            # Handle non-UTF-8 content or binary files
            print("File is binary or not encoded in UTF-8.")
            return False

        # Check if the text is present in the decoded file content
        found = text in file_content_str
        print(f"Text found: {found}")
        return found

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
