import React, { useState } from 'react';

const QWLDiagrams = () => {
  const [activeSlide, setActiveSlide] = useState(0);

  // Classical WL visualization colors
  const wlColors = ['#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#8b5cf6'];

  const Slide1 = () => (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-rose-400 to-orange-400 bg-clip-text text-transparent">
        Classical Weisfeiler-Lehman Recap
      </h2>
      
      <div className="flex items-center justify-center gap-8 flex-wrap">
        {/* Initial coloring */}
        <div className="flex flex-col items-center">
          <svg width={200} height={200}>
            <defs>
              <filter id="node-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
            </defs>
            {/* Edges */}
            <line x1={100} y1={40} x2={50} y2={100} stroke="#475569" strokeWidth={2}/>
            <line x1={100} y1={40} x2={150} y2={100} stroke="#475569" strokeWidth={2}/>
            <line x1={50} y1={100} x2={100} y2={160} stroke="#475569" strokeWidth={2}/>
            <line x1={150} y1={100} x2={100} y2={160} stroke="#475569" strokeWidth={2}/>
            <line x1={50} y1={100} x2={150} y2={100} stroke="#475569" strokeWidth={2}/>
            {/* Nodes - all same color initially */}
            {[[100,40], [50,100], [150,100], [100,160]].map(([x,y], i) => (
              <g key={i}>
                <circle cx={x} cy={y} r={20} fill="#64748b" stroke="#94a3b8" strokeWidth={2}/>
                <text x={x} y={y+5} textAnchor="middle" fill="white" fontSize="14" fontWeight="600">{i}</text>
              </g>
            ))}
          </svg>
          <span className="text-slate-400 text-sm mt-2">t = 0</span>
          <span className="text-slate-500 text-xs">uniform coloring</span>
        </div>

        <svg width={40} height={40}>
          <path d="M 5 20 L 30 20 M 22 12 L 30 20 L 22 28" stroke="#f59e0b" strokeWidth={2} fill="none"/>
        </svg>

        {/* After 1 iteration */}
        <div className="flex flex-col items-center">
          <svg width={200} height={200}>
            <line x1={100} y1={40} x2={50} y2={100} stroke="#475569" strokeWidth={2}/>
            <line x1={100} y1={40} x2={150} y2={100} stroke="#475569" strokeWidth={2}/>
            <line x1={50} y1={100} x2={100} y2={160} stroke="#475569" strokeWidth={2}/>
            <line x1={150} y1={100} x2={100} y2={160} stroke="#475569" strokeWidth={2}/>
            <line x1={50} y1={100} x2={150} y2={100} stroke="#475569" strokeWidth={2}/>
            {/* Nodes colored by degree */}
            {[[100,40,2,'#f59e0b'], [50,100,3,'#10b981'], [150,100,3,'#10b981'], [100,160,2,'#f59e0b']].map(([x,y,deg,col], i) => (
              <g key={i}>
                <circle cx={x} cy={y} r={20} fill={col} stroke={col} strokeWidth={2} filter="url(#node-glow)"/>
                <text x={x} y={y+5} textAnchor="middle" fill="#1e293b" fontSize="14" fontWeight="600">{deg}</text>
              </g>
            ))}
          </svg>
          <span className="text-slate-400 text-sm mt-2">t = 1</span>
          <span className="text-slate-500 text-xs">degree coloring</span>
        </div>

        <svg width={40} height={40}>
          <path d="M 5 20 L 30 20 M 22 12 L 30 20 L 22 28" stroke="#f59e0b" strokeWidth={2} fill="none"/>
        </svg>

        {/* After refinement */}
        <div className="flex flex-col items-center">
          <svg width={200} height={200}>
            <line x1={100} y1={40} x2={50} y2={100} stroke="#475569" strokeWidth={2}/>
            <line x1={100} y1={40} x2={150} y2={100} stroke="#475569" strokeWidth={2}/>
            <line x1={50} y1={100} x2={100} y2={160} stroke="#475569" strokeWidth={2}/>
            <line x1={150} y1={100} x2={100} y2={160} stroke="#475569" strokeWidth={2}/>
            <line x1={50} y1={100} x2={150} y2={100} stroke="#475569" strokeWidth={2}/>
            {/* Refined colors */}
            {[[100,40,'#3b82f6'], [50,100,'#10b981'], [150,100,'#10b981'], [100,160,'#3b82f6']].map(([x,y,col], i) => (
              <g key={i}>
                <circle cx={x} cy={y} r={20} fill={col} stroke={col} strokeWidth={2} filter="url(#node-glow)"/>
                <text x={x} y={y+5} textAnchor="middle" fill="white" fontSize="10" fontWeight="600">
                  {i === 0 || i === 3 ? '2,3,3' : '3,2,2,3'}
                </text>
              </g>
            ))}
          </svg>
          <span className="text-slate-400 text-sm mt-2">t = 2</span>
          <span className="text-slate-500 text-xs">neighbor aggregation</span>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 max-w-3xl mx-auto">
        <h3 className="text-lg font-semibold text-orange-400 mb-3">Color Refinement Rule</h3>
        <div className="font-mono text-center text-slate-300 text-lg mb-4">
          c<sup>(t+1)</sup>(v) = hash( c<sup>(t)</sup>(v), {'{{'}c<sup>(t)</sup>(u) : u ∈ N(v){'}}' )
        </div>
        <p className="text-slate-400 text-sm text-center">
          Each node's new color is determined by its current color and the <span className="text-orange-300">multiset</span> of its neighbors' colors
        </p>
      </div>
    </div>
  );

  const Slide2 = () => (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
        Quantum WL Circuit Architecture
      </h2>
      
      <div className="max-w-5xl mx-auto">
        {/* Circuit diagram */}
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 mb-6">
          <svg width="100%" height={220} viewBox="0 0 900 220" className="mx-auto">
            {/* Qubit lines */}
            {[0,1,2,3].map(q => (
              <g key={q}>
                <line x1={60} y1={40 + q*45} x2={850} y2={40 + q*45} stroke="#475569" strokeWidth={2}/>
                <text x={35} y={45 + q*45} fill="#64748b" fontSize="12" fontFamily="JetBrains Mono">q{q}</text>
              </g>
            ))}

            {/* Encoder block */}
            <rect x={80} y={20} width={120} height={180} rx={8} fill="#f59e0b" fillOpacity={0.15} stroke="#f59e0b" strokeWidth={2}/>
            <text x={140} y={110} fill="#fbbf24" fontSize="14" textAnchor="middle" fontWeight="600">Encoder</text>
            <text x={140} y={130} fill="#fcd34d" fontSize="10" textAnchor="middle">RY(θ_deg)</text>
            
            {/* Individual RY gates */}
            {[0,1,2,3].map(q => (
              <g key={`ry-${q}`}>
                <rect x={110} y={28 + q*45} width={60} height={24} rx={4} fill="#f59e0b" stroke="#fbbf24"/>
                <text x={140} y={44 + q*45} fill="#1e293b" fontSize="11" textAnchor="middle" fontWeight="600">RY</text>
              </g>
            ))}

            {/* Entangler block */}
            <rect x={220} y={20} width={140} height={180} rx={8} fill="#10b981" fillOpacity={0.15} stroke="#10b981" strokeWidth={2}/>
            <text x={290} y={110} fill="#34d399" fontSize="14" textAnchor="middle" fontWeight="600">Entangler</text>
            <text x={290} y={130} fill="#6ee7b7" fontSize="10" textAnchor="middle">RZZ on edges</text>
            
            {/* RZZ connections */}
            <line x1={260} y1={40} x2={260} y2={85} stroke="#10b981" strokeWidth={3}/>
            <circle cx={260} cy={40} r={5} fill="#10b981"/>
            <circle cx={260} cy={85} r={5} fill="#10b981"/>
            
            <line x1={290} y1={40} x2={290} y2={130} stroke="#10b981" strokeWidth={3}/>
            <circle cx={290} cy={40} r={5} fill="#10b981"/>
            <circle cx={290} cy={130} r={5} fill="#10b981"/>
            
            <line x1={320} y1={85} x2={320} y2={130} stroke="#10b981" strokeWidth={3}/>
            <circle cx={320} cy={85} r={5} fill="#10b981"/>
            <circle cx={320} cy={130} r={5} fill="#10b981"/>

            {/* Repetition bracket */}
            <rect x={380} y={10} width={350} height={200} rx={8} fill="none" stroke="#8b5cf6" strokeWidth={2} strokeDasharray="6,4"/>
            <text x={555} y={205} fill="#a78bfa" fontSize="11" textAnchor="middle">× r repetitions</text>

            {/* Mixer block */}
            <rect x={400} y={20} width={100} height={180} rx={8} fill="#3b82f6" fillOpacity={0.15} stroke="#3b82f6" strokeWidth={2}/>
            <text x={450} y={110} fill="#60a5fa" fontSize="14" textAnchor="middle" fontWeight="600">Mixer</text>
            <text x={450} y={130} fill="#93c5fd" fontSize="10" textAnchor="middle">RX(β)</text>
            
            {[0,1,2,3].map(q => (
              <g key={`rx-${q}`}>
                <rect x={420} y={28 + q*45} width={60} height={24} rx={4} fill="#3b82f6" stroke="#60a5fa"/>
                <text x={450} y={44 + q*45} fill="white" fontSize="11" textAnchor="middle" fontWeight="600">RX</text>
              </g>
            ))}

            {/* Second entangler */}
            <rect x={520} y={20} width={100} height={180} rx={8} fill="#10b981" fillOpacity={0.1} stroke="#10b981" strokeWidth={1.5}/>
            <text x={570} y={115} fill="#34d399" fontSize="12" textAnchor="middle">RZZ</text>

            {/* Dots */}
            <text x={650} y={100} fill="#64748b" fontSize="24">···</text>

            {/* Measurement */}
            <rect x={760} y={20} width={80} height={180} rx={8} fill="#ef4444" fillOpacity={0.15} stroke="#ef4444" strokeWidth={2}/>
            <text x={800} y={100} fill="#f87171" fontSize="14" textAnchor="middle" fontWeight="600">Measure</text>
            {[0,1,2,3].map(q => (
              <g key={`m-${q}`}>
                <rect x={775} y={28 + q*45} width={50} height={24} rx={4} fill="#ef4444" stroke="#f87171"/>
                <text x={800} y={44 + q*45} fill="white" fontSize="12" textAnchor="middle">M</text>
              </g>
            ))}
          </svg>
        </div>

        {/* Component descriptions */}
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-amber-900/30 to-amber-800/10 rounded-lg p-4 border border-amber-700/50">
            <h4 className="font-semibold text-amber-400 mb-2 flex items-center gap-2">
              <span className="w-3 h-3 bg-amber-500 rounded-full"></span>
              Encoder
            </h4>
            <p className="text-sm text-slate-300">
              <span className="font-mono text-amber-300">RY(π · deg(v)/n)</span>
            </p>
            <p className="text-xs text-slate-400 mt-1">
              Encodes node degree into qubit amplitude — analogous to initial WL coloring
            </p>
          </div>
          
          <div className="bg-gradient-to-br from-emerald-900/30 to-emerald-800/10 rounded-lg p-4 border border-emerald-700/50">
            <h4 className="font-semibold text-emerald-400 mb-2 flex items-center gap-2">
              <span className="w-3 h-3 bg-emerald-500 rounded-full"></span>
              Entangler
            </h4>
            <p className="text-sm text-slate-300">
              <span className="font-mono text-emerald-300">RZZ(θ)</span> on each edge
            </p>
            <p className="text-xs text-slate-400 mt-1">
              Creates entanglement reflecting graph topology — neighbor information propagates
            </p>
          </div>
          
          <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/10 rounded-lg p-4 border border-blue-700/50">
            <h4 className="font-semibold text-blue-400 mb-2 flex items-center gap-2">
              <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
              Mixer
            </h4>
            <p className="text-sm text-slate-300">
              <span className="font-mono text-blue-300">RX(β)</span> uniform rotation
            </p>
            <p className="text-xs text-slate-400 mt-1">
              Enables interference between computational basis states
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const Slide3 = () => (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">
        Fingerprint Comparison
      </h2>

      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-center gap-6 flex-wrap mb-8">
          {/* Pattern H */}
          <div className="bg-slate-800/50 rounded-xl p-5 border border-slate-700">
            <div className="text-center mb-3">
              <span className="text-fuchsia-400 font-semibold">Pattern H</span>
            </div>
            <svg width={120} height={100}>
              <line x1={60} y1={20} x2={30} y2={70} stroke="#a855f7" strokeWidth={2}/>
              <line x1={60} y1={20} x2={90} y2={70} stroke="#a855f7" strokeWidth={2}/>
              <line x1={30} y1={70} x2={90} y2={70} stroke="#a855f7" strokeWidth={2}/>
              <circle cx={60} cy={20} r={12} fill="#a855f7"/>
              <circle cx={30} cy={70} r={12} fill="#a855f7"/>
              <circle cx={90} cy={70} r={12} fill="#a855f7"/>
            </svg>
            <div className="mt-3 flex justify-center">
              <svg width={100} height={60}>
                {/* Mini histogram */}
                {[0.35, 0.25, 0.18, 0.12, 0.06, 0.04].map((h, i) => (
                  <rect key={i} x={5 + i*15} y={60 - h*120} width={12} height={h*120} fill="#a855f7" rx={2}/>
                ))}
              </svg>
            </div>
            <div className="text-xs text-slate-400 text-center">sorted P(x)</div>
          </div>

          <div className="text-4xl text-slate-500">≟</div>

          {/* Candidate G[S] - match */}
          <div className="bg-slate-800/50 rounded-xl p-5 border border-emerald-700/50">
            <div className="text-center mb-3">
              <span className="text-emerald-400 font-semibold">G[S₁] ✓</span>
            </div>
            <svg width={120} height={100}>
              <line x1={60} y1={20} x2={30} y2={70} stroke="#10b981" strokeWidth={2}/>
              <line x1={60} y1={20} x2={90} y2={70} stroke="#10b981" strokeWidth={2}/>
              <line x1={30} y1={70} x2={90} y2={70} stroke="#10b981" strokeWidth={2}/>
              <circle cx={60} cy={20} r={12} fill="#10b981"/>
              <circle cx={30} cy={70} r={12} fill="#10b981"/>
              <circle cx={90} cy={70} r={12} fill="#10b981"/>
            </svg>
            <div className="mt-3 flex justify-center">
              <svg width={100} height={60}>
                {[0.34, 0.26, 0.17, 0.13, 0.06, 0.04].map((h, i) => (
                  <rect key={i} x={5 + i*15} y={60 - h*120} width={12} height={h*120} fill="#10b981" rx={2}/>
                ))}
              </svg>
            </div>
            <div className="text-xs text-emerald-400 text-center">L² = 0.001</div>
          </div>

          {/* Candidate G[S] - no match */}
          <div className="bg-slate-800/50 rounded-xl p-5 border border-rose-700/50">
            <div className="text-center mb-3">
              <span className="text-rose-400 font-semibold">G[S₂] ✗</span>
            </div>
            <svg width={120} height={100}>
              <line x1={30} y1={30} x2={90} y2={30} stroke="#f43f5e" strokeWidth={2}/>
              <line x1={90} y1={30} x2={60} y2={80} stroke="#f43f5e" strokeWidth={2}/>
              <circle cx={30} cy={30} r={12} fill="#f43f5e"/>
              <circle cx={90} cy={30} r={12} fill="#f43f5e"/>
              <circle cx={60} cy={80} r={12} fill="#f43f5e"/>
            </svg>
            <div className="mt-3 flex justify-center">
              <svg width={100} height={60}>
                {[0.42, 0.30, 0.15, 0.08, 0.03, 0.02].map((h, i) => (
                  <rect key={i} x={5 + i*15} y={60 - h*120} width={12} height={h*120} fill="#f43f5e" rx={2}/>
                ))}
              </svg>
            </div>
            <div className="text-xs text-rose-400 text-center">L² = 0.089</div>
          </div>
        </div>

        {/* Scoring function */}
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 max-w-2xl mx-auto">
          <h3 className="text-lg font-semibold text-violet-400 mb-4 text-center">Fingerprint Distance</h3>
          <div className="font-mono text-center text-slate-200 text-xl mb-4">
            d(H, G[S]) = Σ<sub>i</sub> (p<sub>H</sub><sup>(i)</sup> − p<sub>G[S]</sub><sup>(i)</sup>)²
          </div>
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="text-center">
              <div className="text-2xl font-mono text-emerald-400">d &lt; τ</div>
              <div className="text-xs text-slate-400">likely isomorphic</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-mono text-rose-400">d ≥ τ</div>
              <div className="text-xs text-slate-400">definitely not isomorphic</div>
            </div>
          </div>
        </div>

        <div className="bg-slate-900/50 rounded-lg p-4 mt-6 max-w-2xl mx-auto">
          <p className="text-slate-300 text-sm text-center">
            <span className="text-fuchsia-400 font-semibold">Key insight:</span> Isomorphic graphs produce 
            <span className="text-violet-400"> identical</span> fingerprints (permutation invariant). 
            Non-isomorphic graphs <span className="text-rose-400">almost always</span> differ.
          </p>
        </div>
      </div>
    </div>
  );

  const Slide4 = () => (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
        Two-Phase Algorithm
      </h2>

      <div className="max-w-5xl mx-auto">
        {/* Pipeline visualization */}
        <div className="flex items-center justify-center gap-3 mb-8 flex-wrap">
          <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700 text-center min-w-[140px]">
            <div className="text-3xl mb-2">📊</div>
            <div className="text-sm text-slate-300 font-semibold">All k-subsets</div>
            <div className="text-xs text-slate-500 mt-1">C(n,k) candidates</div>
          </div>
          
          <svg width={50} height={40}><path d="M 5 20 L 40 20 M 32 12 L 40 20 L 32 28" stroke="#10b981" strokeWidth={2} fill="none"/></svg>
          
          <div className="bg-emerald-900/30 rounded-lg p-4 border border-emerald-700/50 text-center min-w-[140px]">
            <div className="text-3xl mb-2">🔬</div>
            <div className="text-sm text-emerald-300 font-semibold">QWL Filter</div>
            <div className="text-xs text-emerald-500 mt-1">O(k) or O(|E|) gates</div>
          </div>
          
          <svg width={50} height={40}><path d="M 5 20 L 40 20 M 32 12 L 40 20 L 32 28" stroke="#10b981" strokeWidth={2} fill="none"/></svg>
          
          <div className="bg-slate-800/50 rounded-lg p-4 border border-amber-700/50 text-center min-w-[140px]">
            <div className="text-3xl mb-2">🎯</div>
            <div className="text-sm text-amber-300 font-semibold">Top-m ranked</div>
            <div className="text-xs text-amber-500 mt-1">m ≪ C(n,k)</div>
          </div>
          
          <svg width={50} height={40}><path d="M 5 20 L 40 20 M 32 12 L 40 20 L 32 28" stroke="#f59e0b" strokeWidth={2} fill="none"/></svg>
          
          <div className="bg-slate-800/50 rounded-lg p-4 border border-violet-700/50 text-center min-w-[140px]">
            <div className="text-3xl mb-2">✓</div>
            <div className="text-sm text-violet-300 font-semibold">Exact verify</div>
            <div className="text-xs text-violet-500 mt-1">Classical ISO</div>
          </div>
        </div>

        {/* Complexity comparison */}
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <h3 className="text-xl font-semibold text-teal-400 mb-6 text-center">Per-Candidate Complexity</h3>
          
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left py-3 px-4 text-slate-400">Approach</th>
                  <th className="text-center py-3 px-4 text-slate-400">Per-candidate cost</th>
                  <th className="text-center py-3 px-4 text-slate-400">k=10</th>
                  <th className="text-center py-3 px-4 text-slate-400">k=15</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-slate-800">
                  <td className="py-3 px-4 text-rose-400">Classical (permutations)</td>
                  <td className="text-center py-3 px-4 font-mono text-rose-300">O(k!)</td>
                  <td className="text-center py-3 px-4 font-mono text-rose-300">3.6M</td>
                  <td className="text-center py-3 px-4 font-mono text-rose-300">1.3T</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="py-3 px-4 text-emerald-400">QWL (dense graph)</td>
                  <td className="text-center py-3 px-4 font-mono text-emerald-300">O(k²)</td>
                  <td className="text-center py-3 px-4 font-mono text-emerald-300">100</td>
                  <td className="text-center py-3 px-4 font-mono text-emerald-300">225</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-cyan-400">QWL (sparse graph)</td>
                  <td className="text-center py-3 px-4 font-mono text-cyan-300">O(k)</td>
                  <td className="text-center py-3 px-4 font-mono text-cyan-300">10</td>
                  <td className="text-center py-3 px-4 font-mono text-cyan-300">15</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-6 flex justify-center">
            <svg width={400} height={180}>
              {/* Axes */}
              <line x1={60} y1={150} x2={380} y2={150} stroke="#475569" strokeWidth={2}/>
              <line x1={60} y1={150} x2={60} y2={20} stroke="#475569" strokeWidth={2}/>
              
              {/* Y-axis label */}
              <text x={25} y={90} fill="#64748b" fontSize="11" transform="rotate(-90, 25, 90)">log(cost)</text>
              
              {/* X-axis label */}
              <text x={220} y={175} fill="#64748b" fontSize="11" textAnchor="middle">subgraph size k</text>
              
              {/* Grid lines */}
              {[40, 70, 100, 130].map(y => (
                <line key={y} x1={60} y1={y} x2={380} y2={y} stroke="#334155" strokeWidth={1} strokeDasharray="4"/>
              ))}
              
              {/* Classical line (exponential) */}
              <path d="M 80 140 Q 150 130 200 100 T 350 30" stroke="#f43f5e" strokeWidth={3} fill="none"/>
              <circle cx={350} cy={30} r={4} fill="#f43f5e"/>
              <text x={355} y={35} fill="#f43f5e" fontSize="10">k!</text>
              
              {/* QWL dense (quadratic) */}
              <path d="M 80 145 L 200 130 L 350 100" stroke="#10b981" strokeWidth={3} fill="none"/>
              <circle cx={350} cy={100} r={4} fill="#10b981"/>
              <text x={355} y={105} fill="#10b981" fontSize="10">k²</text>
              
              {/* QWL sparse (linear) */}
              <path d="M 80 147 L 350 135" stroke="#06b6d4" strokeWidth={3} fill="none"/>
              <circle cx={350} cy={135} r={4} fill="#06b6d4"/>
              <text x={355} y={140} fill="#06b6d4" fontSize="10">k</text>
              
              {/* X-axis ticks */}
              {[2, 5, 8, 11, 14].map((k, i) => (
                <g key={k}>
                  <line x1={80 + i*70} y1={150} x2={80 + i*70} y2={155} stroke="#475569" strokeWidth={2}/>
                  <text x={80 + i*70} y={165} fill="#64748b" fontSize="10" textAnchor="middle">{k}</text>
                </g>
              ))}
            </svg>
          </div>
        </div>
      </div>
    </div>
  );

  const Slide5 = () => (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-center bg-gradient-to-r from-amber-400 to-rose-400 bg-clip-text text-transparent">
        Key Properties
      </h2>

      <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-6">
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-emerald-900/50 flex items-center justify-center text-xl">🎯</div>
            <h3 className="text-lg font-semibold text-emerald-400">Permutation Invariance</h3>
          </div>
          <p className="text-slate-300 text-sm">
            Sorted probability vectors are <span className="text-emerald-300 font-semibold">identical</span> for 
            isomorphic graphs regardless of node ordering. No explicit mapping required.
          </p>
          <div className="mt-3 font-mono text-xs text-slate-500">
            G ≅ H → fingerprint(G) = fingerprint(H)
          </div>
        </div>

        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-amber-900/50 flex items-center justify-center text-xl">⚡</div>
            <h3 className="text-lg font-semibold text-amber-400">Shallow Circuits</h3>
          </div>
          <p className="text-slate-300 text-sm">
            Circuit depth scales with number of <span className="text-amber-300 font-semibold">edges</span>, not 
            permutations. Dense: O(k²), Sparse: O(k).
          </p>
          <div className="mt-3 font-mono text-xs text-slate-500">
            depth ∝ |E| · repetitions
          </div>
        </div>

        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-violet-900/50 flex items-center justify-center text-xl">🔢</div>
            <h3 className="text-lg font-semibold text-violet-400">Truncated Vectors</h3>
          </div>
          <p className="text-slate-300 text-sm">
            Only top <span className="text-violet-300 font-semibold">O(k)</span> probabilities needed for 
            discrimination. Reduces classical post-processing.
          </p>
          <div className="mt-3 font-mono text-xs text-slate-500">
            truncate_length = 4k typical
          </div>
        </div>

        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-full bg-rose-900/50 flex items-center justify-center text-xl">🧪</div>
            <h3 className="text-lg font-semibold text-rose-400">Early Pruning</h3>
          </div>
          <p className="text-slate-300 text-sm">
            Degree sequence check <span className="text-rose-300 font-semibold">before</span> quantum circuit 
            execution. Skips obviously non-isomorphic candidates.
          </p>
          <div className="mt-3 font-mono text-xs text-slate-500">
            if sorted(deg_H) ≠ sorted(deg_G[S]): skip
          </div>
        </div>
      </div>

      <div className="bg-slate-900/50 rounded-lg p-4 max-w-2xl mx-auto">
        <div className="flex items-center justify-center gap-8">
          <div className="text-center">
            <div className="text-3xl font-bold text-cyan-400">k</div>
            <div className="text-xs text-slate-400">qubits</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-emerald-400">r·|E|</div>
            <div className="text-xs text-slate-400">RZZ gates</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-amber-400">O(shots)</div>
            <div className="text-xs text-slate-400">measurements</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-violet-400">O(k log k)</div>
            <div className="text-xs text-slate-400">classical sort</div>
          </div>
        </div>
      </div>
    </div>
  );

  const slides = [
    { title: 'Classical WL', component: <Slide1 /> },
    { title: 'QWL Circuit', component: <Slide2 /> },
    { title: 'Fingerprints', component: <Slide3 /> },
    { title: 'Algorithm', component: <Slide4 /> },
    { title: 'Properties', component: <Slide5 /> },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">
            Quantum Weisfeiler-Lehman
          </h1>
          <p className="text-slate-400">Fingerprint-Based Subgraph Isomorphism</p>
          <p className="text-slate-500 text-sm">QAMP 2025</p>
        </div>
        
        {/* Slide navigation */}
        <div className="flex justify-center gap-2 mb-8 flex-wrap">
          {slides.map((slide, i) => (
            <button
              key={i}
              onClick={() => setActiveSlide(i)}
              className={`px-4 py-2 rounded-lg transition-all ${
                activeSlide === i 
                  ? 'bg-slate-700 text-white' 
                  : 'bg-slate-800/50 text-slate-400 hover:bg-slate-800'
              }`}
            >
              {slide.title}
            </button>
          ))}
        </div>
        
        {/* Active slide */}
        <div className="bg-slate-900/50 rounded-2xl p-8 border border-slate-800 min-h-[600px]">
          {slides[activeSlide].component}
        </div>
        
        {/* Navigation arrows */}
        <div className="flex justify-between mt-6">
          <button
            onClick={() => setActiveSlide(Math.max(0, activeSlide - 1))}
            disabled={activeSlide === 0}
            className="px-6 py-2 rounded-lg bg-slate-800 text-slate-300 disabled:opacity-30 hover:bg-slate-700 transition-colors"
          >
            ← Previous
          </button>
          <span className="text-slate-500 self-center">
            {activeSlide + 1} / {slides.length}
          </span>
          <button
            onClick={() => setActiveSlide(Math.min(slides.length - 1, activeSlide + 1))}
            disabled={activeSlide === slides.length - 1}
            className="px-6 py-2 rounded-lg bg-slate-800 text-slate-300 disabled:opacity-30 hover:bg-slate-700 transition-colors"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
};

export default QWLDiagrams;
