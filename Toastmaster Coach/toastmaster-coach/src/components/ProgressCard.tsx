'use client';
interface Props {
    title: string;
    value: number;
}

export default function ProgressCard({ title, value }: Props) {
    return (
        <div className="border rounded-lg p-4 bg-white shadow-sm w-full">
            <h2 className="text-lg font-semibold mb-2">{title}</h2>
            <div className="text-2xl font-bold text-blue-600"> {value}</div>
            <p className="text-sm text-gray-500 mt-1"> Progress Score</p>
        </div>

    );
}