'use client'

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function MlSegmentationPage() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [formData, setFormData] = useState({
    algorithm: 'kmeans',
    n_clusters: 3,
    name_prefix: 'ML Segment',
  })

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const response = await fetch(
        '/api/segments/create_ml_segments/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        }
      )

      if (!response.ok) {
        throw new Error('Failed to create ML segments')
      }

      const data = await response.json()
      router.push('/segments')
    } catch (error) {
      console.error('Error creating ML segments:', error)
      alert('Failed to create ML segments. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'n_clusters' ? parseInt(value, 10) : value,
    }))
  }

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Link
            href="/segments"
            className="text-blue-600 hover:underline"
          >
            &larr; Back to Segments
          </Link>
          <h1 className="text-2xl font-bold">ML Segmentation</h1>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Generate ML Segments
              </h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                Use machine learning to automatically segment your
                patients based on patterns in their data
              </p>
            </div>

            <div className="px-4 py-5 sm:p-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label
                    htmlFor="algorithm"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Algorithm
                  </label>
                  <select
                    id="algorithm"
                    name="algorithm"
                    value={formData.algorithm}
                    onChange={handleInputChange}
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="kmeans">K-Means Clustering</option>
                    <option value="dbscan">
                      DBSCAN (Density-Based Clustering)
                    </option>
                    <option value="hierarchical">
                      Hierarchical Clustering
                    </option>
                  </select>
                  <p className="mt-1 text-sm text-gray-500">
                    {formData.algorithm === 'kmeans'
                      ? 'K-Means groups patients into a specified number of clusters based on similarity.'
                      : formData.algorithm === 'dbscan'
                      ? 'DBSCAN finds clusters of varying shapes and sizes based on density.'
                      : 'Hierarchical clustering builds a tree of clusters, useful for nested patient groups.'}
                  </p>
                </div>

                <div>
                  <label
                    htmlFor="n_clusters"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Number of Clusters
                  </label>
                  <input
                    type="number"
                    name="n_clusters"
                    id="n_clusters"
                    min={2}
                    max={10}
                    value={formData.n_clusters}
                    onChange={handleInputChange}
                    className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    How munknown distinct patient segments to create
                    (between 2-10)
                  </p>
                </div>

                <div>
                  <label
                    htmlFor="name_prefix"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Segment Name Prefix
                  </label>
                  <input
                    type="text"
                    name="name_prefix"
                    id="name_prefix"
                    value={formData.name_prefix}
                    onChange={handleInputChange}
                    className="mt-1 focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Generated segments will be named with this prefix
                    followed by a number
                  </p>
                </div>

                <div className="flex justify-end">
                  <Link
                    href="/segments"
                    className="mr-3 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    Cancel
                  </Link>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
                      isSubmitting
                        ? 'bg-blue-400'
                        : 'bg-blue-600 hover:bg-blue-700'
                    } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                  >
                    {isSubmitting
                      ? 'Generating...'
                      : 'Generate Segments'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                About ML Segmentation
              </h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-4">
                <p className="text-sm text-gray-500">
                  ML segmentation analyzes patient data to
                  automatically group similar patients together,
                  helping you create targeted campaigns based on
                  hidden patterns.
                </p>

                <div>
                  <h4 className="text-sm font-medium text-gray-700">
                    How it works:
                  </h4>
                  <ol className="mt-2 list-decimal list-inside text-sm text-gray-600 space-y-1">
                    <li>AI analyzes your patient database</li>
                    <li>
                      Similar patients are grouped into segments
                    </li>
                    <li>
                      Each segment receives an AI-generated
                      description
                    </li>
                    <li>
                      You can use these segments for targeted
                      campaigns
                    </li>
                  </ol>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-700">
                    Algorithms:
                  </h4>
                  <dl className="mt-2 space-y-2 text-sm">
                    <div>
                      <dt className="font-medium text-gray-600">
                        K-Means
                      </dt>
                      <dd className="text-gray-500">
                        Best for creating a specific number of evenly
                        distributed segments
                      </dd>
                    </div>
                    <div>
                      <dt className="font-medium text-gray-600">
                        DBSCAN
                      </dt>
                      <dd className="text-gray-500">
                        Good for discovering natural clusters of
                        varying sizes and identifying outliers
                      </dd>
                    </div>
                    <div>
                      <dt className="font-medium text-gray-600">
                        Hierarchical
                      </dt>
                      <dd className="text-gray-500">
                        Creates nested clusters, good for
                        understanding relationships between patient
                        groups
                      </dd>
                    </div>
                  </dl>
                </div>

                <div className="pt-3 mt-4 border-t border-gray-200">
                  <h4 className="text-sm font-medium text-gray-700">
                    Features used for segmentation:
                  </h4>
                  <ul className="mt-2 list-disc list-inside text-sm text-gray-600 space-y-1">
                    <li>Demographics (age, gender, location)</li>
                    <li>Engagement history</li>
                    <li>Response patterns</li>
                    <li>Communication preferences</li>
                    <li>Campaign interaction history</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
