'use client';
import { useUser } from '@auth0/nextjs-auth0';

export default function Playground() {
    //react component for playground page UI
    const { user, isLoading } = useUser();

    //handle edge cases
    if (isLoading) return <p>Loading ...</p>
    if (!user) return <p>Please sign in to enter Playground</p>

    return (
        <main className="p-8">
            <h1 className="text-2xl font-bold mb-4">Your Playground</h1>
            <p className="mb-4"> Prompt: What is the best advice you have recieved?</p>
            <button className="bg-green-600 text-white px-4 py-2 rounded">Record</button>
        </main>
    );
}