from pathlib import Path
import zipfile
root=Path('deliverables')
files=[root/'CampusOS-School-SaaS-Blueprint.pdf',root/'CampusOS-Requirements.csv',root/'CampusOS-Screen-Gallery.jpg',root/'README.md',root/'verification-report.json',root/'page-map.json']
files += sorted((root/'screens').glob('*.png'))
files += [root/'source'/n for n in ['build_blueprint.py','requirements.py','requirements.txt','verify_and_export.py','preview.py','layout-check.json']]
with zipfile.ZipFile(root/'CampusOS-Complete-Blueprint-Pack.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(f,Path('CampusOS-Blueprint')/f.relative_to(root))
with zipfile.ZipFile(root/'CampusOS-Complete-Blueprint-Pack.zip') as z:
    assert z.testzip() is None
print('Pack verified:',len(files),'files')
for f in root.glob('*'):
    if f.is_file():print(f.name, f.stat().st_size)
