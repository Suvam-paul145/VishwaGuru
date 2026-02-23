import React, { useState, useEffect, useMemo } from 'react';
import { scorecardApi } from '../api';
import {
    ArrowLeft, Trophy, Building2, MapPin, TrendingUp, TrendingDown,
    Award, BarChart3, Clock, CheckCircle, AlertTriangle, RefreshCw
} from 'lucide-react';

const ScorecardView = ({ setView }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('departments');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await scorecardApi.getScorecard();
                setData(result);
            } catch (err) {
                console.error('Failed to fetch scorecard', err);
                setError('Unable to load scorecard data.');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const entries = useMemo(() => {
        if (!data) return [];
        return activeTab === 'departments' ? data.departments : data.regions;
    }, [data, activeTab]);

    const trends = useMemo(() => {
        if (!data) return {};
        return activeTab === 'departments' ? data.department_trends : data.region_trends;
    }, [data, activeTab]);

    const getRankBadge = (rank) => {
        if (rank === 1) return (
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-yellow-300 to-amber-500 shadow-lg shadow-yellow-200/50">
                <Trophy size={16} className="text-white" />
            </div>
        );
        if (rank === 2) return (
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-gray-300 to-gray-400 shadow-lg shadow-gray-200/50">
                <Award size={16} className="text-white" />
            </div>
        );
        if (rank === 3) return (
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-amber-500 to-orange-600 shadow-lg shadow-orange-200/50">
                <Award size={16} className="text-white" />
            </div>
        );
        return (
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-700">
                <span className="text-sm font-bold text-gray-500 dark:text-gray-300">{rank}</span>
            </div>
        );
    };

    const getScoreColor = (score) => {
        if (score >= 70) return 'text-emerald-600 dark:text-emerald-400';
        if (score >= 40) return 'text-amber-600 dark:text-amber-400';
        return 'text-red-600 dark:text-red-400';
    };

    const getScoreBg = (score) => {
        if (score >= 70) return 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-700';
        if (score >= 40) return 'bg-amber-50 dark:bg-amber-900/30 border-amber-200 dark:border-amber-700';
        return 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-700';
    };

    const getRateColor = (rate) => {
        if (rate >= 70) return 'text-emerald-600 dark:text-emerald-400';
        if (rate >= 40) return 'text-amber-600 dark:text-amber-400';
        return 'text-red-600 dark:text-red-400';
    };

    const renderMiniTrend = (name) => {
        const points = trends[name];
        if (!points || points.length === 0) return (
            <span className="text-xs text-gray-400 italic">No trend</span>
        );
        const maxRate = Math.max(...points.map(p => p.resolution_rate), 1);
        return (
            <div className="flex items-end gap-0.5 h-6">
                {points.map((p, i) => (
                    <div
                        key={p.period}
                        className="w-2.5 rounded-t transition-all duration-500 ease-out"
                        style={{
                            height: `${Math.max((p.resolution_rate / maxRate) * 100, 8)}%`,
                            backgroundColor: p.resolution_rate >= 70 ? '#10b981' : p.resolution_rate >= 40 ? '#f59e0b' : '#ef4444',
                            opacity: 0.5 + (i / points.length) * 0.5,
                        }}
                        title={`${p.period}: ${p.resolution_rate}%`}
                    />
                ))}
            </div>
        );
    };

    // Summary stats
    const summaryStats = useMemo(() => {
        if (!entries.length) return { totalGrievances: 0, avgResRate: 0, avgHours: 0, topPerformer: '-' };
        const totalGrievances = entries.reduce((sum, e) => sum + e.total_grievances, 0);
        const avgResRate = entries.reduce((sum, e) => sum + e.resolution_rate, 0) / entries.length;
        const avgHours = entries.reduce((sum, e) => sum + e.avg_resolution_hours, 0) / entries.length;
        const topPerformer = entries[0]?.name || '-';
        return { totalGrievances, avgResRate: avgResRate.toFixed(1), avgHours: avgHours.toFixed(1), topPerformer };
    }, [entries]);

    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
        </div>
    );

    if (error) return (
        <div className="p-8 text-center">
            <AlertTriangle className="mx-auto mb-3 text-red-400" size={40} />
            <p className="text-red-600 dark:text-red-400 font-medium">{error}</p>
        </div>
    );

    return (
        <div className="p-4 sm:p-6 max-w-6xl mx-auto space-y-6">
            {/* Header */}
            <div className="flex items-center gap-4">
                {setView && (
                    <button onClick={() => setView('home')} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition">
                        <ArrowLeft size={24} className="text-gray-600 dark:text-gray-300" />
                    </button>
                )}
                <div>
                    <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                        <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl shadow-lg shadow-indigo-200/50 dark:shadow-indigo-900/30">
                            <BarChart3 size={24} className="text-white" />
                        </div>
                        Resolution Scorecard
                    </h1>
                    <p className="text-gray-500 dark:text-gray-400 text-sm mt-1">
                        Public performance rankings for grievance resolution
                    </p>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-gradient-to-br from-indigo-50 to-blue-50 dark:from-indigo-900/30 dark:to-blue-900/30 p-4 rounded-xl border border-indigo-100 dark:border-indigo-800">
                    <p className="text-xs font-semibold text-indigo-500 dark:text-indigo-400 uppercase tracking-wider">Total Grievances</p>
                    <p className="text-2xl font-extrabold text-indigo-800 dark:text-indigo-200 mt-1">{summaryStats.totalGrievances}</p>
                </div>
                <div className="bg-gradient-to-br from-emerald-50 to-green-50 dark:from-emerald-900/30 dark:to-green-900/30 p-4 rounded-xl border border-emerald-100 dark:border-emerald-800">
                    <div className="flex items-center gap-1.5">
                        <CheckCircle size={12} className="text-emerald-500" />
                        <p className="text-xs font-semibold text-emerald-500 dark:text-emerald-400 uppercase tracking-wider">Avg Resolution</p>
                    </div>
                    <p className="text-2xl font-extrabold text-emerald-800 dark:text-emerald-200 mt-1">{summaryStats.avgResRate}%</p>
                </div>
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/30 dark:to-orange-900/30 p-4 rounded-xl border border-amber-100 dark:border-amber-800">
                    <div className="flex items-center gap-1.5">
                        <Clock size={12} className="text-amber-500" />
                        <p className="text-xs font-semibold text-amber-500 dark:text-amber-400 uppercase tracking-wider">Avg Time</p>
                    </div>
                    <p className="text-2xl font-extrabold text-amber-800 dark:text-amber-200 mt-1">{summaryStats.avgHours}h</p>
                </div>
                <div className="bg-gradient-to-br from-purple-50 to-fuchsia-50 dark:from-purple-900/30 dark:to-fuchsia-900/30 p-4 rounded-xl border border-purple-100 dark:border-purple-800">
                    <div className="flex items-center gap-1.5">
                        <Trophy size={12} className="text-purple-500" />
                        <p className="text-xs font-semibold text-purple-500 dark:text-purple-400 uppercase tracking-wider">Top Performer</p>
                    </div>
                    <p className="text-lg font-extrabold text-purple-800 dark:text-purple-200 mt-1 truncate">{summaryStats.topPerformer}</p>
                </div>
            </div>

            {/* Tab Switcher */}
            <div className="flex bg-gray-100 dark:bg-gray-800 rounded-xl p-1 gap-1">
                <button
                    onClick={() => setActiveTab('departments')}
                    className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${activeTab === 'departments'
                            ? 'bg-white dark:bg-gray-700 text-indigo-700 dark:text-indigo-300 shadow-sm'
                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                        }`}
                >
                    <Building2 size={16} /> Departments
                </button>
                <button
                    onClick={() => setActiveTab('regions')}
                    className={`flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-200 ${activeTab === 'regions'
                            ? 'bg-white dark:bg-gray-700 text-indigo-700 dark:text-indigo-300 shadow-sm'
                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                        }`}
                >
                    <MapPin size={16} /> Regions
                </button>
            </div>

            {/* Leaderboard Table */}
            <div className="bg-white dark:bg-gray-800/50 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
                {/* Table Header */}
                <div className="hidden md:grid grid-cols-12 bg-gray-50 dark:bg-gray-800 p-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider border-b border-gray-100 dark:border-gray-700">
                    <div className="col-span-1 text-center">Rank</div>
                    <div className="col-span-3">Name</div>
                    <div className="col-span-1 text-center">Total</div>
                    <div className="col-span-1 text-center">Resolved</div>
                    <div className="col-span-2 text-center">Resolution %</div>
                    <div className="col-span-1 text-center">Avg Time</div>
                    <div className="col-span-1 text-center">Score</div>
                    <div className="col-span-2 text-center">Trend</div>
                </div>

                {/* Table body */}
                <div className="divide-y divide-gray-50 dark:divide-gray-700/50">
                    {entries.length > 0 ? (
                        entries.map((entry) => (
                            <div key={entry.name} className="grid grid-cols-1 md:grid-cols-12 p-4 items-center gap-3 md:gap-0 hover:bg-gray-50/50 dark:hover:bg-gray-700/30 transition-colors">
                                {/* Mobile layout */}
                                <div className="md:hidden space-y-3">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-3">
                                            {getRankBadge(entry.rank)}
                                            <span className="font-semibold text-gray-800 dark:text-gray-200">{entry.name}</span>
                                        </div>
                                        <div className={`px-3 py-1 rounded-full border text-sm font-bold ${getScoreBg(entry.score)} ${getScoreColor(entry.score)}`}>
                                            {entry.score}
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-4 gap-2 text-center text-xs">
                                        <div>
                                            <p className="text-gray-400 dark:text-gray-500">Total</p>
                                            <p className="font-bold text-gray-700 dark:text-gray-300">{entry.total_grievances}</p>
                                        </div>
                                        <div>
                                            <p className="text-gray-400 dark:text-gray-500">Resolved</p>
                                            <p className="font-bold text-emerald-600 dark:text-emerald-400">{entry.resolved_count}</p>
                                        </div>
                                        <div>
                                            <p className="text-gray-400 dark:text-gray-500">Rate</p>
                                            <p className={`font-bold ${getRateColor(entry.resolution_rate)}`}>{entry.resolution_rate}%</p>
                                        </div>
                                        <div>
                                            <p className="text-gray-400 dark:text-gray-500">Avg Time</p>
                                            <p className="font-bold text-gray-700 dark:text-gray-300">{entry.avg_resolution_hours}h</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs text-gray-400">Trend:</span>
                                        {renderMiniTrend(entry.name)}
                                    </div>
                                </div>

                                {/* Desktop layout */}
                                <div className="hidden md:flex col-span-1 justify-center">{getRankBadge(entry.rank)}</div>
                                <div className="hidden md:flex col-span-3 items-center gap-2">
                                    <span className="font-semibold text-gray-800 dark:text-gray-200 truncate">{entry.name}</span>
                                    {entry.rank <= 3 && (
                                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-700">
                                            Top {entry.rank}
                                        </span>
                                    )}
                                </div>
                                <div className="hidden md:flex col-span-1 justify-center font-medium text-gray-600 dark:text-gray-300">{entry.total_grievances}</div>
                                <div className="hidden md:flex col-span-1 justify-center font-medium text-emerald-600 dark:text-emerald-400">{entry.resolved_count}</div>
                                <div className="hidden md:flex col-span-2 justify-center">
                                    <div className="flex items-center gap-2">
                                        <div className="w-16 bg-gray-100 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                                            <div
                                                className="h-2 rounded-full transition-all duration-700 ease-out"
                                                style={{
                                                    width: `${entry.resolution_rate}%`,
                                                    backgroundColor: entry.resolution_rate >= 70 ? '#10b981' : entry.resolution_rate >= 40 ? '#f59e0b' : '#ef4444'
                                                }}
                                            />
                                        </div>
                                        <span className={`text-sm font-bold ${getRateColor(entry.resolution_rate)}`}>{entry.resolution_rate}%</span>
                                    </div>
                                </div>
                                <div className="hidden md:flex col-span-1 justify-center text-sm text-gray-600 dark:text-gray-300 items-center gap-1">
                                    <Clock size={12} className="text-gray-400" />
                                    {entry.avg_resolution_hours}h
                                </div>
                                <div className="hidden md:flex col-span-1 justify-center">
                                    <span className={`px-2.5 py-1 rounded-lg border text-sm font-bold ${getScoreBg(entry.score)} ${getScoreColor(entry.score)}`}>
                                        {entry.score}
                                    </span>
                                </div>
                                <div className="hidden md:flex col-span-2 justify-center">{renderMiniTrend(entry.name)}</div>
                            </div>
                        ))
                    ) : (
                        <div className="p-12 text-center">
                            <BarChart3 className="mx-auto mb-3 text-gray-300 dark:text-gray-600" size={40} />
                            <p className="text-gray-400 dark:text-gray-500 text-sm">
                                No scorecard data available yet. Grievances need to be filed first.
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {/* Footer with cache info */}
            {data && (
                <div className="flex items-center justify-center gap-2 text-xs text-gray-400 dark:text-gray-500">
                    <RefreshCw size={10} />
                    <span>
                        Generated {new Date(data.generated_at).toLocaleString()} • Refreshes every {Math.round(data.cache_ttl_seconds / 60)} min
                    </span>
                </div>
            )}
        </div>
    );
};

export default ScorecardView;
