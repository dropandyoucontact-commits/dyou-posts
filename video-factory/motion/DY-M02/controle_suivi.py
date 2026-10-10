"""planche de contrôle du suivi : quadrilatère vert + écran recouvert en rouge"""
import cv2, json, numpy as np, pathlib, sys
P = pathlib.Path(__file__).resolve().parent
noms = ['baskets', 'textile', 'magasin-electronique', 'usine-electronique', 'surron']
pas = int(sys.argv[1]) if len(sys.argv) > 1 else 18
out = []
for nom in noms:
    d = json.loads((P / 'suivi' / f'{nom}.json').read_text()); cap = cv2.VideoCapture(str(P / f'media/rushes/{nom}.mp4')); fr = []
    while True:
        ok, im = cap.read()
        if not ok: break
        fr.append(im)
    row = []
    for i in range(6, len(fr), pas):
        im = fr[i].copy(); m = cv2.imread(str(P / f'suivi/{nom}/{i + 1:05d}.png'), 0)
        im[m > 0] = (0.4 * im[m > 0] + [0, 0, 150]).astype(np.uint8)
        cv2.polylines(im, [np.round(np.array(d['coins'][i])).astype(np.int32)], True, (0, 255, 0), 1)
        cv2.putText(im, f'{i / 24:.2f}', (5, 20), 0, 0.6, (0, 255, 255), 2)
        row.append(cv2.resize(im, (180, 320)))
    out.append(np.hstack(row))
w = max(r.shape[1] for r in out); out = [np.pad(r, ((0, 0), (0, w - r.shape[1]), (0, 0))) for r in out]
cv2.imwrite(sys.argv[2] if len(sys.argv) > 2 else 'suivi/controle.jpg', np.vstack(out))
