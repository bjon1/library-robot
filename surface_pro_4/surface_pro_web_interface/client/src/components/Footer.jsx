import { useNavigate, useLocation } from 'react-router-dom';
import RobotAPI from '../../utilities/RobotAPI';

const Footer = () => {

    const navigate = useNavigate();
    const address = useLocation();
    const isOnMainMenu = address.pathname === '/';

    return(
        
        <div className="footer">
            <img className="footer_stop" src="./imgs/stop.png" onClick={RobotAPI.stopRobot}/>
            <p>&copy; {new Date().getFullYear()} SD2024</p>
            {isOnMainMenu && 
                <img 
                    className="footer_admin" 
                    src="./imgs/admin-tools.png" 
                    onClick={() => navigate('/admin')}
                />
            }
        </div>
   
    );

}
export default Footer