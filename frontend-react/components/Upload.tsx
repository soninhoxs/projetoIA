'use client'

import { useState, useRef, ChangeEvent, DragEvent } from 'react'
import { Upload as UploadIcon, Loader2 } from 'lucide-react'
import { predictImage } from '@/lib/api'
import type { PredictionResult } from '@/types'

interface UploadProps {
  onPrediction: (result: PredictionResult, imageUrl: string) => void
  isApiOnline: boolean
}

export default function Upload({ onPrediction, isApiOnline }: UploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFile = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Por favor, envie apenas imagens')
      return
    }

    setError(null)
    const imageUrl = URL.createObjectURL(file)
    setPreview(imageUrl)
    setIsLoading(true)

    try {
      const result = await predictImage(file)
      onPrediction(result, imageUrl)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao processar imagem')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) handleFile(file)
  }

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  return (
    <div className="space-y-3 md:space-y-4">
      {/* Upload area */}
      <div
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          relative border-2 border-dashed rounded-xl p-4 md:p-8 cursor-pointer
          transition-all duration-300 group
          ${isDragging 
            ? 'border-accent-500 bg-accent-500/10' 
            : 'border-primary-700 hover:border-accent-600 hover:bg-primary-800/30'
          }
          ${!isApiOnline && 'opacity-50 cursor-not-allowed'}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleChange}
          disabled={!isApiOnline || isLoading}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center text-center space-y-2 md:space-y-3">
          <div className={`
            p-3 md:p-4 rounded-full transition-colors
            ${isDragging ? 'bg-accent-500/20' : 'bg-primary-800 group-hover:bg-primary-700'}
          `}>
            {isLoading ? (
              <Loader2 className="w-6 h-6 md:w-8 md:h-8 text-accent-500 animate-spin" />
            ) : (
              <UploadIcon className="w-6 h-6 md:w-8 md:h-8 text-primary-300 group-hover:text-accent-500 transition-colors" />
            )}
          </div>

          <div>
            <p className="text-primary-200 font-medium mb-1 text-sm md:text-base break-words px-2">
              {isLoading ? 'Processando...' : 'Clique ou arraste uma imagem'}
            </p>
            <p className="text-primary-500 text-xs md:text-sm">
              PNG, JPG ou JPEG até 10MB
            </p>
          </div>
        </div>
      </div>

      {/* Preview */}
      {preview && (
        <div className="rounded-xl overflow-hidden border border-primary-800">
          <img 
            src={preview} 
            alt="Preview" 
            className="w-full h-auto object-cover max-h-64 md:max-h-96"
          />
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-2 md:p-3 text-red-400 text-xs md:text-sm flex items-start gap-2">
          <svg className="w-4 h-4 md:w-5 md:h-5 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="break-words">{error}</span>
        </div>
      )}

      {/* Info message */}
      {!isApiOnline && (
        <div className="bg-amber-500/10 border border-amber-500/50 rounded-lg p-2 md:p-3 text-amber-400 text-xs md:text-sm flex items-start gap-2">
          <svg className="w-4 h-4 md:w-5 md:h-5 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <p className="font-semibold mb-1 break-words">API Offline</p>
            <p className="text-[10px] md:text-xs break-all">Inicie com: <code className="font-mono bg-amber-500/20 px-1 py-0.5 rounded">python app.py</code></p>
          </div>
        </div>
      )}
    </div>
  )
}
