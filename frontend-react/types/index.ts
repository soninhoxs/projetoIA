export interface PredictionResult {
  prediction: string
  confidence: number
  probabilities: {
    asphalt: number
    belgian_blocks: number
    offroad: number
  }
  processing_time_ms: number
}

export interface ApiHealthResponse {
  status: string
  model_loaded: boolean
}
