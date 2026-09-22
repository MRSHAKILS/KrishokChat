import sys
try:
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(r'd:\KrishokChat Advisory System\paper\EACL Final\paper\latex\main.pdf')
    num_pages = len(pdf)
    print(f'Total Pages: {num_pages}')
    
    # Check page 6 and 7 text
    page6_text = pdf[5].get_textpage().get_text_range()
    page7_text = pdf[6].get_textpage().get_text_range()
    
    if '6 Conclusion' in page6_text or 'Conclusion' in page6_text:
        print('Section 6 found on page 6.')
    else:
        print('Section 6 NOT found on page 6.')
        
    if '7 Ethics Statement' in page7_text or 'References' in page7_text:
        print('Section 7 / References found on page 7.')
    else:
        print('Section 7 / References NOT found on page 7.')
except Exception as e:
    print('Failed to run pypdfium2 check:', e)
