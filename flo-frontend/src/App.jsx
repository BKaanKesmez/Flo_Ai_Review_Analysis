import { useState } from 'react'
import { searchReviews } from './api'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [onlyComplaints, setOnlyComplaints] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query) return

    setLoading(true)
    const data = await searchReviews(query , onlyComplaints)
    setResults(data)
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-3xl mx-auto">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-bold text-orange-600 mb-2">Flo AI Asistan</h1>
          <p className="text-gray-600">RAG Tabanlı Akıllı Müşteri Yorum Analizi</p>
        </header>

        <form onSubmit={handleSearch} className="flex gap-4 mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Kronik bir şikayet arayın (Örn: uncomfortable shoes)..."
            className="flex-1 p-4 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-orange-500 focus:outline-none"
          />
          <button 
            type="submit"
            className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 rounded-lg font-semibold transition"
          >
            Ara
          </button>
        </form>
        <div className="mt-4 flex items-center justify-center space-x-2">
            <input 
                type="checkbox" 
                id="complaint-filter"
                className="w-5 h-5 text-orange-600 rounded"
                checked={onlyComplaints}
                onChange={(e) => setOnlyComplaints(e.target.checked)}
            />
            <label htmlFor="complaint-filter" className="text-gray-700 font-medium">
                Sadece kronik şikayetleri (1-3 Yıldız) getir
            </label>
        </div>
        

        {loading && <p className="text-center text-orange-600 font-medium">Yapay Zeka Analiz Ediyor...</p>}

        <div className="space-y-4">
          {results.map((item, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-orange-500">
              <div className="flex justify-between items-center mb-3">
                <span className="text-sm font-bold text-gray-500 uppercase">{item.kategori}</span>
                <span className="bg-yellow-100 text-yellow-800 text-xs font-bold px-3 py-1 rounded">⭐ {item.puan}/5</span>
              </div>
              <p className="text-gray-700 mb-2">{item.yorum}</p>
              <p className="text-xs text-gray-400">Benzerlik Skoru: {item.uzaklik_skoru}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
