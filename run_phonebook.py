import logging

from FileReader import FileReader

DEFAULT_FILE_PATH = 'test_file.txt'
DEFAULT_SORT_ORDERING = 'Ascending'
DEFAULT_SORT_COLUMN = 'first_name'

if __name__ == '__main__':
    try:
        file_path = input(f"Input file path (default -> {DEFAULT_FILE_PATH})") or DEFAULT_FILE_PATH
        sort_ordering = input("Please choose an ordering to sort (type):"
                              f" “Ascending” or “Descending” "
                              f"(default -> {DEFAULT_SORT_ORDERING})-> ") or 'DEFAULT_SORT_ORDERING'
        sort_column = input(f"Please choose criteria (type) (default -> {DEFAULT_SORT_COLUMN})-> "
                            "“first_name”, “last_name” or “phone_number” -> ") or DEFAULT_SORT_COLUMN
        file_reader = FileReader(file_path)
        file_dataframe = file_reader.start_reading()
        if sort_ordering == 'Ascending':
            sort_ordering = True
        else:
            sort_ordering = False
        try:
            file_dataframe = file_dataframe.sort_values(by=[sort_column], ascending=sort_ordering)
            print(file_dataframe.to_markdown())
        except KeyError as exception:
            logging.error(f"Error during sorting with message {exception}")
    except Exception as exception:
        logging.error(f"Happened error with message {exception}")
