import { useState } from "react";
import { Sparkles, ArrowRight } from "lucide-react";
import CountUp from "react-countup";

const features = ["Fast sync", "Smart tags", "Team spaces"];

export default function App() {
  const [open, setOpen] = useState(false);
  return (
    <main className="min-h-screen bg-white">
      <section className="text-center py-24 px-6 bg-gradient-to-r from-purple-600 to-blue-500">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent">Elevate your notes seamlessly</h1>
        <p className="mt-4 text-lg text-gray-500">The AI notebook for teams.</p>
        <button className="mt-8 px-6 py-3 rounded-lg bg-indigo-600 text-white outline-none">Get Started <ArrowRight /></button>
      </section>
      <section className="grid grid-cols-3 gap-6 p-8">
        {features.map((f) => (
          <div key={f} className="rounded-2xl shadow-lg p-6 bg-white">
            <Sparkles className="text-indigo-500" />
            <h3 className="mt-4 text-xl font-semibold">{f}</h3>
          </div>
        ))}
        <div className="rounded-2xl shadow-lg p-6 bg-white">Teams</div>
        <div className="rounded-2xl shadow-lg p-5 bg-slate-50">Notes</div>
      </section>
      <div className="p-8 text-sm" onClick={() => setOpen(!open)}><CountUp end={12000} /> notes taken. Oops, that's a lot.</div>
      <p className="text-xs text-gray-400">Syncing...</p>
      <button className="transition-all">Submit</button>
    </main>
  );
}
