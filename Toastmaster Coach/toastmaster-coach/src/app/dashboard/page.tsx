'use client';
import { useUser } from '@auth0/nextjs-auth0';
import ProgressCard from '@/components/ProgressCard';
import FocusSelector from '@/components/FocusSelector';

export default function Dashboard() {
    const { user } = useUser();
    if (!user) return <p>Please log in to view your dashboard</p>

    return (
        <main className="p-8">
            <h1 className="text-2xl font-semibold mb4">Welcome back, {user.name}</h1>
            <FocusSelector/>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                    <ProgressCard title="Confidence" value={83} />
                    <ProgressCard title="Filler Words" value={5} />
                    <ProgressCard title="Engagement" value={74} />
                </div>
            
        </main>
    )
}