# 🛣️ Road Surface AI

Sistema completo de classificação de superfícies de vias usando Deep Learning com FastAPI + React/Next.js.

## 👥 Autores

- **João Henrique dos Santos Silva** - jhss2@cin.ufpe.br
- **Carlos Vinicius Felix da Silva** - cvfs@cin.ufpe.br

**CIn - UFPE | Inteligência Artificial | 2026**

---

## 📊 Resultados do Modelo

- **Modelo:** EfficientNetV2-S (21M parâmetros)
- **F1-Macro:** 83.87%
- **Acurácia:** 91.48%
- **Classes:** Asfalto, Blocos Belgas, Off-road

---

## 🏗️ Arquitetura

### Backend (FastAPI)
- Python 3.11+
- PyTorch
- FastAPI
- Modelo: EfficientNetV2-S
- Inferência em tempo real

### Frontend (React/Next.js)
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts
- Design System profissional

---

## 🚀 Instalação e Uso

### 1. Backend (API)

```bash
# Instalar dependências
pip install torch torchvision fastapi uvicorn python-multipart pillow

# Rodar API
python app.py
```

A API estará disponível em: `http://localhost:8000`

### 2. Frontend (React)

```bash
# Navegar para a pasta
cd frontend-react

# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev
```

O frontend estará disponível em: `http://localhost:3000`

---

## 📁 Estrutura do Projeto

```
.
├── app.py                    # Backend FastAPI
├── model_B.pth              # Modelo treinado (não versionado)
├── frontend-react/          # Frontend Next.js
│   ├── app/                 # Pages e layouts
│   ├── components/          # Componentes React
│   ├── lib/                 # Utilitários e API client
│   └── types/              # TypeScript types
├── frontend_premium.py      # Frontend Streamlit (alternativo)
├── ProjetoFinal_IA_UFPE.ipynb  # Notebook de treinamento
└── README.md
```

---

## 🎨 Features

### Backend
- ✅ API REST com FastAPI
- ✅ Upload de imagens
- ✅ Inferência em tempo real
- ✅ Preprocessamento otimizado
- ✅ Health check endpoint
- ✅ CORS habilitado

### Frontend
- ✅ Interface moderna e profissional
- ✅ Upload com drag & drop
- ✅ Preview de imagens
- ✅ Gráficos interativos
- ✅ Real-time API health check
- ✅ Design responsivo
- ✅ TypeScript para type safety
- ✅ Otimizado para acessibilidade (WCAG AA)

---

## 🔌 API Endpoints

### GET `/`
Informações da API

### GET `/health`
Health check da API

### POST `/predict`
Classificar imagem
- **Body:** multipart/form-data
- **Field:** image (file)
- **Response:**
```json
{
  "prediction": "asphalt",
  "confidence": 0.98,
  "probabilities": {
    "asphalt": 0.98,
    "belgian_blocks": 0.01,
    "offroad": 0.01
  },
  "processing_time_ms": 45.2
}
```

---

## 🎯 Design System

### Paleta de Cores
- **Primary (Slate):** Cinzas neutros
- **Accent (Sky):** Azul suave
- **Success (Green):** Verde profissional

### Tipografia
- **Sans:** Inter
- **Mono:** JetBrains Mono

### Princípios
- Contraste WCAG AA compliance
- Mobile-first responsive
- Animações suaves
- Feedback visual claro

---

## 📦 Deploy

### Backend (API)
```bash
# Produção com Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

### Frontend (Vercel - Recomendado)
```bash
cd frontend-react
vercel
```

---

## 🧪 Testes

### Backend
```bash
pytest tests/
```

### Frontend
```bash
cd frontend-react
npm run test
```

---

## 📝 Licença

Projeto acadêmico desenvolvido para a disciplina de Inteligência Artificial do CIn-UFPE.

---

## 🙏 Agradecimentos

- Prof. da disciplina de Inteligência Artificial (CIn-UFPE)
- PyTorch e TorchVision
- FastAPI e Next.js
- Comunidade open-source

---

**Desenvolvido com ❤️ no CIn-UFPE | 2026**
