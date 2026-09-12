import { LandingPage } from './components/LandingPage';
import { Dashboard } from './features/requests/Dashboard';
import './styles/global.css';

export default function App() {
  const path = window.location.pathname;

  if (path === '/dashboard' || path.startsWith('/dashboard/')) {
    return <Dashboard />;
  }

  return <LandingPage />;
}
