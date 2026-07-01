import { useState } from 'react'

const OCCUPATIONS = ['Farmer','Student','Labour','Women','Business','Teacher','Worker']
const STATES = [
  'Andhra Pradesh','Assam','Bihar','Chhattisgarh','Delhi','Goa','Gujarat',
  'Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh',
  'Maharashtra','Manipur','Meghalaya','Odisha','Punjab','Rajasthan','Sikkim',
  'Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal',
]

const fieldCls = 'w-full bg-[#0B1220] border border-white/8 rounded-xl px-4 py-2.5 text-sm text-gray-100 placeholder-gray-600 outline-none focus:border-orange-500/50 focus:ring-1 focus:ring-orange-500/20 transition-all'

export default function ProfileForm({ onSubmit, loading }) {
  const [form, setForm] = useState({ age:'', state:'', occupation:'', income:'', gender:'', top_k:10 })
  const set = (k,v) => setForm(f=>({...f,[k]:v}))

  const submit = e => {
    e.preventDefault()
    onSubmit({
      age:        form.age        ? Number(form.age)    : null,
      income:     form.income     ? Number(form.income) : null,
      state:      form.state      || null,
      occupation: form.occupation || null,
      gender:     form.gender     || null,
      top_k:      form.top_k,
    })
  }

  return (
    <form onSubmit={submit} className="space-y-5">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1.5">Age</label>
          <input type="number" placeholder="e.g. 28" className={fieldCls}
            value={form.age} onChange={e=>set('age',e.target.value)}/>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1.5">Annual Income (₹)</label>
          <input type="number" placeholder="e.g. 80000" className={fieldCls}
            value={form.income} onChange={e=>set('income',e.target.value)}/>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1.5">State</label>
          <select className={fieldCls} value={form.state} onChange={e=>set('state',e.target.value)}>
            <option value="">Select state</option>
            {STATES.map(s=><option key={s}>{s}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1.5">Occupation</label>
          <select className={fieldCls} value={form.occupation} onChange={e=>set('occupation',e.target.value)}>
            <option value="">Select occupation</option>
            {OCCUPATIONS.map(o=><option key={o}>{o}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1.5">Gender</label>
          <select className={fieldCls} value={form.gender} onChange={e=>set('gender',e.target.value)}>
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-400 mb-1.5">Number of Results</label>
          <select className={fieldCls} value={form.top_k} onChange={e=>set('top_k',Number(e.target.value))}>
            {[5,10,15,20].map(n=><option key={n} value={n}>{n} schemes</option>)}
          </select>
        </div>
      </div>

      <button type="submit" disabled={loading}
        className="w-full bg-[#F97316] hover:bg-[#EA6C0A] disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition-colors text-sm">
        {loading ? (
          <>
            <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="32" strokeDashoffset="12"/>
            </svg>
            Analysing…
          </>
        ) : (
          <>
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            Find My Schemes
          </>
        )}
      </button>
    </form>
  )
}
