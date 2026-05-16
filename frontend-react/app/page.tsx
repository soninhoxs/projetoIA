'use client'

import { useState, useEffect } from 'react'
import Upload from '@/components/Upload'
import Results from '@/components/Results'
import StatusBadge from '@/components/StatusBadge'
import { checkApiHealth } from '@/lib/api'
import type { PredictionResult } from '@/types'

export default function Home() {
  const [isApiOnline, setIsApiOnline] = useState<boolean>(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)

  useEffect(() => {
    const checkHealth = async () => {
      const online = await checkApiHealth()
      setIsApiOnline(online)
    }
    
    checkHealth()
    const interval = setInterval(checkHealth, 5000)
    
    return () => clearInterval(interval)
  }, [])

  const handlePrediction = (data: PredictionResult, imageUrl: string) => {
    setResult(data)
    setUploadedImage(imageUrl)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-950 via-primary-900 to-primary-950">
      {/* Grid pattern overlay */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(100,116,139,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(100,116,139,0.03)_1px,transparent_1px)] bg-[size:50px_50px] pointer-events-none" />
      
      <div className="relative z-10 container mx-auto px-4 py-8 md:py-12">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold mb-3 bg-gradient-to-r from-primary-200 via-accent-400 to-primary-300 bg-clip-text text-transparent tracking-tight">
            Road Surface AI
          </h1>
          <p className="text-primary-400 text-sm md:text-base font-mono tracking-widest uppercase">
            Deep Learning • Computer Vision • Real-Time Classification
          </p>
          
          <div className="mt-6 flex justify-center">
            <StatusBadge isOnline={isApiOnline} />
          </div>
        </header>

        {/* Main content */}
        <div className="grid md:grid-cols-2 gap-6 md:gap-8 max-w-7xl mx-auto">
          {/* Upload section */}
          <div className="glass glass-hover rounded-2xl p-6 overflow-hidden">
            <h2 className="text-xl font-semibold mb-4 text-primary-100 flex items-center gap-2">
              <svg className="w-5 h-5 text-accent-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <span className="truncate">Upload de Imagem</span>
            </h2>
            <Upload 
              onPrediction={handlePrediction}
              isApiOnline={isApiOnline}
            />
          </div>

          {/* Results section */}
          <div className="glass glass-hover rounded-2xl p-6 overflow-hidden">
            <h2 className="text-xl font-semibold mb-4 text-primary-100 flex items-center gap-2">
              <svg className="w-5 h-5 text-success-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="truncate">Resultado da Análise</span>
            </h2>
            <Results 
              result={result}
              imageUrl={uploadedImage}
            />
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-primary-500 text-sm">
          <div className="glass rounded-xl p-6 max-w-3xl mx-auto overflow-hidden">
            <div className="flex items-center justify-center gap-2 mb-3">
              <svg className="w-5 h-5 text-accent-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <p className="font-semibold text-primary-300">DESENVOLVIDO POR</p>
            </div>
            <p className="mb-1 px-2">João Henrique dos Santos Silva & Carlos Vinicius Felix da Silva</p>
            <p className="text-primary-600 mb-4">CIn - UFPE | Inteligência Artificial | 2026</p>
            <div className="flex flex-wrap justify-center gap-3 text-xs font-mono px-2">
              <span className="flex items-center gap-1 whitespace-nowrap">
                <span className="w-2 h-2 rounded-full bg-primary-500 flex-shrink-0"></span>
                <span><strong className="text-primary-400">MODELO:</strong> EfficientNetV2-S</span>
              </span>
              <span className="flex items-center gap-1 whitespace-nowrap">
                <span className="w-2 h-2 rounded-full bg-success-500 flex-shrink-0"></span>
                <span><strong className="text-success-500">F1-MACRO:</strong> 83.87%</span>
              </span>
              <span className="flex items-center gap-1 whitespace-nowrap">
                <span className="w-2 h-2 rounded-full bg-accent-500 flex-shrink-0"></span>
                <span><strong className="text-accent-500">ACC:</strong> 91.48%</span>
              </span>
            </div>
          </div>
        </footer>
      </div>
    </main>
  )
}
