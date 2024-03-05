
import { useNavigate } from 'react-router-dom'

const MainButtons = ({ image, link, name }) => {

   const navigate = useNavigate()

    return(
 
      <div className="menubutton">
         <img className="menuimg" src={image} onClick={ () => navigate(link)}/>
         <p className="menubutton__name">{name}</p>
      </div>

    )
 }
 
 export default MainButtons