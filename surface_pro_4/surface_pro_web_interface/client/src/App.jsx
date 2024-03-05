import './App.css'

import { useRoutes } from 'react-router-dom'
import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'

import MainMenu from './MainMenu.jsx'
import Movement from './components/Movement.jsx'
import Diagnostics from './components/Diagnostics.jsx'
import Faces from './components/Faces.jsx'
import ViewCameras from './components/ViewCameras.jsx'
import Admin from './components/Admin.jsx'
import NotFound from './components/NotFound.jsx'

const App = () => {

   let element = useRoutes([
      {
         path: '/',
         element: <MainMenu />
      },
      {
         path: '/movement',
         element: <Movement />
      },
      {
         path: '/diagnostics',
         element: <Diagnostics />
      },
      {
         path: '/faces',
         element: <Faces />
      },
      {
         path: '/viewcameras',
         element: <ViewCameras />
      },
      {
         path: '/admin',
         element: <Admin />
      },
      { 
         path: '*', 
         element: <NotFound />
      }
   ])

   return(
      <div className = "App container">
         <Header/>
            <div className="App__center">
               {element}
            </div>
         <Footer/>
      </div>
   );
}

export default App
