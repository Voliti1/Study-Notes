import os
import re

posts = [
    '2026-05-16-python_notes_06_logistic_regression.html',
    '2026-05-17-python_notes_07_knn.html',
    '2026-05-18-python_notes_08_kfold.html',
    '2026-05-19-python_notes_09_gridsearch.html',
    '2026-05-20-python_notes_10_randomforest.html',
    '2026-05-21-python_notes_11_kmeans.html',
    '2026-05-22-python_notes_12_dbscan.html'
]

site_dir = './_site'
errors = 0

for post in posts:
    path = os.path.join(site_dir, post)
    exists = os.path.exists(path)
    print(f'Checking {post}: Exists = {exists}')
    
    if not exists:
        errors += 1
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for incorrect Study-Notes2 path
    if 'Study-Notes2' in content:
        print(f'  [WARNING] Found "Study-Notes2" in {post}!')
        errors += 1
        
    # Check MathJax loading
    if 'MathJax.js' not in content:
        print(f'  [WARNING] MathJax script missing in {post}!')
        errors += 1
        
    # Check image assets matching for specific files
    if 'knn' in post:
        if 'assets/images/knn_scatter.png' not in content or 'assets/images/knn_k_accuracy.png' not in content:
            print(f'  [WARNING] Expected KNN images missing in {post}!')
            errors += 1
    elif 'randomforest' in post:
        if 'assets/images/random_forest_feature_importance.png' not in content:
            print(f'  [WARNING] Expected Random Forest image missing in {post}!')
            errors += 1
    elif 'kmeans' in post:
        if 'assets/images/kmeans_before.png' not in content or 'assets/images/kmeans_after.png' not in content or 'assets/images/kmeans_elbow.png' not in content:
            print(f'  [WARNING] Expected K-Means images missing in {post}!')
            errors += 1
    elif 'dbscan' in post:
        images = [
            'assets/images/dbscan_moons_kmeans.png',
            'assets/images/dbscan_moons_dbscan.png',
            'assets/images/dbscan_circles_kmeans.png',
            'assets/images/dbscan_circles_dbscan.png'
        ]
        for img in images:
            if img not in content:
                print(f'  [WARNING] Expected DBSCAN image {img} missing in {post}!')
                errors += 1

print(f'\nVerification completed. Total warnings/errors: {errors}')
