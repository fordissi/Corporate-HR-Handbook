import os, sys
try:
    import PyPDF2
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyPDF2'])
    import PyPDF2

pdf_dir = r'e:\Antigravity_HOME_PC\HR\Employee Handbook'
out_dir = r'e:\Antigravity_HOME_PC\HR\Employee Handbook\pdf_texts'
os.makedirs(out_dir, exist_ok=True)

for file in os.listdir(pdf_dir):
    if file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_dir, file)
        out_path = os.path.join(out_dir, file + '.txt')
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'Extracted {file}')
        except Exception as e:
            print(f'Failed to extract {file}: {e}')
print('Done!')
