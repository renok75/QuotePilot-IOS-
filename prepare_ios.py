#!/usr/bin/env python3
"""Prepare the generated Capacitor iOS project for QuotePilot."""
from pathlib import Path
import json, shutil, plistlib
root=Path(__file__).resolve().parent.parent
app=root/'ios/App/App'
if not app.exists():raise SystemExit('Run npx cap add ios before this script.')
icon_dir=app/'Assets.xcassets/AppIcon.appiconset'
icon_dir.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'resources/AppIcon-1024.png',icon_dir/'AppIcon-1024.png')
(icon_dir/'Contents.json').write_text(json.dumps({'images':[{'filename':'AppIcon-1024.png','idiom':'universal','platform':'ios','size':'1024x1024'}],'info':{'author':'xcode','version':1}},indent=2)+'\n')
plist=app/'Info.plist'
with plist.open('rb') as f: data=plistlib.load(f)
data['CFBundleDisplayName']='QuotePilot'
data['ITSAppUsesNonExemptEncryption']=False
with plist.open('wb') as f:plistlib.dump(data,f)
print('QuotePilot iOS icon and Info.plist prepared.')
