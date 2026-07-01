import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import Navbar         from './components/Navbar'
import Home           from './pages/Home'
import Chat           from './pages/Chat'
import Recommendation from './pages/Recommendation'

function PageWrapper({ children }) {
  return (
    <motion.div initial={{opacity:0,y:8}} animate={{opacity:1,y:0}}
      exit={{opacity:0,y:-8}} transition={{duration:0.25}}>
      {children}
    </motion.div>
  )
}

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/"          element={<PageWrapper><Home/></PageWrapper>}/>
        <Route path="/recommend" element={<PageWrapper><Recommendation/></PageWrapper>}/>
        <Route path="/chat"      element={<PageWrapper><Chat/></PageWrapper>}/>
      </Routes>
    </AnimatePresence>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar/>
      <AnimatedRoutes/>
    </BrowserRouter>
  )
}
