import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import RobotAPI from '../../utilities/RobotAPI';

const Footer = () => {

    const [isOnMovement, setIsOnMovement] = useState(false);
    const address = useLocation();
    const navigate = useNavigate();
    const isOnMainMenu = address.pathname === '/';

    useEffect(() => {
        if (address.pathname === '/movement') {
            setIsOnMovement(true)
        } else {
            setIsOnMovement(false)
        }
    }, [address])

    return(
        
        <div className="footer">
            {isOnMainMenu && <img className="footer_stop" src="./imgs/stop.png" onClick={RobotAPI.stopRobot}/>}
            <p>SD2024</p>
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