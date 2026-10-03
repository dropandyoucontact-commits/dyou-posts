import json,pathlib,shutil

root=pathlib.Path(__file__).resolve().parent
out=root.parent
agency=json.loads((out/'dyou-video-scripts/scripts.json').read_text())
china=json.loads((out/'chinabook-video-scripts/scripts.json').read_text())
visual={v['id']:v for v in json.loads((out/'chinabook-video-scripts/visual-packs.json').read_text())}
all_scripts=agency+china
assert len(all_scripts)==50 and len(visual)==50
manifest=[]
for s in all_scripts:
 id=s['id'];d=root/'videos'/id
 for sub in ('images','captures','audio','video'): (d/sub).mkdir(parents=True,exist_ok=True)
 (d/'script.txt').write_text(s['script']+'\n')
 v=visual[id]
 brief={'id':id,'brand':'ChinaBook' if id.startswith('CB-') else 'DYOU Agency','profession':s.get('metier','Revendeurs / sourcing Chine'),'angle':s['angle'],'format':s.get('duree','moyen'),'voice_text':s['script'],'audio_filename':f'audio/{id}.mp3','final_video_filename':f'video/{id}.mp4','images':[{'filename':f'images/{n:02}.webp','prompt':p,'status':'pending'} for n,p in enumerate(v['prompts'],1)],'real_asset_requirement':v['real'],'motion_direction':v['motion'],'real_asset_status':'pending'}
 (d/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n')
 (d/'captures'/'A-LIRE.txt').write_text(v['real']+'\n')
 manifest.append({'id':id,'brand':brief['brand'],'profession':brief['profession'],'angle':s['angle'],'script':f'videos/{id}/script.txt','brief':f'videos/{id}/brief.json','images':[f'videos/{id}/images/{n:02}.webp' for n in (1,2,3)],'real_asset_requirement':v['real'],'audio':f'videos/{id}/audio/{id}.mp3','video':f'videos/{id}/video/{id}.mp4'})
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
shutil.copy2(out.parent/'upload/copy_93C19386-5147-4462-BDCE-A2F7E189FA0F.mp4',root/'videos/RES-01/captures/POLYRA-navigation-originale.mp4')
shutil.copy2(out.parent/'upload/IMG_5197(1).png',root/'brand-DYOU-original.png')
(root/'README.md').write_text('''# Bibliothèque de production vidéo\n\nUn dossier par ID : `script.txt` est exactement la voix off ; `brief.json` relie l'angle, les trois images, la capture réelle attendue, l'audio et la vidéo finale. `manifest.json` indexe les 50 dossiers.\n\n`images/01.webp` à `03.webp` sont les photos générées. Les captures, conversations, prix et logos réels vont dans `captures/`, jamais dans une fausse image générée. La navigation POLYRA fournie est déjà rangée dans RES-01. Le logo DYOU d'origine est à la racine.\n\nLes audio doivent être `audio/ID.mp3` et les vidéos `video/ID.mp4`. Montage 9:16, alternance de fonds noir/violet et de photos, typographie forte, sons d'apparition sans musique. La durée suit exactement le MP3.\n\nPour ChinaBook, vérifier les prix, le transport et les produits avant publication. Garder les captures WeChat autorisées et masquer les coordonnées privées dans les visuels publics.\n''')
print('Prepared',len(manifest),'videos')
