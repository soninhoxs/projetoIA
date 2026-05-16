from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_v2_s
import io
import time

app = FastAPI(
    title="API de Classificação de Superfícies de Vias",
    description="Classifica imagens de vias em: Asphalt, Belgian Blocks ou Off-road",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
CLASS_NAMES = ['asphalt', 'belgian_blocks', 'offroad']

# Classe de crop
class CropBordas:
    def __init__(self, pct_topo=0.35, pct_lateral=0.075):
        self.pct_topo = pct_topo
        self.pct_lateral = pct_lateral
    
    def __call__(self, img):
        w, h = img.size
        top = int(h * self.pct_topo)
        lado = int(w * self.pct_lateral)
        return img.crop((lado, top, w - lado, h))

# Transforms
eval_transform = transforms.Compose([
    CropBordas(0.35, 0.075),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# Criar modelo
def criar_modelo():
    from torchvision.models import EfficientNet_V2_S_Weights
    model = efficientnet_v2_s(weights=EfficientNet_V2_S_Weights.IMAGENET1K_V1)
    
    for param in model.features.parameters():
        param.requires_grad = False
    
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(in_features, 3)
    )
    
    for param in model.features[-1].parameters():
        param.requires_grad = True
    for param in model.features[-2].parameters():
        param.requires_grad = True
    
    return model

# Carregar modelo
print("Carregando modelo...")
model = criar_modelo()
checkpoint = torch.load('model_B.pth', map_location=device, weights_only=False)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()
print(f"[OK] Modelo carregado! Device: {device}")

@app.get("/")
def read_root():
    return {
        "mensagem": "API de Classificação de Superfícies de Vias",
        "status": "online",
        "device": str(device),
        "classes": CLASS_NAMES,
        "f1_test": float(checkpoint.get('f1_test', 0)),
        "acc_test": float(checkpoint.get('acc_test', 0))
    }

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    start_time = time.time()
    
    try:
        contents = await image.read()
        
        # Tentar abrir a imagem - PIL valida automaticamente
        try:
            img = Image.open(io.BytesIO(contents)).convert('RGB')
        except Exception:
            raise HTTPException(400, "Formato inválido. Use JPEG ou PNG.")
        
        img_tensor = eval_transform(img).unsqueeze(0).to(device)
        
        with torch.no_grad():
            output = model(img_tensor)
            probs = torch.softmax(output, dim=1)[0]
            pred_idx = output.argmax(1).item()
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            "prediction": CLASS_NAMES[pred_idx],
            "confidence": float(probs[pred_idx]),
            "probabilities": {
                CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))
            },
            "processing_time_ms": round(processing_time, 2)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erro ao processar imagem: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.get("/status", response_class=HTMLResponse)
def status_page():
    f1_score = checkpoint.get('f1_test', 0) * 100
    acc = checkpoint.get('acc_test', 0) * 100
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Road Surface AI - Status</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #e2e8f0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: rgba(30, 41, 59, 0.8);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(100, 116, 139, 0.3);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            }}
            h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 10px;
                background: linear-gradient(90deg, #60a5fa, #34d399);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .subtitle {{
                color: #94a3b8;
                margin-bottom: 30px;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            .status-badge {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: rgba(34, 197, 94, 0.2);
                border: 1px solid #22c55e;
                color: #22c55e;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.875rem;
                font-weight: 600;
                margin-bottom: 30px;
            }}
            .pulse {{
                width: 8px;
                height: 8px;
                background: #22c55e;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-top: 20px;
            }}
            .metric {{
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(100, 116, 139, 0.3);
                border-radius: 12px;
                padding: 20px;
            }}
            .metric-label {{
                color: #94a3b8;
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }}
            .metric-value {{
                font-size: 1.8rem;
                font-weight: 700;
                color: #60a5fa;
            }}
            .info {{
                margin-top: 20px;
                padding: 15px;
                background: rgba(59, 130, 246, 0.1);
                border-left: 3px solid #3b82f6;
                border-radius: 8px;
                font-size: 0.875rem;
                color: #cbd5e1;
            }}
            .device {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                margin-top: 15px;
                font-size: 0.875rem;
                color: #94a3b8;
            }}
            .gpu-badge {{
                background: rgba(168, 85, 247, 0.2);
                color: #a855f7;
                padding: 2px 8px;
                border-radius: 4px;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛣️ Road Surface AI</h1>
            <p class="subtitle">API Status Dashboard</p>
            
            <div class="status-badge">
                <div class="pulse"></div>
                <span>API ONLINE</span>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-label">F1-Score</div>
                    <div class="metric-value">{f1_score:.2f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Accuracy</div>
                    <div class="metric-value">{acc:.2f}%</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Model</div>
                    <div class="metric-value" style="font-size: 1.2rem;">EfficientNetV2-S</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Classes</div>
                    <div class="metric-value" style="font-size: 1.2rem;">3</div>
                </div>
            </div>
            
            <div class="device">
                Device: <span class="gpu-badge">{str(device).upper()}</span>
            </div>
            
            <div class="info">
                <strong>✓ Model Loaded:</strong> model_B.pth<br>
                <strong>✓ Endpoints:</strong> /predict, /health, /docs<br>
                <strong>✓ Frontend:</strong> <a href="http://localhost:3000" style="color: #60a5fa;">http://localhost:3000</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Volta para porta 8000