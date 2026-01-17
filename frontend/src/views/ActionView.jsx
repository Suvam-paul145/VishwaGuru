import React, { useEffect, useState } from 'react';
import StatusTracker from '../components/StatusTracker';
import { issuesApi } from '../api/issues';

const ActionView = ({ actionPlan, setActionPlan, issueId, setView }) => {
  const [polling, setPolling] = useState(false);

  useEffect(() => {
    // If we have an issueId but no actionPlan, poll for it
    if (!actionPlan && issueId) {
      setPolling(true);
      const interval = setInterval(async () => {
        try {
          const issue = await issuesApi.getById(issueId);
          if (issue && issue.action_plan) {
            setActionPlan(issue.action_plan);
            setPolling(false);
            clearInterval(interval);
          }
        } catch (e) {
          console.error("Polling failed", e);
        }
      }, 2000); // Poll every 2 seconds

      return () => clearInterval(interval);
    }
  }, [actionPlan, issueId, setActionPlan]);

  if (!actionPlan) {
      if (polling) {
        return (
            <div className="mt-6 space-y-6 text-center">
                 <StatusTracker currentStep={2} /> {/* step 2 is "Analyzed", waiting for Plan */}
                 <div className="p-8">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <h3 className="text-xl font-semibold text-gray-700">Generating Action Plan...</h3>
                    <p className="text-gray-500 mt-2">Our AI is drafting the perfect complaint for you.</p>
                 </div>
            </div>
        );
      }
      return null;
  }

  return (
    <div className="mt-6 space-y-6">
      <StatusTracker currentStep={3} />

      <div className="bg-green-50 p-4 rounded-lg border border-green-200">
        <h2 className="text-xl font-bold text-green-800 mb-2">Action Plan Generated!</h2>
        <p className="text-green-700">Here are ready-to-use drafts to send to authorities.</p>
      </div>

      <div className="bg-white p-4 rounded shadow border">
        <h3 className="font-bold text-lg mb-2 flex items-center">
          <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm mr-2">WhatsApp</span>
        </h3>
        <div className="bg-gray-100 p-3 rounded text-sm mb-3 whitespace-pre-wrap">
          {actionPlan.whatsapp}
        </div>
        <a
          href={`https://wa.me/?text=${encodeURIComponent(actionPlan.whatsapp)}`}
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full text-center bg-green-500 text-white py-2 rounded hover:bg-green-600 transition"
        >
          Send on WhatsApp
        </a>
      </div>

      {actionPlan.x_post && (
        <div className="bg-white p-4 rounded shadow border">
          <h3 className="font-bold text-lg mb-2 flex items-center">
            <span className="bg-black text-white px-2 py-1 rounded text-sm mr-2">X.com</span>
          </h3>
          <div className="bg-gray-100 p-3 rounded text-sm mb-3 whitespace-pre-wrap">
            {actionPlan.x_post}
          </div>
          <a
            href={`https://x.com/intent/post?text=${encodeURIComponent(actionPlan.x_post)}`}
            target="_blank"
            rel="noopener noreferrer"
            className="block w-full text-center bg-slate-900 text-white py-2 rounded hover:bg-slate-800 transition"
          >
            Post on X.com
          </a>
        </div>
      )}

      <div className="bg-white p-4 rounded shadow border">
        <h3 className="font-bold text-lg mb-2">Email Draft</h3>
        <div className="mb-2">
          <span className="font-semibold text-gray-700">Subject:</span> {actionPlan.email_subject}
        </div>
        <div className="bg-gray-100 p-3 rounded text-sm mb-3 whitespace-pre-wrap">
          {actionPlan.email_body}
        </div>
        <a
          href={`mailto:?subject=${encodeURIComponent(actionPlan.email_subject)}&body=${encodeURIComponent(actionPlan.email_body)}`}
           className="block w-full text-center bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
        >
          Open in Email App
        </a>
      </div>

      <button onClick={() => setView('home')} className="text-blue-600 underline text-center w-full block">Back to Home</button>
    </div>
  );
};

export default ActionView;
