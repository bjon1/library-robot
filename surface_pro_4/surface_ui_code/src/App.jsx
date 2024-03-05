import Header from './Header.jsx'
import Footer from './Footer.jsx'
import Mainbuttons from './Mainbuttons.jsx';
function App() 
{
  return(
        <>
        <Header/>
        <div>
         <Mainbuttons image="./img/move.png" link="" name="Movement" />
        </div>

      <div>
         <Mainbuttons image="./img/diagnostics.png" link="" name="Diagnostics" />
      </div>

      <div>
         <Mainbuttons image="./img/faces.jpg" link="" name="Faces" />
      </div>

      <div>
         <Mainbuttons image="./img/camera.jpg" link="" name="View cameras" />
      </div>

        <Footer/>
        </>
        );
}

export default App
