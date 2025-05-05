'use client'

import { ChevronDown } from 'lucide-react'
import React from 'react'

export function FaqItem({ question, answer }) {
  const [isOpen, setIsOpen] = React.useState(false)

  return (
    <div className="border-b border-gray-200 py-6">
      <button
        className="flex w-full justify-between items-center text-left"
        onClick={() => setIsOpen(!isOpen)}
      >
        <h3 className="text-lg font-semibold text-gray-900">
          {question}
        </h3>
        <div
          className={`transform transition-transform duration-300 ${
            isOpen ? 'rotate-180' : ''
          }`}
        >
          <ChevronDown className="h-5 w-5 text-gray-500" />
        </div>
      </button>
      <div
        className={`mt-2 text-gray-600 overflow-hidden transition-all duration-300 ${
          isOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <p className="pt-2">{answer}</p>
      </div>
    </div>
  )
}
