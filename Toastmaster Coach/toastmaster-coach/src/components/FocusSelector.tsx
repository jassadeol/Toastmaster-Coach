'use client';
export default function FocusSelector() {
    const focuses = [
        { title: 'Voice Control', description: 'Improve vocal steadiness and tone.' },
        { title: 'Structure', description: 'Organize your ideas clearly.' },
        { title: 'Emotional Cues', description: 'Enhance impact using expression.' },
    ];

    return (
        <section className="mt-4">
            <h2 className="text-xl font-bold mb-2"> Select up to 3 focuses</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {focuses.map((focus, i) => (
                    <div key={i} className="border p-4 rounded-lg bg-gray-50 shadow-sm hover:bg-blue-50 transition">
                        <h3 className="text-lg font-semibold mb-1"> {focus.title}</h3>
                        <p className="text-sm text-gray-600">{focus.description}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}