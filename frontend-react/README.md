# Road Surface AI - Frontend React

Frontend profissional em Next.js 14 + TypeScript + Tailwind CSS

## 🚀 Instalação

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Iniciar produção
npm start
```

## 📁 Estrutura

```
frontend-react/
├── app/
│   ├── layout.tsx      # Layout principal
│   ├── page.tsx        # Página home
│   └── globals.css     # Estilos globais
├── components/
│   ├── Upload.tsx      # Componente de upload
│   ├── Results.tsx     # Componente de resultados
│   └── StatusBadge.tsx # Badge de status da API
├── lib/
│   └── api.ts          # Funções de API
├── types/
│   └── index.ts        # TypeScript types
└── public/             # Assets estáticos
```

## 🎨 Design System

### Cores Neutras
- **Primary**: Tons de cinza (slate)
- **Accent**: Azul suave (sky)
- **Success**: Verde profissional

### Tipografia
- **Sans**: Inter
- **Mono**: JetBrains Mono

## 🔌 API

Configure a URL da API em `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ✨ Features

- ✅ TypeScript para type safety
- ✅ Tailwind CSS com design neutro e profissional
- ✅ Upload com drag & drop
- ✅ Gráficos interativos (Recharts)
- ✅ Responsivo (mobile-first)
- ✅ Performance otimizada (Next.js 14)
- ✅ Loading states e error handling
- ✅ Real-time API health check

## 📦 Deploy

### Vercel (Recomendado)
```bash
npm install -g vercel
vercel
```

### Docker
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## 🧪 QA Checklist

- ✅ Upload funciona com drag & drop
- ✅ Upload funciona com click
- ✅ Validação de tipos de arquivo
- ✅ Loading states durante predição
- ✅ Error handling robusto
- ✅ API health check em tempo real
- ✅ Resultados exibem corretamente
- ✅ Gráficos renderizam
- ✅ Responsive em mobile/tablet/desktop
- ✅ Performance otimizada
