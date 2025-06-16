import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [projectDescription, setProjectDescription] = useState('');
  const [projectDifficulty, setProjectDifficulty] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [projectId, setProjectId] = useState(null);
  const [recommendations, setRecommendations] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setRecommendations(null); // Clear previous recommendations on new submission

    if (!projectDescription || !projectDifficulty) {
      setError("Please fill in both project description and difficulty.");
      setLoading(false);
      return;
    }

    try {
      // Step 1: Submit Project and get Project ID
      const projectResponse = await fetch('http://localhost:8000/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description: projectDescription,
          project_complexity: projectDifficulty,
        }),
      });

      if (!projectResponse.ok) {
        throw new Error(`HTTP error! status: ${projectResponse.status}`);
      }

      const projectData = await projectResponse.json();
      console.log('Project created:', projectData);
      setProjectId(projectData.id);
      alert(`Project submitted successfully! Project ID: ${projectData.id}`);

      // Step 2: Fetch Recommendations using the Project ID
      const recommendationsResponse = await fetch('http://localhost:8000/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ project_id: projectData.id }),
      });

      if (!recommendationsResponse.ok) {
        throw new Error(`HTTP error! status: ${recommendationsResponse.status}`);
      }

      const recommendationsData = await recommendationsResponse.json();
      console.log('Recommendations fetched:', recommendationsData);
      setRecommendations(recommendationsData.recommendation); // Store the recommendation text

    } catch (e) {
      console.error('Error during submission or fetching recommendations:', e);
      setError('Failed to get tech stack. Please ensure the backend is running and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white p-8 flex flex-col items-center">
      <nav className="w-full max-w-4xl flex justify-between items-center mb-16">
        <h1 className="text-2xl font-bold text-gray-800">stack-own</h1>
        <a href="https://github.com/shreyap2702/stack-own" target="_blank" rel="noopener noreferrer" className="text-lg text-gray-600 hover:text-gray-900">github</a>
      </nav>

      <main className="flex flex-col items-center px-4">
        <div className="w-full max-w-2xl text-left mb-12">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Want your project to truly own its <span className="text-primary italic">tech-stack</span>?
          </h2>
          <p className="text-2xl font-bold text-gray-800">
            We've got you.
          </p>
        </div>

        <div className="w-full max-w-2xl text-left">
          <label htmlFor="project-description" className="block text-xl font-medium text-gray-700 mb-2">
            project name and its description
          </label>
          <textarea
            id="project-description"
            rows="4"
            placeholder="describe your project here, along with its name"
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary mb-8 text-lg"
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
          ></textarea>

          <label htmlFor="project-difficulty" className="block text-xl font-medium text-gray-700 mb-2">
            what is project difficulty?
          </label>
          <select
            id="project-difficulty"
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary mb-12 text-lg appearance-none bg-white pr-10 text-gray-500"
            value={projectDifficulty}
            onChange={(e) => setProjectDifficulty(e.target.value)}
          >
            <option value="">select one project difficulty for your project</option>
            <option value="simple">Simple</option>
            <option value="medium">Medium</option>
            <option value="complex">Hard</option>
          </select>

          {error && <p className="text-red-500 mb-4">{error}</p>}
          <button
            onClick={handleSubmit}
            className="w-full bg-primary-light text-primary font-bold py-4 px-6 rounded-lg text-xl hover:bg-primary hover:text-white transition-colors duration-200 flex items-center justify-center space-x-2"
            disabled={loading} // Disable button when loading
          >
            {loading ? (
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <>
                <span>Get your tech stack here</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                </svg>
              </>
            )}
          </button>
        </div>

        {recommendations && (
          <div className="w-full max-w-2xl mt-12 p-6 bg-gray-50 rounded-lg text-left">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Here is your optimal project tech stack.</h3>
            <div className="whitespace-pre-wrap text-gray-700 text-lg font-medium">
              {recommendations}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
