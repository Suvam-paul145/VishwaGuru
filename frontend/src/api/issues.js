import { apiClient } from './client';
import { fakeRecentIssues } from '../fakeData';

export const issuesApi = {
  getRecent: async () => {
    try {
      return await apiClient.get('/api/issues/recent');
    } catch (error) {
      console.warn('Failed to fetch recent issues, using fake data', error);
      return fakeRecentIssues;
    }
  },

  create: async (formData) => {
    // formData is expected to be a FormData object containing 'file', 'description', etc.
    return await apiClient.postForm('/api/issues', formData);
  },

  vote: async (id) => {
    return await apiClient.post(`/api/issues/${id}/vote`, {}); // The backend endpoint might not require a body for upvote
  },

  getById: async (id) => {
    try {
      return await apiClient.get(`/api/issues/${id}`);
    } catch (error) {
      console.warn(`Failed to fetch issue ${id}, using fake data if available`, error);
      // Fallback logic could be complex here, for now just return null or throw
      // The component handles null/loading
      return null;
    }
  }
};
