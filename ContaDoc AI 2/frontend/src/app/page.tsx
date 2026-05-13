// frontend/src/app/page.tsx
"use client";
import React, { useState } from 'react';
import ChatInterface from '@/components/ChatInterface';
import FileUpload from '@/components/FileUpload';

export default function Home() {
  const [clientId, setClientId] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold text-slate-800">ContaDoc AI</h1>
            <p className="text-slate-500">Assistente Inteligente para Escritórios de Contabilidade</p>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">ID do Cliente / Workspace</label>
              <input
                className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Ex: cliente_abc_2024"
                value={clientId}
                onChange={(e) => setClientId(e.target.value)}
              />
            </div>
            <button
              onClick={() => clientId && setIsLoggedIn(true)}
              className="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all"
            >
              Acessar Workspace
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 p-6">
      <header className="max-w-7xl mx-auto mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">ContaDoc AI Enterprise</h1>
          <p className="text-slate-500">Workspace: <span className="font-mono text-blue-600">{clientId}</span></p>
        </div>
        <button
          onClick={() => setIsLoggedIn(false)}
          className="text-sm text-slate-500 hover:text-red-600 transition-colors"
        >
          Sair do Workspace
        </button>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-160px)]">
        <div className="lg:col-span-1 space-y-6">
          <FileUpload clientId={clientId} />
          <div className="p-4 bg-white border rounded-xl shadow-sm">
            <h3 className="font-semibold text-slate-700 mb-2">Dicas de Pesquisa</h3>
            <ul className="text-xs text-slate-500 space-y-2">
              <li>• "Qual a variação de receita do último mês?"</li>
              <li>• "Resuma as pendências fiscais do contrato."</li>
              <li>• "Existem inconsistências no balancete?"</li>
            </ul>
          </div>
        </div>
        <div className="lg:col-span-3">
          <ChatInterface clientId={clientId} />
        </div>
      </main>
    </div>
  );
}
