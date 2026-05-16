'use client'

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import type { PredictionResult } from '@/types'

interface ResultsProps {
  result: PredictionResult | null
  imageUrl: string | null
}

const classDisplay = {
  asphalt: { 
    name: 'Asfalto', 
    color: '#94a3b8', // Mais claro
    bgColor: 'bg-primary-500',
    borderColor: 'border-primary-400'
  },
  belgian_blocks: { 
    name: 'Paralelepípedo', 
    color: '#38bdf8', // Azul mais vibrante
    bgColor: 'bg-accent-500',
    borderColor: 'border-accent-400'
  },
  offroad: { 
    name: 'Off-road', 
    color: '#4ade80', // Verde mais vibrante
    bgColor: 'bg-success-500',
    borderColor: 'border-success-400'
  },
}

export default function Results({ result, imageUrl }: ResultsProps) {
  if (!result) {
    return (
      <div className="flex items-center justify-center h-64 text-primary-500">
        <div className="text-center space-y-3">
          <div className="w-16 h-16 mx-auto rounded-full bg-primary-800/50 flex items-center justify-center">
            <svg className="w-8 h-8 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p className="text-sm">Faça upload de uma imagem primeiro</p>
        </div>
      </div>
    )
  }

  const display = classDisplay[result.prediction as keyof typeof classDisplay]
  
  const chartData = Object.entries(result.probabilities).map(([key, value]) => ({
    name: classDisplay[key as keyof typeof classDisplay]?.name || key,
    value: value * 100,
    color: classDisplay[key as keyof typeof classDisplay]?.color || '#64748b',
  }))

  return (
    <div className="space-y-6">
      {/* Prediction result */}
      <div className={`${display?.bgColor}/15 border-2 ${display?.borderColor} rounded-xl p-6 text-center backdrop-blur-sm shadow-lg overflow-hidden`}>
        <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full ${display?.bgColor}/25 mb-4 shadow-lg`}>
          <div className={`w-10 h-10 rounded-full ${display?.bgColor} animate-pulse shadow-xl`}></div>
        </div>
        <h3 className="text-2xl sm:text-3xl font-bold mb-4 text-primary-100">
          {display?.name}
        </h3>
        
        {/* Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="glass rounded-lg p-4 border border-primary-700/50 overflow-hidden">
            <p className="text-primary-400 text-xs font-mono uppercase tracking-wider mb-2 font-semibold truncate">
              Confiança
            </p>
            <p className="text-3xl sm:text-4xl font-bold truncate" style={{ color: display?.color }}>
              {(result.confidence * 100).toFixed(1)}%
            </p>
          </div>
          <div className="glass rounded-lg p-4 border border-primary-700/50 overflow-hidden">
            <p className="text-primary-400 text-xs font-mono uppercase tracking-wider mb-2 font-semibold truncate">
              Latência
            </p>
            <p className="text-3xl sm:text-4xl font-bold text-accent-400 truncate">
              {result.processing_time_ms.toFixed(0)}ms
            </p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-primary-900/70 rounded-xl p-5 border border-primary-700/50 backdrop-blur-sm overflow-hidden">
        <h4 className="text-sm font-semibold text-primary-200 mb-4 flex items-center gap-2">
          <svg className="w-4 h-4 text-accent-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span className="truncate">Distribuição de Probabilidades</span>
        </h4>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={chartData} margin={{ top: 20, right: 10, left: 0, bottom: 5 }}>
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#e2e8f0', fontSize: 12, fontWeight: 600 }}
              axisLine={{ stroke: '#475569', strokeWidth: 1 }}
              tickLine={false}
            />
            <YAxis 
              tick={{ fill: '#e2e8f0', fontSize: 11, fontWeight: 500 }}
              axisLine={{ stroke: '#475569', strokeWidth: 1 }}
              tickLine={false}
              tickFormatter={(value) => `${value}%`}
              domain={[0, 100]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                border: '1px solid #64748b',
                borderRadius: '12px',
                padding: '12px 16px',
                boxShadow: '0 10px 40px rgba(0,0,0,0.5)',
              }}
              labelStyle={{ 
                fontWeight: 700, 
                marginBottom: '6px',
                color: '#f1f5f9',
                fontSize: '14px'
              }}
              formatter={(value: number) => [
                <span style={{ color: '#4ade80', fontWeight: 700 }}>{value.toFixed(2)}%</span>, 
                <span style={{ color: '#e0f2fe' }}>Probabilidade</span>
              ]}
              cursor={{ fill: 'rgba(148, 163, 184, 0.15)' }}
            />
            <Bar 
              dataKey="value" 
              radius={[12, 12, 0, 0]}
              animationDuration={800}
              animationEasing="ease-out"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.color}
                  stroke={entry.color}
                  strokeWidth={0}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        
        {/* Legend */}
        <div className="flex flex-wrap justify-center gap-4 mt-4 pt-3 border-t border-primary-800/50">
          {chartData.map((item, index) => (
            <div key={index} className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded-full flex-shrink-0" 
                style={{ backgroundColor: item.color }}
              />
              <span className="text-xs font-medium text-primary-200 whitespace-nowrap">{item.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
