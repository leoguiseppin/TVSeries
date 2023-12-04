import os
import re
import json
import chardet

# Fonction pour extraire le texte à partir d'un fichier SRT
def extract_text_from_srt(srt_file):
    encodings_to_try = ['utf-8', 'latin-1']

    for encoding in encodings_to_try:
        try:
            with open(srt_file, 'r', encoding=encoding) as file:
                lines = file.readlines()

            subtitles = []
            current_subtitle = None

            for line in lines:
                line = line.strip()
                if re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):
                    if current_subtitle:
                        subtitles.append(current_subtitle)
                    current_subtitle = {'text': ''}
                else:
                    if current_subtitle:
                        current_subtitle['text'] += ' ' + line

            if current_subtitle:
                subtitles.append(current_subtitle)

            return subtitles

        except UnicodeDecodeError:
            continue

    return []

# Fonction pour extraire le texte à partir d'un fichier SUB (format 1)
def extract_text_from_sub(sub_file):
    with open(sub_file, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    subtitles = []
    current_subtitle = None
    format1 = False

    for line in lines:
        line = line.strip()
        if line.startswith('{') and line.endswith('}'):
            if not current_subtitle:
                current_subtitle = {'text': ''}
            else:
                subtitles.append(current_subtitle)
                current_subtitle = {'text': ''}
            current_subtitle['text'] += line.split('}', 1)[1].strip()
        elif line.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) and ' --> ' in line:
            if not current_subtitle:
                current_subtitle = {'text': ''}
            else:
                subtitles.append(current_subtitle)
                current_subtitle = {'text': ''}
            current_subtitle['text'] += line
            format1 = True
        elif current_subtitle:
            current_subtitle['text'] += ' ' + line

    if current_subtitle:
        subtitles.append(current_subtitle)

    if format1:
        for subtitle in subtitles:
            subtitle['text'] = re.sub(r'^\d+\s*', '', subtitle['text'].strip())

    return subtitles

# Fonction pour extraire le texte à partir d'un fichier VO
def extract_text_from_vo(vo_file):
    with open(vo_file, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    subtitles = []
    current_subtitle = None

    with open(vo_file, 'r', encoding=encoding) as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if re.match(r'^\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):
            continue
        elif not line:
            if current_subtitle:
                subtitles.append(current_subtitle)
                current_subtitle = None
        else:
            if not current_subtitle:
                current_subtitle = {'text': line}
            else:
                current_subtitle['text'] += ' ' + line

    return subtitles

# Fonction pour traiter un répertoire de sous-titres
def process_directory(root_directory, output_base_directory):
    for root, dirs, files in os.walk(root_directory):
        subtitles = []
        series_title = os.path.basename(root)
        subtitles.append({'series_title': series_title})

        for filename in files:
            if filename.endswith('.srt'):
                srt_file = os.path.join(root, filename)
                subtitles.extend(extract_text_from_srt(srt_file))

                series_title = os.path.basename(root)
                output_series_directory = os.path.join(output_base_directory, series_title)
                os.makedirs(output_series_directory, exist_ok=True)
                output_json_file = os.path.join(output_series_directory, 'subtitles.json')

                with open(output_json_file, 'w', encoding='utf-8') as json_file:
                    json.dump(subtitles, json_file, ensure_ascii=False, indent=4)

                os.remove(srt_file)
                print(f"Fichier SRT '{filename}' de la série TV '{series_title}' traité et sauvegardé dans '{output_json_file}'.")

def main():
    subtitles_root_directory = 'C:/Users/leogu/Desktop/SAE/sous-titres'
    output_base_directory = 'C:/Users/leogu/Desktop/SAE/output'

    process_directory(subtitles_root_directory, output_base_directory)

if __name__ == "__main__":
    main()
