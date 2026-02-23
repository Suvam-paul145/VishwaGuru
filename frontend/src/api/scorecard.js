import { apiClient } from './client';

export const scorecardApi = {
    getScorecard: async () => {
        try {
            return await apiClient.get('/api/scorecard');
        } catch (error) {
            console.warn('Failed to fetch scorecard data', error);
            return {
                departments: [],
                regions: [],
                department_trends: {},
                region_trends: {},
                generated_at: new Date().toISOString(),
                cache_ttl_seconds: 300,
            };
        }
    },
};
