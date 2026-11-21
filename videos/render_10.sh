#!/bin/bash
cd /home/user/Eununcasoube/videos
declare -A N=([12-sol]="video12-luz-do-sol-8-minutos" [13-cleopatra]="video13-cleopatra-e-a-lua" [14-venus]="video14-venus-dia-maior-que-ano" [15-webcam]="video15-primeira-webcam-cafeteira" [16-cerebro]="video16-cerebro-20-por-cento" [17-coala]="video17-coala-digitais" [18-banana-radioativa]="video18-banana-radioativa" [19-qrcode]="video19-tres-quadrados-qr-code" [20-tardigrado]="video20-tardigrado-no-espaco" [21-wombat]="video21-wombat-coco-cubico")
for v in 12-sol 13-cleopatra 14-venus 15-webcam 16-cerebro 17-coala 18-banana-radioativa 19-qrcode 20-tardigrado 21-wombat; do (cd $v/proj && npx --yes hyperframes@0.9.72 render -o ../../entrega/${N[$v]}.mp4 2>&1 | grep -E "MB|Error"); done
echo ALLDONE
