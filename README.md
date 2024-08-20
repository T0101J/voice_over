# Vídeo Processing Script

Este projeto é um script Python que automatiza o processamento de um vídeo, realizando operações como corte, extração de áudio, transcrição, tradução de texto, síntese de voz e substituição do áudio original do vídeo por uma versão traduzida.

## Funcionalidades

- **Corte de Vídeo**: Corta os primeiros 5 minutos de um vídeo.
- **Extração de Áudio**: Extrai o áudio do vídeo cortado e o salva como um arquivo `.wav`.
- **Transcrição de Áudio**: Transcreve o áudio extraído usando o modelo Whisper.
- **Tradução de Texto**: Traduz o texto transcrito para o inglês usando a API GPT-3.5 da OpenAI.
- **Síntese de Voz**: Converte o texto traduzido em áudio usando a API de Text-to-Speech da OpenAI.
- **Substituição de Áudio**: Substitui o áudio original do vídeo pelo novo áudio em inglês.

## Dependências

- Python 3.7+
- Bibliotecas Python:
  - `moviepy`
  - `pydub`
  - `whisper`
  - `openai`

## Como Usar

1. **Instale as dependências**:
   ```bash
   pip install moviepy pydub openai whisper
Configure sua chave de API da OpenAI:

Defina a variável de ambiente OPENAI_API_KEY com sua chave de API da OpenAI:
No Windows:
bash
Copiar código
setx OPENAI_API_KEY "sua-chave-de-api-aqui"
No Linux ou macOS:
bash
Copiar código
export OPENAI_API_KEY="sua-chave-de-api-aqui"
Execute o script:

bash
Copiar código
python process_video.py
Resultado:

O vídeo processado será salvo como video_with_english_audio.mp4.
Limpeza de Arquivos Temporários
O script remove automaticamente os arquivos temporários após a execução para garantir que não haja consumo desnecessário de espaço.

Observações
O áudio gerado será ajustado em velocidade para garantir que se alinhe corretamente com o tempo do vídeo original.
