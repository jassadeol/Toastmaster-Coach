'use client'; //open client browser 
import { useUser } from '@auth0/nextjs-auth0'; //react hook  current user session

export default function Login() { //react component for login page UI
    const { user, error, isLoading } = useUser();

    //handle edge cases
    if (isLoading) return <p>Loading ...</p>
    if (error) return <p>{error.message}</p>

    return (
        <main className="flex flex-col items-center justify-center h-screen">
            {user ? ( //user exists
                <>
                    <h1>Welcome, {user.name}</h1>
                    <a href="/api/auth/logout" className="text-blue-600">Logout</a>
                </>
            ) : (
                <a href="/api/auth/login" className="px-4 py-2 bg-blue-600 text-white rounded">Login</a>
            )}
        </main>
    );
}