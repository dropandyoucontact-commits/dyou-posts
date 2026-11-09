#!/bin/zsh
# Clips Seedance 2.5 (API Higgsfield) depuis les images clés ChatGPT.
# usage : ./generer-clips.sh c1 c2 ...   (sans argument : tous ceux dont le mp4 manque)
set -u; setopt nullglob
cd "$(dirname "$0")"
source ~/.config/higgsfield/env.sh
STYLE="Realistic cinematic product commercial, 24 fps, shallow depth of field. The product stays perfectly rigid, sharp and identical to the image: same shape, same black dome lid, same transparent body with black VORIX print, same black base. No deformation, no morphing, no added text, no hands unless stated."
typeset -A IMG TXT
IMG[c1]=k1; TXT[c1]="The electric shaker bottle stands on a wet dark rock in high mountains. Slow smooth camera orbit around the product, about a quarter turn with a gentle push-in. Thin mist drifts across the rocks, a few water droplets fall and splash softly at the base, cold blue-grey dusk light, one white light beam behind the product."
IMG[c2]=k2; TXT[c2]="Macro shot. Inside the transparent cup, the chocolate protein shake spins in a tight vortex driven by the small steel whisk at the bottom; fine bubbles and streaks rotate, small droplets slide down the outside wall. Camera locked off with a very slow push-in. Mountain and mist stay softly blurred behind."
IMG[c3]=k3; TXT[c3]="The three parts of the shaker lie on the wet rock: dome lid, transparent cup with the steel whisk, black motor base. Slow lateral camera slide from left to right, a soft white light sweeps across the parts, a few water drops fall on them. Mist drifts behind."
IMG[c4]=k4; TXT[c4]="A man's hand pours clear water from a glass bottle into the open transparent cup, water level rises to about half, then a scoop of chocolate protein powder is tipped in from a small scoop. Camera locked off, slight push-in. Dark kitchen counter, cold moody light."
IMG[c5]=k5; TXT[c5]="A thumb presses the round button on the black base, a small blue LED lights up, and the liquid inside the transparent cup starts spinning into a vortex within one second. Camera locked off, slight push-in. Dark counter, cold moody light."
IMG[c6]=k6; TXT[c6]="Running tap water pours over the three shaker parts held under the faucet, water splashes and sheets off the transparent cup, droplets fly in slow natural motion. Camera locked off. Dark sink, cold moody light."
IMG[c7]=k7; TXT[c7]="Wide shot of the shaker standing small on a rock ridge in dark high mountains. Very slow push-in toward the product, mist flows through the valley, clouds drift, a single white light beam behind the product. Upper half of the frame stays dark and empty."
liste=("$@"); (( $#liste == 0 )) && for c in c1 c2 c3 c4 c5 c6 c7; do [[ -e media/videos/$c.mp4 ]] || liste+=$c; done
for c in $liste; do
  k=${IMG[$c]}; [[ -e media/images/$k.png ]] || { echo "manque media/images/$k.png"; continue; }
  echo "== $c ($k)"
  ~/bin/hf video bytedance/seedance-2.5/image-to-video --prompt "${TXT[$c]} $STYLE" \
    --photo media/images/$k.png --reference-field image_url \
    --set duration=8 --set resolution=720p --set generate_audio=false \
    --output-dir media/videos/$c 2>&1 | tee media/videos/$c.log
  fs=(media/videos/$c/*.mp4(Nom)); (( $#fs )) && cp "$fs[1]" media/videos/$c.mp4 && echo "→ media/videos/$c.mp4"
done
