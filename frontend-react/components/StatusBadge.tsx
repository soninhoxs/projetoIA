interface StatusBadgeProps {
  isOnline: boolean
}

export default function StatusBadge({ isOnline }: StatusBadgeProps) {
  return (
    <div
      className={`
        inline-flex items-center gap-2 px-4 py-2 rounded-full
        text-xs font-mono font-bold tracking-wider uppercase
        border transition-all duration-300
        ${
          isOnline
            ? 'bg-success-500/20 border-success-500/50 text-success-500 animate-pulse'
            : 'bg-red-500/20 border-red-500/50 text-red-500'
        }
      `}
    >
      <span className="relative flex h-2 w-2 flex-shrink-0">
        {isOnline && (
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success-400 opacity-75"></span>
        )}
        <span
          className={`relative inline-flex rounded-full h-2 w-2 ${
            isOnline ? 'bg-success-500' : 'bg-red-500'
          }`}
        ></span>
      </span>
      <span className="whitespace-nowrap">{isOnline ? 'API Online' : 'API Offline'}</span>
    </div>
  )
}
