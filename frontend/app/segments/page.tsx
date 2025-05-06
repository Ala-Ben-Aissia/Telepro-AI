import { getSegments, analyzeSegment } from '@/app/api/actions';
import Link from 'next/link';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function SegmentsPage() {
  const segments = await getSegments();
  
  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Patient Segments</h1>
          <p className="text-gray-600">Create and manage patient segments for targeted campaigns</p>
        </div>
        
        <div className="flex space-x-3">
          <Link
            href="/segments/ml"
            className="flex items-center px-4 py-2 bg-gray-700 text-white rounded-md text-sm font-medium"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-4 w-4 mr-2" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            ML Segmentation
          </Link>
          <Link
            href="/segments/new"
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium"
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-4 w-4 mr-2" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Segment
          </Link>
        </div>
      </header>
      
      {/* Segments Table */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Segment List
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Patient segments for targeted communication campaigns
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Criteria
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {segments.length > 0 ? (
                segments.map((segment) => (
                  <tr key={segment.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link href={`/segments/${segment.id}`} className="text-blue-600 hover:text-blue-900 font-medium">
                        {segment.name}
                      </Link>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900 line-clamp-2">{segment.description}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        segment.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {segment.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex flex-wrap gap-1">
                        {segment.criteria && Object.entries(segment.criteria).slice(0, 3).map(([key, value]) => (
                          <span key={key} className="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs">
                            {typeof value === 'object' 
                              ? `${key}: ${Object.keys(value).length} filters` 
                              : `${key}: ${String(value).substring(0, 10)}${String(value).length > 10 ? '...' : ''}`
                            }
                          </span>
                        ))}
                        {segment.criteria && Object.keys(segment.criteria).length > 3 && (
                          <span className="px-2 py-1 bg-gray-50 text-gray-700 rounded-full text-xs">
                            +{Object.keys(segment.criteria).length - 3} more
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(segment.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex justify-end space-x-3">
                        <Link href={`/segments/${segment.id}`} className="text-blue-600 hover:text-blue-900">
                          View
                        </Link>
                        <Link href={`/segments/${segment.id}/edit`} className="text-gray-600 hover:text-gray-900">
                          Edit
                        </Link>
                        <form action={`/api/segments/${segment.id}/analyze`} method="POST">
                          <button type="submit" className="text-green-600 hover:text-green-900">
                            Analyze
                          </button>
                        </form>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-10 text-center">
                    <p className="text-gray-500 mb-4">No segments found</p>
                    <div className="flex justify-center space-x-3">
                      <Link
                        href="/segments/new"
                        className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium"
                      >
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          className="h-4 w-4 mr-2" 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        Create Manual Segment
                      </Link>
                      <Link
                        href="/segments/ml"
                        className="inline-flex items-center px-4 py-2 bg-gray-700 text-white rounded-md text-sm font-medium"
                      >
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          className="h-4 w-4 mr-2" 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        Generate ML Segments
                      </Link>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Segment Types Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Manual Segments
            </h3>
          </div>
          <div className="px-4 py-5 sm:p-6">
            <p className="text-sm text-gray-500 mb-4">
              Create custom segments based on specific criteria like age groups, location, preferred contact methods, and more.
            </p>
            <ul className="mt-3 list-disc list-inside text-sm text-gray-600 space-y-2">
              <li>Target specific demographic groups</li>
              <li>Filter by engagement levels</li>
              <li>Segment by communication preferences</li>
              <li>Create custom rules for specialized targeting</li>
            </ul>
            <div className="mt-6">
              <Link
                href="/segments/new"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
              >
                Create Manual Segment
              </Link>
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              ML-Generated Segments
            </h3>
          </div>
          <div className="px-4 py-5 sm:p-6">
            <p className="text-sm text-gray-500 mb-4">
              Let AI discover patterns in your patient data and create intelligent segments based on behavior, engagement, and demographics.
            </p>
            <ul className="mt-3 list-disc list-inside text-sm text-gray-600 space-y-2">
              <li>Discover hidden patterns in patient behavior</li>
              <li>Group similar patients automatically</li>
              <li>Optimize campaign targeting based on AI insights</li>
              <li>Use clustering algorithms to identify natural patient groups</li>
            </ul>
            <div className="mt-6">
              <Link
                href="/segments/ml"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gray-700 hover:bg-gray-800"
              >
                Generate ML Segments
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
