// frontend/src/components/FileUpload.tsx
import React, { useState } from 'react';
import { uploadFile } from '@/lib/api';

export default function FileUpload({ clientId }: { clientId: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    try {
      await uploadFile(clientId, file);
      setStatus('success');
    } catch (error) {
      setStatus('error');
    }
  };

  return (
    <div className="p-4 bg-white border rounded-xl shadow-sm space-y-4">
      <h3 className="font-semibold text-slate-700">Ingestão de Documentos</h3>
      <div className="flex flex-col gap-3">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button
          onClick={handleUpload}
          disabled={!file || status === 'uploading'}
          className="w-full py-2 bg-slate-800 text-white rounded-md hover:bg-slate-900 transition-colors disabled:bg-slate-300"
        >
          {status === 'uploading' ? 'Indexando Documentos...' : 'Adicionar ao Caderno'}
        </button>
        {status === 'success' && <p className="text-green-600 text-xs text-center">Documento integrado com sucesso!</p>}
        {status === 'error' && <p className="text-red-600 text-xs text-center">Erro ao processar arquivo.</p>}
      </div>
    </div>
  );
}
