import pypdf

reader = pypdf.PdfReader('paper/EACL Final/paper/latex/main.pdf')
print('Total pages:', len(reader.pages))
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    headers_found = []
    for header in ['1 Introduction', '5 Evaluation', '6 Limitations', 'Conclusion', 'Ethics and Broader Impact', 'References', 'A Extended Architecture']:
        if header.lower() in text.lower():
            headers_found.append(header)
    if headers_found:
        print(f'Page {i+1}: contains {headers_found}')
