import os
import re

f = '_site/2026-05-15-python_notes_05_regression.html'

exists = os.path.exists(f)
print(f'File {f} exists:', exists)

if exists:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    print('Checking content of regression post:')

    # Check for correct /Study-Notes baseurl in asset links
    image_refs = re.findall(r'src="[^"]*assets/images/linear_regression[^"]*"', content)
    print(f'  [INFO] Found images: {image_refs}')
    if len(image_refs) == 2: # linear_regression_scatter.png and linear_regression_fit.png
        print('  [OK] Linear regression images found.')
    else:
        print('  [WARNING] Expected linear regression images, found:', len(image_refs))

    poly_image_ref = re.findall(r'src="[^"]*assets/images/polynomial_regression_fit[^"]*"', content)
    print(f'  [INFO] Found polynomial image: {poly_image_ref}')
    if poly_image_ref:
        print('  [OK] Polynomial image found.')
    else:
        print('  [WARNING] Polynomial image missing.')

    # Check for MathJax script
    mathjax_found = 'MathJax.js' in content
    print('  MathJax script loaded:', mathjax_found)

    # Check for LaTeX content
    latex_formulas = re.findall(r'\$\$[^\$]+\$\$|\$[^\$]+\$', content)
    print(f'  [INFO] Found raw or rendered LaTeX-like strings: {len(latex_formulas)}')

    # Check for sidebar inclusion
    python_category_in_sidebar = 'data-path="/Study-Notes/python/"' in content
    print('  Python category in sidebar:', python_category_in_sidebar)
    
    regression_in_sidebar = '2026-05-15-python_notes_05_regression.html' in content
    print('  Regression post in sidebar:', regression_in_sidebar)
else:
    print('Error: Output HTML does not exist.')
