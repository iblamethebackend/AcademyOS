from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
excluded={'node_modules','.expo','__pycache__','native-export','.git'}
files=[p for p in root.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(root).parts) and p.suffix!='.zip']
target=root/'AcademyOS-Design-and-Expo-Pack.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,Path('AcademyOS')/p.relative_to(root))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(f'Verified archive: {len(files)} files, {target.stat().st_size:,} bytes')
