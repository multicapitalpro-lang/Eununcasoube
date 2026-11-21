#!/bin/bash
cd /home/user/Eununcasoube/videos
declare -A N=([06-chuva]="video06-cheiro-de-chuva" [07-polvo]="video07-polvo-tres-coracoes" [08-eiffel]="video08-torre-eiffel-muda-de-tamanho" [09-mel]="video09-mel-nao-estraga" [10-banana]="video10-banana-e-uma-baga" [11-ceu]="video11-por-que-o-ceu-e-azul")
for v in 06-chuva 07-polvo 08-eiffel 09-mel 10-banana 11-ceu; do (cd $v/proj && npx --yes hyperframes@0.9.72 render -o ../../entrega/${N[$v]}.mp4 2>&1 | grep -E "MB|Error"); done
echo ALLDONE
