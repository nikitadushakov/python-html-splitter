import click
import python_html_splitter


@click.command()
@click.option('--max_len', help='Максимальная длина одного фрагмента')
@click.argument('file_path')
def main(max_len, file_path):
    with open(file_path, 'r') as f:
        fragments = python_html_splitter.split_html(
            f, message_size=int(max_len))
        for fragment in fragments:
            print(fragment)


if __name__ == "__main__":
    main()
