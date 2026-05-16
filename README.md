<div align="center">

# 🛣️ Road Surface AI

### Sistema de Classificação de Superfícies de Vias usando Deep Learning

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

**Desenvolvido por:**  
João Henrique dos Santos Silva & Carlos Vinicius Felix da Silva  
**CIn - UFPE | Inteligência Artificial | 2026**

[Demo](#-demo) • [Características](#-características) • [Instalação](#-instalação) • [API](#-api-endpoints) • [Arquitetura](#-arquitetura)

</div>

---

## 📊 Resultados do Modelo

<div align="center">

| Métrica | Valor |
|---------|-------|
| **Modelo** | EfficientNetV2-S (21M parâmetros) |
| **F1-Macro** | **83.87%** |
| **Acurácia** | **91.48%** |
| **Classes** | Asfalto, Blocos Belgas, Off-road |
| **Inferência** | ~45ms (GPU) / ~200ms (CPU) |

</div>

### Desempenho por Classe

- **Asfalto:** Precisão 98% | Recall 94%
- **Off-road:** Precisão 91% | Recall 100%
- **Blocos Belgas:** Precisão 75% | Recall 59%

---

## ✨ Características

### 🎯 Backend (FastAPI)
- ✅ API REST moderna e eficiente
- ✅ Upload de imagens via multipart/form-data
- ✅ Inferência em tempo real (~45ms)
- ✅ Preprocessamento otimizado (crop + normalização)
- ✅ Health check endpoint
- ✅ CORS habilitado
- ✅ Suporte GPU/CPU automático

### 🎨 Frontend (React/Next.js)
- ✅ Interface moderna e profissional
- ✅ Upload com drag & drop
- ✅ Preview de imagens em tempo real
- ✅ Gráficos interativos (Recharts)
- ✅ Health check automático da API
- ✅ Design System completo
- ✅ TypeScript para type safety
- ✅ Acessibilidade (WCAG AA)
- ✅ Totalmente responsivo
- ✅ Animações suaves e feedback visual

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                       │
│  http://localhost:3000                                      │
│  - React 18 + TypeScript                                    │
│  - Tailwind CSS + Design System                             │
│  - Upload drag & drop + Preview                             │
│  - Gráficos interativos (Recharts)                          │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP POST /predict
                     │ (multipart/form-data)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  http://localhost:8000                                      │
│  - Python 3.11 + FastAPI                                    │
│  - PyTorch 2.0+ (CUDA/CPU)                                  │
│  - EfficientNetV2-S (Transfer Learning)                     │
│  - Preprocessing Pipeline                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Modelo (model_B.pth)                        │
│  - EfficientNetV2-S fine-tuned                              │
│  - Input: 224x224 RGB                                       │
│  - Output: [asphalt, belgian_blocks, offroad]               │
│  - Trained with Focal Loss + Data Augmentation              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura do Projeto

```
trabalho-ia/
├── 📁 backend-go/              # Backend alternativo em Go (descontinuado)
├── 📁 dataset_processed/       # Dataset organizado e processado
│   ├── train/                  # Dados de treino
│   ├── val/                    # Dados de validação
│   └── test/                   # Dados de teste
├── 📁 frontend-react/          # Frontend em React/Next.js
│   ├── app/                    # Páginas e layouts
│   ├── components/             # Componentes React
│   ├── lib/                    # Utilitários e API client
│   ├── types/                  # TypeScript types
│   └── public/                 # Arquivos estáticos
├── 📁 notebooks/               # Notebooks Jupyter de treinamento
│   ├── ProjetoFinal_IA_UFPE4.ipynb  # Versão mais recente
│   └── ...
├── 📁 results/                 # Resultados do treinamento
│   ├── plots/                  # Gráficos e visualizações
│   │   ├── curvas_finais.png
│   │   ├── matrizes_finais.png
│   │   └── ...
│   └── images/                 # Imagens auxiliares
├── 📁 scripts/                 # Scripts auxiliares
│   └── frontend_premium.py     # Frontend alternativo
├── 📁 docs/                    # Documentação adicional
│   ├── README_PROJECT.md
│   └── VERIFICACAO_MODELO.txt
├── 📄 app.py                   # API FastAPI (Backend Principal)
├── 📄 model_B.pth              # Modelo treinado (83.94% F1-Score)
├── 📄 requirements.txt         # Dependências Python
├── 📄 README.md                # Este arquivo
└── 📄 .gitignore               # Arquivos ignorados pelo git
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- npm ou yarn
- (Opcional) GPU NVIDIA com CUDA 11.8+

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/soninhoxs/projetoIA.git
cd projetoIA
```

### 2️⃣ Backend (FastAPI)

```bash
# Instalar PyTorch (escolha uma opção)

# Com GPU (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Sem GPU (apenas CPU)
pip install torch torchvision torchaudio

# Instalar outras dependências
pip install fastapi uvicorn[standard] python-multipart pillow

# Baixar modelo treinado (link fornecido separadamente)
# Colocar model_B.pth na raiz do projeto

# Rodar API
python app.py
```

A API estará disponível em: `http://localhost:8000`

### 3️⃣ Frontend (React/Next.js)

```bash
# Navegar para a pasta
cd frontend-react

# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev

# Ou build para produção
npm run build
npm start
```

O frontend estará disponível em: `http://localhost:3000`

---

## 📁 Estrutura do Projeto

```
projetoIA/
├── 📄 app.py                          # Backend FastAPI
├── 🔧 model_B.pth                     # Modelo treinado (não versionado)
├── 📓 ProjetoFinal_IA_UFPE.ipynb     # Notebook de treinamento
├── 🐍 frontend_premium.py             # Frontend Streamlit (alternativo)
├── 📚 README.md                       # Este arquivo
├── 🚫 .gitignore                      # Arquivos ignorados
│
├── 📂 frontend-react/                 # Frontend Next.js
│   ├── 📂 app/
│   │   ├── layout.tsx                # Layout principal
│   │   ├── page.tsx                  # Página home
│   │   └── globals.css               # Estilos globais
│   │
│   ├── 📂 components/
│   │   ├── Upload.tsx                # Componente de upload
│   │   ├── Results.tsx               # Componente de resultados
│   │   └── StatusBadge.tsx           # Badge de status
│   │
│   ├── 📂 lib/
│   │   └── api.ts                    # Cliente API
│   │
│   ├── 📂 types/
│   │   └── index.ts                  # TypeScript types
│   │
│   ├── ⚙️ next.config.js              # Configuração Next.js
│   ├── ⚙️ tailwind.config.js          # Configuração Tailwind
│   ├── ⚙️ tsconfig.json               # Configuração TypeScript
│   └── 📦 package.json                # Dependências npm
│
└── 📂 dataset_processed/              # Dataset (não versionado)
    ├── train/
    └── test/
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### `GET /`
**Informações da API**

**Response:**
```json
{
  "mensagem": "API de Classificação de Superfícies de Vias",
  "status": "online",
  "device": "cuda",
  "classes": ["asphalt", "belgian_blocks", "offroad"],
  "f1_test": 0.8387,
  "acc_test": 0.9148
}
```

### `GET /health`
**Health check da API**

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### `POST /predict`
**Classificar imagem de via**

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** 
  - `image`: Arquivo de imagem (JPEG/PNG)

**Response:**
```json
{
  "prediction": "asphalt",
  "confidence": 0.9823,
  "probabilities": {
    "asphalt": 0.9823,
    "belgian_blocks": 0.0124,
    "offroad": 0.0053
  },
  "processing_time_ms": 45.2
}
```

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@road_image.jpg"
```

---

## 🎨 Design System

### Paleta de Cores

| Nome | Hex | Uso |
|------|-----|-----|
| Primary (Slate) | `#94a3b8` | Asfalto, elementos principais |
| Accent (Sky) | `#38bdf8` | Blocos Belgas, destaques |
| Success (Green) | `#4ade80` | Off-road, confirmações |

### Tipografia

- **Sans:** Inter (UI elements)
- **Mono:** JetBrains Mono (código, dados)

### Princípios

- ✅ Contraste WCAG AA compliance (7:1+)
- ✅ Mobile-first responsive design
- ✅ Animações suaves (< 300ms)
- ✅ Feedback visual imediato
- ✅ Estados de loading claros

---

## 🧪 Metodologia de Treinamento

### Transfer Learning
- Base: EfficientNetV2-S pré-treinado (ImageNet)
- Fine-tuning em 2 fases:
  1. Apenas classificador (lr=0.001)
  2. 2 últimos blocos + classificador (lr=0.0001)

### Técnicas de Balanceamento
- **Focal Loss** (gamma=2) para classes desbalanceadas
- **WeightedRandomSampler** no DataLoader
- **Data Augmentation** diferenciado por classe

### Preprocessamento
- Crop: Remove 35% topo + 7.5% laterais
- Resize: 224x224
- Normalização: ImageNet stats
- Augmentation: Rotação, flip, cor, brilho

---

## 📦 Deploy

### Backend (Render/Railway)

```bash
# Dockerfile exemplo
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Frontend (Vercel)

```bash
cd frontend-react
vercel
```

**Variáveis de ambiente:**
```env
NEXT_PUBLIC_API_URL=https://sua-api.railway.app
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Inteligência Artificial do CIn-UFPE.

---

## 👥 Autores

<div align="center">

### João Henrique dos Santos Silva
📧 jhss2@cin.ufpe.br

### Carlos Vinicius Felix da Silva
📧 cvfs@cin.ufpe.br

**Centro de Informática - Universidade Federal de Pernambuco**  
**2026**

</div>

---

## 🙏 Agradecimentos

- Prof. da disciplina de Inteligência Artificial (CIn-UFPE)
- PyTorch e TorchVision pela excelente biblioteca
- FastAPI e Next.js pelos frameworks eficientes
- Comunidade open-source de Machine Learning

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

[![GitHub](https://img.shields.io/github/stars/soninhoxs/projetoIA?style=social)](https://github.com/soninhoxs/projetoIA)

**Desenvolvido com ❤️ no CIn-UFPE | 2026**

</div>
