#!/bin/bash
cd /home/user/Eununcasoube/videos
declare -A N=([02-raio]="video02-raio-mais-quente-que-o-sol" [03-ossos]="video03-voce-nasceu-com-mais-ossos" [04-preco]="video04-por-que-tudo-custa-9-99" [05-apollo]="video05-celular-vs-apollo")
for v in 02-raio 03-ossos 04-preco 05-apollo; do (cd $v/proj && npx --yes hyperframes@0.9.72 render -o ../../entrega/${N[$v]}.mp4 2>&1 | grep -E "MB|Error" ); done
echo ALLDONE
