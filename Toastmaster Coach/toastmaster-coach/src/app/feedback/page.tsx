'use client';
import {useUser } from '@auth0/nextjs-auth0'
export default function Feedback() {
    //react component for feedback page UI
    const { user, isLoading } = useUser();

    //handle edge cases
    if (isLoading) return <p>Loading ...</p>
    if (!user) return <p>Please sign in to view feedback</p>
    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold mb-4"> Let's Review</h1>
            <section className="space-y-4">
                <div>
                    <h2 className="font-semibold">Voice & Delivery</h2>
                    <p>Body text for main takeaways, quotes or anecdotes</p>
                </div>
                <div>
                    <h2 className="font-semibold">Structure & Timing </h2>
                    <p>Body text for main takeaways, quotes or anecdotes</p>
                </div>
                <div>
                    <h2 className="font-semibold">Emotional Cues</h2>
                    <p>Body text for main takeaways, quotes or anecdotes</p>
                </div>
            </section>
        </main>
    );
}