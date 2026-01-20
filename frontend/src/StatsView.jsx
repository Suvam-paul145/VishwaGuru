import React, { useState, useEffect } from 'react';
import { BarChart, PieChart, Activity, AlertCircle } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || '';

const StatsView = ({ onBack }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await fetch(`${API_URL}/api/stats`);
                if (response.ok) {
                    const data = await response.json();
                    setStats(data);
                } else {
                    throw new Error('Failed to fetch stats');
                }
            } catch (err) {
                console.error(err);
                setError("Could not load statistics.");
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    return (
        <div className="mt-6 w-full max-w-lg mx-auto p-4">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <BarChart className="text-purple-600" />
                City Statistics
            </h2>

            {loading && (
                 <div className="flex justify-center p-8">
                     <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                 </div>
            )}

            {error && (
                <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-4 flex gap-2">
                    <AlertCircle size={20} />
                    {error}
                </div>
            )}

            {stats && (
                <div className="space-y-6">
                    {/* Summary Card */}
                    <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl p-6 text-white shadow-lg">
                        <p className="text-purple-200 text-sm font-medium uppercase tracking-wider mb-1">Total Issues Reported</p>
                        <p className="text-4xl font-bold">{stats.total}</p>
                    </div>

                    {/* Category Breakdown */}
                    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                        <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
                            <PieChart size={18} className="text-gray-500" />
                            Issues by Category
                        </h3>

                        <div className="space-y-4">
                            {stats.by_category.length > 0 ? (
                                stats.by_category.sort((a,b) => b.count - a.count).map((item) => (
                                    <div key={item.category}>
                                        <div className="flex justify-between text-sm mb-1">
                                            <span className="capitalize font-medium text-gray-700">{item.category}</span>
                                            <span className="text-gray-500">{item.count}</span>
                                        </div>
                                        <div className="w-full bg-gray-100 rounded-full h-2">
                                            <div
                                                className="bg-purple-500 h-2 rounded-full transition-all duration-1000"
                                                style={{ width: `${stats.total > 0 ? (item.count / stats.total) * 100 : 0}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p className="text-gray-500 text-sm text-center py-4">No data available yet.</p>
                            )}
                        </div>
                    </div>
                </div>
            )}

            <button
                onClick={onBack}
                className="mt-8 w-full text-gray-500 hover:text-gray-900 underline text-center"
            >
                Back to Home
            </button>
        </div>
    );
};

export default StatsView;
