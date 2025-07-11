import Image from "next/image";

export default function Home() {
  return (
      <div className="min-h-screen flex flex-col items-center justify-center p-8 sm:p-20 bg-gray-50">
      <main className="text-center">
              <h1 className="text-4xl text-black font-bold mb-4"> Toastmaster AI Coach</h1>
              <p className="text-lg text-gray-600 mb-6">
              Your guide to perfecting public speech
              </p>
              <a href="/login" className="px-6 py-3 bg-green-800 text-white rounded hover:bg-blue-7">
              Sign in to begin
              </a>
      </main>
     
    </div>
  );
}
