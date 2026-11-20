# Vídeo 01 — "Você está usando o celular errado?"

**Legenda (Reels / TikTok / Shorts):**

Você sabia que o calor pode acelerar o desgaste da bateria do celular? 🔋
E tem muita gente que deixa o aparelho em lugares quentes sem perceber.
Você costuma deixar o celular carregando durante a noite? 👀

#curiosidades #vocêsabia #tecnologia #celular #dicas #eununcasoube

## Notas de produção
- 1080x1920, 30 fps, 29,2 s (a fala em ritmo natural ficou mais longa que os ~25 s do roteiro; dá para encurtar ajustando `speed` em `scripts/build_audio.py`).
- Voz: Kokoro `pf_dora` (feminina, pt-BR), sintética e gerada offline, porque não havia chave do ElevenLabs. Troque por uma voz do ElevenLabs quando tiver a chave: gere o áudio, ponha em `proj/assets/` e rode `scripts/build_html.py` de novo com o novo `times.json`.
- Trilha e efeitos sintetizados no código (sem direitos autorais). Mix a -14 LUFS.
- Visual: padrão `motion-sem-cara-de-ia` (iPhone como protagonista, Nunito, 1 cor de destaque, fundos com luz, sem cartões). Não usei fotos reais (sem chave Pexels); o roteiro pede "pessoa segurando o celular", troque por foto/vídeo real se preferir.
- Texto sem afirmar que "carregar à noite estraga a bateria".
- Reproduzir: `python3 scripts/build_audio.py <modelo_kokoro> proj/assets` → `python3 scripts/build_html.py proj` → `cd proj && npx hyperframes render`.
