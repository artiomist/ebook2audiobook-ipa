import os
import re
import sys
import zipfile
import shutil
from bs4 import BeautifulSoup
from omogre import Transcriptor
from num2words import num2words
from ebooklib import epub
from decimal import Decimal, InvalidOperation


def extract_russian_text_nodes(soup):
    """Return all NavigableString nodes containing Russian text."""
    return [text for text in soup.descendants if isinstance(text, str) and re.search(r'[А-Яа-я]', text)]

def replace_russian_with_transcription(soup, original_texts, transcribed_texts):
    mapping = dict(zip(original_texts, transcribed_texts))
    for text_node in soup.descendants:
        if isinstance(text_node, str):
            text = text_node
            if text in mapping:
                text_node.replace_with(mapping[text])
    return soup



def normalize_numbers(text):
    number_pattern = r'\b\d+[\d,]*(\.\d+)?\b'

    def replace_match(match):
        number = match.group(0)
        try:
            if ',' in number:
                number = number.replace(',', '.')
            if '.' in number:
                integer, decimal = number.split('.')
                return f"{num2words(integer, lang='ru')} точка {num2words(decimal, lang='ru')}"
            return num2words(number, lang='ru')
        except InvalidOperation:
            return number

    return re.sub(number_pattern, replace_match, text)


def transcribe_chapter(html_content):
    # Extract XML declaration and opening <html> tag
    xml_decl_match = re.match(r"(<\?xml[^>]+\?>)", html_content)
    html_tag_match = re.search(r"(<html[^>]*>)", html_content)

    xml_decl = xml_decl_match.group(1) if xml_decl_match else ''
    html_tag = html_tag_match.group(1) if html_tag_match else '<html>'

    # Strip the XML declaration and opening <html> tag before parsing
    stripped_content = html_content
    if xml_decl:
        stripped_content = stripped_content.replace(xml_decl, '')
    if html_tag:
        stripped_content = stripped_content.replace(html_tag, '<html>', 1)

    # Process with BeautifulSoup
    soup = BeautifulSoup(normalize_numbers(stripped_content), 'html.parser')
    texts = extract_russian_text_nodes(soup)
    transcriptor = Transcriptor(data_path='omogre_data', punct=None)
    transcribed = transcriptor(texts)
    transcribed_body = str(replace_russian_with_transcription(soup, texts, transcribed))

    # Replace the placeholder <html> with the original
    transcribed_body = transcribed_body.replace('<html>', html_tag, 1)

    # Reattach XML declaration at the top
    if xml_decl:
        transcribed_body = f"{xml_decl}\n{transcribed_body}"

    return transcribed_body



def process_epub(input_epub_path):
    print(f"📖 Opening EPUB: {input_epub_path}")
    
    # Read the EPUB file
    book = epub.read_epub(input_epub_path)

    # Unzip the EPUB file
    output_folder = input_epub_path.replace('.epub', '_transcribed')
    with zipfile.ZipFile(input_epub_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
        
    print(f"📂 Output folder created: {output_folder}")

    # Process only the index_split_ files and copy other resources as-is
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, output_folder)
            output_file_path = os.path.join(output_folder, relative_file_path)

            if file.lower().endswith('.xhtml'):
                # Process only the index_split_ files
                if file.lower().startswith('index_split_'):
                    print(f"📄 Transcribing: {file}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    transcribed_content = transcribe_chapter(content)
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        f.write(transcribed_content)
                else:
                    # Copy other .xhtml files as-is
                    print(f"📁 Skipping resource: {file}")
            else:
                # Copy non-XHTML resources (like images and stylesheets) as-is
                print(f"📁 Skipping resource: {file}")

    # After processing, re-compress the folder into a new EPUB
    new_epub_path = input_epub_path.replace('.epub', '_processed.epub')
    shutil.make_archive(new_epub_path.replace('.epub', ''), 'zip', output_folder)
    os.rename(new_epub_path.replace('.epub', '.zip'), new_epub_path)
    print(f"✅ Done! New EPUB created: {new_epub_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Please provide the input EPUB file path.")
        print("Usage: python transcribe_file_6_book.py path_to_input.epub")
    else:
        process_epub(sys.argv[1])
