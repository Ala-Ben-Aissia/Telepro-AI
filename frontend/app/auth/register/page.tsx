'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { register } from '@/app/api/actions'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [passwordConfirm, setPasswordConfirm] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    const res = await fetch('/api/accounts/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        email,
        password,
        password_confirm: passwordConfirm,
      }),
    })
    if (res.ok) {
      router.push('/auth/login')
    } else {
      setError('Registration failed')
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-8 rounded shadow-md w-full max-w-md"
    >
      <h1 className="text-2xl font-bold mb-6">Register</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <input
        type="username"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        className="w-full mb-4 p-2 border rounded"
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full mb-4 p-2 border rounded"
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full mb-6 p-2 border rounded"
        required
      />
      <input
        type="password"
        placeholder="PasswordConfirm"
        value={passwordConfirm}
        onChange={(e) => setPasswordConfirm(e.target.value)}
        className="w-full mb-6 p-2 border rounded"
        required
      />
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        onClick={() =>
          register(username, email, password, passwordConfirm)
        }
      >
        Register
      </button>
    </form>
  )
}
