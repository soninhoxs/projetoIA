from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)