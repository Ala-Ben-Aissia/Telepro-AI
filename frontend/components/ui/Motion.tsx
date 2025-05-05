'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface FadeInProps {
  children: ReactNode
  delay?: number
  duration?: number
  className?: string
}

const FadeIn = ({
  children,
  delay = 0,
  duration = 0.5,
  className = '',
}: FadeInProps) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration, delay, ease: 'easeOut' }}
    className={className}
  >
    {children}
  </motion.div>
)

interface StaggerContainerProps {
  children: ReactNode
  className?: string
  delayChildren?: number
  staggerChildren?: number
}

const StaggerContainer = ({
  children,
  className = '',
  delayChildren = 0.1,
  staggerChildren = 0.1,
}: StaggerContainerProps) => (
  <motion.div
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true }}
    variants={{
      hidden: { opacity: 0 },
      visible: {
        opacity: 1,
        transition: {
          delayChildren,
          staggerChildren,
        },
      },
    }}
    className={className}
  >
    {children}
  </motion.div>
)

interface StaggerItemProps {
  children: ReactNode
  className?: string
}

const StaggerItem = ({
  children,
  className = '',
}: StaggerItemProps) => (
  <motion.div
    variants={{
      hidden: { opacity: 0, y: 20 },
      visible: {
        opacity: 1,
        y: 0,
        transition: { duration: 0.5, ease: 'easeOut' },
      },
    }}
    className={className}
  >
    {children}
  </motion.div>
)

interface AnimatedGradientTextProps {
  children: ReactNode
  className?: string
}

const AnimatedGradientText = ({
  children,
  className = '',
}: AnimatedGradientTextProps) => (
  <motion.div
    initial={{ opacity: 0, clipPath: 'inset(0 100% 0 0)' }}
    whileInView={{ opacity: 1, clipPath: 'inset(0 0% 0 0)' }}
    viewport={{ once: true }}
    transition={{ duration: 0.8, delay: 0.2, ease: 'easeOut' }}
    className={className}
  >
    {children}
  </motion.div>
)

export { FadeIn, StaggerContainer, StaggerItem, AnimatedGradientText }
