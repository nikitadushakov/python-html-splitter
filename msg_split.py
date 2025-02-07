import click
import os
import python_html_splitter



@click.command()
@click.option('--max_len', help='Максимальная длина одного фрагмента')
@click.argument('file_path')
def main(max_len, file_path):
    num_columns = os.get_terminal_size().columns
    with open(file_path, 'r') as rows_stream:
        fragments = python_html_splitter.split_html(
            rows_stream, message_size=int(max_len)
        )
        for fragment_no, fragment in enumerate(fragments, start=1):
            print(f'\nFragment number {fragment_no}: '.ljust(num_columns, '='))
            print(fragment)


if __name__ == "__main__":
    main()
